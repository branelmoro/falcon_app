# always extend your controller from base_controller
# always give controller class name same as filename
from falcon import HTTP_200
from ..base_controller import baseController
from ..base_controller import appException

from ...resources.redis import redis as appCache

from datetime import datetime

from ...library import json

try:
	from hashlib import blake2b
except ImportError:
	from pyblake2 import blake2b

import base64

# import all required models here
from ...models.oauth2Model import oauth2ClientModel
from ...models.oauth2Model import oauth2ScopeModel
from ...models.oauth2Model import oauth2AdminUserModel
# from ...models.sampleModel import sampleModel

class index(baseController):

	def __init__(self):
		self.__path = "/token"
		self.aTokenDb = "token_scopeDb"
		self.rTokenDb = "refresh_tokenDb"
		self.sessionDb = "token_sessionDb"
		self.uTokenDb = "user_tokenDb"

		self.__accessTokenExpiry = 900
		self.__refreshTokenExpiry = 3600

	def getPath(self):
		return self.__path

	def post(self, container):
		req = container.req
		resp = container.resp

		container.data["client_app_data"] = []
		container.data["userscope"] = []

		self.__validateHttpPost(container)

		resp.status = HTTP_200  # This is the default status

		# validate usename, password and usertype
		# if valid then generate token and store in redis cache
		token_data = {}
		if(req.body["grant_type"] == "password"):
			token_data = self.__generateTokenFromUserCredentials(container)
		elif(req.body["grant_type"] == "client_credentials"):
			token_data = self.__generateTokenFromClientCredentials(container)
		elif(req.body["grant_type"] == "refresh_token"):
			token_data = self.__generateTokenFromRefreshToken(container)
		elif(req.body["grant_type"] == "authorization_code"):
			appResponce = {}
			appResponce["grant_type"] = self._getError('GRT_AUTH_NOT_IMPL')
			raise appException.clientException_400(appResponce)

		resp.body = json.encode(token_data)

	# function to handle all validation
	def __validateHttpPost(self, container):
		req = container.req
		# token validation
		self.validateHTTPRequest(req, False)

		# data validation
		appResponce = {}
		if("AUTHORIZATION" not in req.headers):
			appResponce["authorization"] = self._getError('NEED_AUTH_CRD')
		else:
			arr = req.headers["AUTHORIZATION"].split(' ')
			authCredentials = base64.b64decode(arr[-1]).decode('utf8').split(':')
			if(len(authCredentials) == 2):
				req.body["client_id"] = authCredentials[0]
				req.body["client_secret"] = authCredentials[1]
			else:
				appResponce["authorization"] = self._getError('INVALID_CLIENT_CRD')

		if("grant_type" not in req.body):
			appResponce["grant_type"] = self._getError('NEED_GTANT_TYPE')
		elif(req.body["grant_type"] != "authorization_code" and req.body["grant_type"] != "password" and req.body["grant_type"] != "client_credentials" and req.body["grant_type"] != "refresh_token"):
			appResponce["grant_type"] = self._getError('INVALID_GTANT_TYPE')
		elif(req.body["grant_type"] == "password"):
			if("username" not in req.body or (not isinstance(req.body["username"], str)) or req.body["username"] == ""):
				appResponce["username"] = self._getError('NEED_USERNAME')
			if("password" not in req.body or (not isinstance(req.body["password"], str)) or req.body["password"] == ""):
				appResponce["password"] = self._getError('NEED_PASSWORD')
		elif(req.body["grant_type"] == "client_credentials"):
			pass
		elif(req.body["grant_type"] == "refresh_token"):
			if("refresh_token" not in req.body or (not isinstance(req.body["refresh_token"], str)) or req.body["refresh_token"] == ""):
				appResponce["refresh_token"] = self._getError('NEED_REFRESH_TOKEN')
		elif(req.body["grant_type"] == "authorization_code"):
			appResponce["grant_type"] = self._getError('AUTH_CODE_NOT_IMPL')


		if appResponce:
			raise appException.clientException_400(appResponce)
		else:

			self.__validateClient(container)

			if(req.body["grant_type"] == "password"):
				self.__validateUser(container)

			if(req.body["grant_type"] == "refresh_token"):
				self.__validateRefreshToken(req.body["refresh_token"])

	def __validateClient(self, container, extraData = None):
		client_id = container.req.body["client_id"]
		client_secret = container.req.body["client_secret"]
		appResponce = {}

		oauth2_client = oauth2ClientModel()
		container.data["client_app_data"] = oauth2_client.get_user_type_scope(client_id, client_secret)
		if(not container.data["client_app_data"]):
			appResponce["authorization"] = self._getError('INVALID_CLIENT_CRD')

		if appResponce:
			raise appException.clientException_400(appResponce)

	def __validateUser(self, container, extraData = None):
		username = container.req.body["username"]
		password = container.req.body["password"]
		appResponce = {}
		if(container.data["client_app_data"][0] == "admin"):
			oauth2_admin_user = oauth2AdminUserModel()
			user_data = oauth2_admin_user.get_user_scope(username, password)
			if(user_data is False):
				appResponce["username"] = self._getError('INALID_USERNAME_PASSWORD')
			else:
				container.data["userscope"] = user_data[0]
				container.data["user_data"] = {
					"id":user_data[1]
				}

		elif(container.data["client_app_data"][0] == "guest"):
			pass
		elif(container.data["client_app_data"][0] == "registered_user"):
			pass

		if appResponce:
			raise appException.clientException_400(appResponce)

	def __validateRefreshToken(self, refresh_token, extraData = None):
		appResponce = {}

		if appResponce:
			raise appException.clientException_400(appResponce)

	def __generateTokenFromClientCredentials(self, container):
		req = container.req
		client_id = req.body["client_id"]
		client_secret = req.body["client_secret"]

		aTokenDb = appCache(self.aTokenDb)

		timestamp = str(datetime.now())

		accessKey  = client_id + "____" + client_secret + "____" + timestamp

		accessToken = self.__generateTokenFromKey(accessKey, aTokenDb)

		scope = container.data["client_app_data"][1]

		# save new token and refresh token in cache
		# aTokenDb.set(accessToken, json.encode(scope), self.__accessTokenExpiry)
		for i in scope:
			aTokenDb.lpush(accessToken, i)
		aTokenDb.expire(accessToken, self.__accessTokenExpiry)

		params = {
			"accessToken" : accessToken,
			"accessTokenExpiry" : self.__accessTokenExpiry,
			# "scope": oauth2ScopeModel().getScopeNamesFromIds(scope),
			"resources": oauth2ScopeModel().getAllowedResourcesFromScopeCodes(scope)
		}

		return params

	def __generateTokenFromUserCredentials(self, container):
		req = container.req
		token_data = self.__generate_new_token(container)
		if "user_data" in container.data:
			self.__setSessionData(accessToken=token_data["accessToken"], data=container.data["user_data"])
		return token_data

	def __generateTokenFromRefreshToken(self, container):
		req = container.req
		rTokenDb = appCache(self.rTokenDb)
		# data = json.decode(rTokenDb.get(req.body["refresh_token"]))
		data = rTokenDb.hgetall(req.body["refresh_token"])
		token_data = self.__generate_new_token(container)
		rTokenDb.delete(req.body["refresh_token"])
		self.__refreshSessionData(old_accessToken=data["accessToken"], accessToken=token_data["accessToken"])
		return token_data

	def __refreshSessionData(self, old_accessToken, accessToken):
		sessionDb = appCache(self.sessionDb)
		if sessionDb.exists(old_accessToken):
			sessionDb.hmset(accessToken, sessionDb.hgetall(old_accessToken))
			sessionDb.expire(accessToken, self.__refreshTokenExpiry)
			sessionDb.delete(old_accessToken)

	def __setSessionData(self, accessToken, data):
		sessionDb = appCache(self.sessionDb)
		sessionDb.hmset(accessToken, data)
		sessionDb.expire(accessToken, self.__refreshTokenExpiry)

	def __deleteSessionData(self, accessToken):
		sessionDb = appCache(self.sessionDb)
		sessionDb.delete(accessToken)

	def __generate_new_token(self, container):
		client_id = container.req.body["client_id"]
		username = container.req.body["username"]

		aTokenDb = appCache(self.aTokenDb)

		rTokenDb = appCache(self.rTokenDb)

		timestamp = str(datetime.now())

		accessKey = client_id + "____" + timestamp + "____" + username

		refreshKey = username + "____" + timestamp + "____" + client_id

		accessToken = self.__generateTokenFromKey(accessKey, aTokenDb)

		refreshToken = self.__generateTokenFromKey(refreshKey, rTokenDb)

		scope = list(set(container.data["client_app_data"][1] + container.data["userscope"]))

		# save new token and refresh token in cache
		# aTokenDb.set(accessToken, json.encode(scope), self.__accessTokenExpiry)
		for i in scope:
			aTokenDb.lpush(accessToken, i)
		aTokenDb.expire(accessToken, self.__accessTokenExpiry)

		# rTokenDb.set(refreshToken, json.encode({"client_id":client_id,"username":username}), self.__refreshTokenExpiry)
		rTokenDb.hmset(refreshToken, {"client_id":client_id,"username":username,"accessToken":accessToken})
		rTokenDb.expire(refreshToken, self.__refreshTokenExpiry)

		params = {
			"accessToken" : accessToken,
			"refreshToken" : refreshToken,
			"accessTokenExpiry" : self.__accessTokenExpiry,
			"refreshTokenExpiry" : self.__refreshTokenExpiry,
			# "scope": oauth2ScopeModel().getScopeNamesFromIds(scope),
			"resources": oauth2ScopeModel().getAllowedResourcesFromScopeCodes(scope)
		}

		return params

	def __generateTokenFromKey(self, key, dbName):
		token = blake2b(key.encode('utf-8')).hexdigest()
		# generate new if key exists in dbName
		while dbName.exists(key):
			token = self.__generateTokenFromKey(key, dbName)
		return token

	def delete(self, container):
		req = container.req
		resp = container.resp

		self.__validateHttpDelete(req)

		resp.status = HTTP_200  # This is the default status

		token_data = {}

		accessToken = None

		if("accessToken" in req.body):
			accessToken = req.body["accessToken"]
			appCache(self.aTokenDb).delete(req.body["accessToken"])
			token_data["accessToken"] = True

		if("refreshToken" in req.body):
			rTokenDb = appCache(self.rTokenDb)
			data = rTokenDb.hgetall(req.body["refreshToken"])
			accessToken = data["accessToken"]
			rTokenDb.delete(req.body["refreshToken"])
			token_data["refreshToken"] = True

		if accessToken:
			self.__deleteSessionData(accessToken)

		resp.body = json.encode(token_data)


	def __validateHttpDelete(self, req):
		# token validation
		self.validateHTTPRequest(req, False)

		# data validation
		appResponce = {}
		if("accessToken" not in req.body and "refreshToken" not in req.body):
			appResponce["accessToken"] = self._getError('NEED_TOKEN')

		if appResponce:
			raise appException.clientException_400(appResponce)