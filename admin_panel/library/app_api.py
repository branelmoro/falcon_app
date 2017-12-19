import hashlib
from . import APPCACHE
from ..resources.backend_api import BACKEND_API, Auth

from .. import exception as appException

class APP_API(object):

	__session = None

	__client_session = {
		"token_api_call":False
	}

	def __init__(self, session = None):
		self.__session = session

	def get(self, path, header={}):
		return self.__getDataFromAPI(method="GET", path=path, header=header)

	def post(self, path, data = None, header={}):
		return self.__getDataFromAPI(method="POST", path=path, data=data, header=header)

	def put(self, path, data = None, header={}):
		return self.__getDataFromAPI(method="PUT", path=path, data=data, header=header)

	def delete(self, path, data, header={}):
		return self.__getDataFromAPI(method="DELETE", path=path, data=data, header=header)

	def __getDataFromAPI(self, method, path, data=None, header={}):
		header["access-token"] = self.__getToken()
		if method == "GET":
			response = BACKEND_API.get(path=path, header=header)
		elif method == "POST":
			response = BACKEND_API.post(path=path, data=data, header=header)
		elif method == "PUT":
			response = BACKEND_API.put(path=path, data=data, header=header)
		elif method == "DELETE":
			response = BACKEND_API.delete(path=path, data=data, header=header)

		if response["httpcode"] == 401:
			# unauthorised token found, regenerate token
			self.__generateToken()
			return self.__getDataFromAPI(method=method, path=path, data=data, header=header)
		elif response["httpcode"] == 404:
			# throw error, api does not exists
			pass
		else:
			if int(response["httpcode"]/100) == 5:
				# throw api server error
				pass
			else:
				return response

	def __refreshUserToken(self):
		refresh_token = self.__session.get("refreshToken")
		arrResponce = Auth.grant_type_refresh_token()
		if arrResponce["httpcode"] == 400:
			self.__session.destory()
		else:
			self.__session.refresh(arrResponce["response"])

	@classmethod
	def __generateClientToken(cls):
		bln_wait = cls.__client_session["token_api_call"]
		while cls.__client_session["token_api_call"]:
			time.sleep(0.1)
		cls.__client_session["token_api_call"] = True
		if bln_wait:
			return

		arrResponce = Auth.grant_type_client_credentials()
		if arrResponce["httpcode"] == 400:
			raise appException.serverException_500({"app":"APP authorization failed"})
		cls.__client_session = arrResponce["response"]

		cls.__client_session["token_api_call"] = False

	def __generateToken(self):
		if self.__session is not None and self.__session.exists():
			self.__refreshUserToken()
		else:
			# client doesn't have right throw exception
			self.__generateClientToken()

	@classmethod
	def __getClientToken(cls):
		if "accessToken" not in cls.__client_session:
			cls.__generateClientToken()
		return cls.__client_session["accessToken"]

	def __getToken(self):
		if self.__session is not None and self.__session.exists():
			return self.__session.get("accessToken")
		else:
			return self.__getClientToken()