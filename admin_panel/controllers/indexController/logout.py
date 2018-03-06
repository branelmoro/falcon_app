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

class logout(baseController):

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

			auth_data = AUTH.destroyTokens(data={
				"accessToken":container.getSession().get("accessToken"),
				"refreshToken":container.getSession().get("refreshToken")
			})

			print(auth_data)

			container.getSession().destroy()

		raise HTTPFound("/")