import pycurl,base64
from .resource_api import BACKEND_API

from ...config import CLIENT_APP_CREDENTIALS

class AUTH(BACKEND_API):

	@classmethod
	def __authorize(cls, data):
		headers = {
			# "Content-Type":"application/json",
			"Authorization":"Basic" + base64.b64encode((CLIENT_APP_CREDENTIALS[0]+":"+CLIENT_APP_CREDENTIALS[1]).encode('utf-8')).decode('utf-8')
		}
		return cls.post(url=BACKEND_API+"/token/", data=data, header=header)

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
	def grant_type_refresh_token(cls, data={}):
		data = {
			"refresh_token":"asdfsdfsdfsdfsdfsdfsdfsdfsdf",
			"grant_type":"refresh_token"
		}
		return cls.__authorize(data)

	@classmethod
	def destroyTokens(data):
		return cls.delete(url=BACKEND_API+"/token/", data=data)