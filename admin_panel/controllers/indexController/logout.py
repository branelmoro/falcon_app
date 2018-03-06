# always extend your controller from base_controller
# always give controller class name same as filename
from falcon import HTTP_200, HTTP_302, HTTPFound
from ..base_controller import baseController

import datetime
from ...resources.backend_api import AUTH
from ...library import json


server_start_time = datetime.datetime.now()

api_info = {
	"started_at" : str(server_start_time),
	"version" : "0.0.1"
}

# import all required models here
# from app.models.sampleModel import sampleModel

class index(baseController):

	def __init__(self):
		self.__path = "/logout"

	def getPath(self):
		return self.__path

	def get(self, container):
		req = container.req
		resp = container.resp

		if container.getSession().isUserLoggedIn():
			# collect data for home page
			resp.body = self._render(view="home")
		else:
			resp.body = self._render(view="login")

	def post(self, container):
		req = container.req
		resp = container.resp
		raw_json = req.bounded_stream.read()

		print(raw_json)

		auth_data = AUTH.grant_type_password(data={
			"username":"branelm",
			"password":"123456"
		})
		print(auth_data)


		if "httpcode" in auth_data and auth_data["httpcode"] == 200:
			response = json.decode(auth_data["response"])
			container.getSession().start(expiry = response["refreshTokenExpiry"], data=response)
			# resp.body = self._render(view="login")
			# resp.status = HTTP_302
			raise HTTPFound("/")
		else:
			resp.body = self._render(view="login")