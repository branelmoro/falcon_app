import pycurl,base64
from .resource_api import BACKEND_API

from ...config import CLIENT_APP_CREDENTIALS, BACKEND_API_URL

class AUTH(BACKEND_API):

	@classmethod
	def __authorize(cls, data):
		header = {
			# "Content-Type":"application/json",
			"Authorization":"Basic " + base64.b64encode((CLIENT_APP_CREDENTIALS[0]+":"+CLIENT_APP_CREDENTIALS[1]).encode('utf-8')).decode('utf-8')
		}
		return cls.post(url=BACKEND_API_URL+"/token/", data=data, header=header)

	@classmethod
	def grant_type_authorization_code(cls, data):
		# not needed for our own apps
		pass

	@classmethod
	def grant_type_password(cls, data={}):
		data["grant_type"] = "password"
		return cls.__authorize(data)

	@classmethod
	def grant_type_client_credentials(cls, data={}):
		data["grant_type"] = "client_credentials"
		return cls.__authorize(data)

	@classmethod
	def grant_type_refresh_token(cls, refresh_token):
		data = {
			"refresh_token":refresh_token,
			"grant_type":"refresh_token"
		}
		# data["grant_type"] = "refresh_token"
		return cls.__authorize(data)

	@classmethod
	def destroyTokens(cls, data={}):
		return cls.delete(url=BACKEND_API_URL+"/token/", data=data)