# always extend your controller from base_controller
# always give controller class name same as filename
from ... import falcon
from ..base_controller import baseController
from ..base_controller import appException

# from app import appCache

from ...resources.redis import redis as appCache

from datetime import datetime

from ...library import json

import hashlib

import base64

# import all required models here
from ...models.oauth2Model import oauth2ClientModel
from ...models.oauth2Model import oauth2ScopeModel
from ...models.oauth2Model import oauth2AdminUserModel
# from ...models.sampleModel import sampleModel

class index(baseController):

	def __init__(self):
		self.__path = "/token"
		self.aTokenDb = appCache("access_tokenDb")
		self.rTokenDb = appCache("refresh_tokenDb")

		self.__accessTokenExpiry = 900
		self.__refreshTokenExpiry = 3600*7*24

		self.client_app_data = []
		self.userscope = []

	def getPath(self):
		return self.__path

	def post(self, req, resp):

		self.__validateHttpPost(req)

		resp.status = falcon.HTTP_200  # This is the default status

		# validate usename, password and usertype
		# if valid then generate token and store in redis cache
		token_data = {}
		if(req.body["grant_type"] == "password"):
			token_data = self.__generateTokenFromUserCredentials(req);
		elif(req.body["grant_type"] == "client_credentials"):
			token_data = self.__generateTokenFromClientCredentials(req);
		elif(req.body["grant_type"] == "refresh_token"):
			token_data = self.__generateTokenFromRefreshToken(req);
		elif(req.body["grant_type"] == "authorization_code"):
			appResponce = {}
			appResponce["grant_type"] = self._getError(43)
			raise appException.clientException_400(appResponce)

		resp.body = json.encode(token_data)

	# function to handle all validation
	def __validateHttpPost(self, req):
		# token validation
		self.validateHTTPRequest(req, False)

		# data validation
		appResponce = {}
		if("AUTHORIZATION" not in req.headers):
			appResponce["authorization"] = self._getError(44)
		else:
			arr = req.headers["AUTHORIZATION"].split(' ')
			authCredentials = base64.b64decode(arr[-1]).decode('utf8').split(':')
			if(len(authCredentials) == 2):
				req.body["client_id"] = authCredentials[0]
				req.body["client_secret"] = authCredentials[1]
			else:
				appResponce["authorization"] = self._getError(45)

		if("grant_type" not in req.body):
			appResponce["grant_type"] = self._getError(46)
		elif(req.body["grant_type"] != "authorization_code" and req.body["grant_type"] != "password" and req.body["grant_type"] != "client_credentials" and req.body["grant_type"] != "refresh_token"):
			appResponce["grant_type"] = self._getError(47)
		elif(req.body["grant_type"] == "password"):
			if("username" not in req.body or (not isinstance(req.body["username"], str)) or req.body["username"] == ""):
				appResponce["username"] = self._getError(48)
			if("password" not in req.body or (not isinstance(req.body["password"], str)) or req.body["password"] == ""):
				appResponce["password"] = self._getError(49)
		elif(req.body["grant_type"] == "client_credentials"):
			pass
		elif(req.body["grant_type"] == "refresh_token"):
			if("refresh_token" not in req.body or (not isinstance(req.body["refresh_token"], str)) or req.body["refresh_token"] == ""):
				appResponce["refresh_token"] = self._getError(50)
		elif(req.body["grant_type"] == "authorization_code"):
			appResponce["grant_type"] = self._getError(51)


		if appResponce:
			raise appException.clientException_400(appResponce)
		else:

			self.__validateClient(req.body["client_id"], req.body["client_secret"])

			if(req.body["grant_type"] == "password"):
				self.__validateUser(req.body["username"], req.body["password"])

			if(req.body["grant_type"] == "refresh_token"):
				self.__validateRefreshToken(req.body["refresh_token"])

	def __validateClient(self, client_id, client_secret, extraData = None):
		appResponce = {}

		oauth2_client = oauth2ClientModel()
		self.client_app_data = oauth2_client.get_user_type_scope(client_id, client_secret)
		if(not self.client_app_data):
			appResponce["authorization"] = self._getError(45)

		if appResponce:
			raise appException.clientException_400(appResponce)

	def __validateUser(self, username, password, extraData = None):
		appResponce = {}
		if(self.client_app_data[0] == "admin"):
			oauth2_admin_user = oauth2AdminUserModel()
			self.userscope = oauth2_admin_user.get_user_scope(username, password)
			if(self.userscope is False):
				appResponce["username"] = self._getError(52)
		elif(self.client_app_data[0] == "guest"):
			pass
		elif(self.client_app_data[0] == "registered_user"):
			pass

		if appResponce:
			raise appException.clientException_400(appResponce)

	def __validateRefreshToken(self, refresh_token, extraData = None):
		appResponce = {}

		if appResponce:
			raise appException.clientException_400(appResponce)

	def __generateTokenFromClientCredentials(self, req):
		client_id = req.body["client_id"]
		client_secret = req.body["client_secret"]

		timestamp = str(datetime.now())

		accessKey  = client_id + "____" + client_secret + "____" + timestamp

		accessToken = self.__generateTokenFromKey(accessKey, self.aTokenDb)

		scope = self.client_app_data[1]

		# save new token and refresh token in cache
		# self.aTokenDb.set(accessToken, json.encode(scope), self.__accessTokenExpiry)
		self.aTokenDb.sadd(accessToken, scope)
		self.aTokenDb.expire(accessToken, self.__accessTokenExpiry)

		params = {
			"accessToken" : accessToken,
			"accessTokenExpiry" : self.__accessTokenExpiry,
			"scope": oauth2ScopeModel().getScopeNamesFromIds(scope)
		}

		return params

	def __generateTokenFromUserCredentials(self, req):
		return self.__generate_new_token(req.body["client_id"], req.body["username"])

	def __generateTokenFromRefreshToken(self, req):
		# data = json.decode(self.rTokenDb.get(req.body["refresh_token"]))
		data = self.rTokenDb.hgetall(req.body["refresh_token"])
		token_data = self.__generate_new_token(data["client_id"], data["username"])
		self.rTokenDb.delete(req.body["refresh_token"])
		return token_data;

	def __generate_new_token(self, client_id, username):

		timestamp = str(datetime.now())

		accessKey = client_id + "____" + timestamp + "____" + username

		refreshKey = username + "____" + timestamp + "____" + client_id

		accessToken = self.__generateTokenFromKey(accessKey, self.aTokenDb)

		refreshToken = self.__generateTokenFromKey(refreshKey, self.rTokenDb)

		scope = list(set(self.client_app_data[1] + self.userscope))

		# save new token and refresh token in cache
		# self.aTokenDb.set(accessToken, json.encode(scope), self.__accessTokenExpiry)
		self.aTokenDb.sadd(accessToken, scope)
		self.aTokenDb.expire(accessToken, self.__accessTokenExpiry)

		# self.rTokenDb.set(refreshToken, json.encode({"client_id":client_id,"username":username}), self.__refreshTokenExpiry)
		self.rTokenDb.hmset(refreshToken, {"client_id":client_id,"username":username})
		self.rTokenDb.expire(refreshToken, self.__refreshTokenExpiry)

		params = {
			"accessToken" : accessToken,
			"refreshToken" : refreshToken,
			"accessTokenExpiry" : self.__accessTokenExpiry,
			"refreshTokenExpiry" : self.__refreshTokenExpiry,
			"scope": oauth2ScopeModel().getScopeNamesFromIds(scope)
		}

		return params

	def __generateTokenFromKey(self, key, dbName):
		token = hashlib.blake2b(key.encode('utf-8')).hexdigest();
		# generate new if key exists in dbName
		while dbName.exists(key):
			token = self.__generateTokenFromKey(key, dbName)
		return token



	def delete(self, req, resp):

		self.__validateHttpDelete(req)

		resp.status = falcon.HTTP_200  # This is the default status

		token_data = {}

		if("accessToken" in req.body):
			self.aTokenDb.delete(req.body["accessToken"])
			token_data["accessToken"] = True

		if("refreshToken" not in req.body):
			self.rTokenDb.delete(req.body["refreshToken"])
			token_data["refreshToken"] = True

		resp.body = json.encode(token_data)


	def __validateHttpDelete(self, req):
		# token validation
		self.validateHTTPRequest(req, False)

		# data validation
		appResponce = {}
		if("accessToken" not in req.body and "refreshToken" not in req.body):
			appResponce["accessToken"] = self._getError(53)

		if appResponce:
			raise appException.clientException_400(appResponce)