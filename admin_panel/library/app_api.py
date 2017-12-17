import hashlib
from . import APPCACHE
from ..resources.backend_api import BACKEND_API, Auth

from ..config import CLIENT_APP_CREDENTIALS

class APP_API(object):

	__session = None

	def __init__(self, session = None):
		self.__session = session

	def get(self, path, header={}):
		while True:
			header["access-token"] = self.__getToken()
			response = BACKEND_API.get(method="GET", path=path, header=header)
			if response["httpcode"] == 401:
				# unauthorised token found, regenerate token
				self.__generateToken()

	def post(self, path, data = None, header={}):
		return BACKEND_API.post(method="POST", path=path, data=data, header=header)

	def put(self, path, data = None, header={}):
		return BACKEND_API.put(method="PUT", path=path, data=data, header=header)

	def delete(self, path, data, header={}):
		return BACKEND_API.delete(method="DELETE", path=path, data=data, header=header)

	def __refreshUserToken(self):
		refresh_token = self.__session.get("refreshToken")
		arrResponce = Auth.grant_type_refresh_token()
		# if token expired then:
		# 	destory session
		pass

	def __generateClientToken(self):
		client_session_id = hashlib.md5(json.encode(CLIENT_APP_CREDENTIALS))
		arrResponce = Auth.grant_type_client_credentials()
		if arrResponce["httpcode"] == 400:
			# throw new \Exception("Clientapp authorization failed");
			pass
		client_data = arrResponce["response"]
		APPCACHE.hmset(client_session_id,client_data)

	def __generateToken(self):
		if self.__session is not None and self.__session.exists():
			self.__refreshUserToken()
		else:
			self.__generateClientToken()

	def __getClientToken(self):
		client_session_id = hashlib.md5(json.encode(CLIENT_APP_CREDENTIALS))
		client_data = APPCACHE.hgetall(client_session_id)
		if not client_data:
			self.__generateClientToken()
			client_data = APPCACHE.hgetall(client_session_id)
		return client_data["accessToken"]

	def __getToken(self):
		if self.__session is not None and self.__session.exists():
			return self.__session.get("accessToken")
		else:
			return self.__getClientToken()