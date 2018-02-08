# always extend your controller from base_controller
# always give controller class name same as filename
from falcon import HTTP_200
from ..base_controller import baseController

import datetime


server_start_time = datetime.datetime.now()

api_info = {
	"started_at" : str(server_start_time),
	"version" : "0.0.1"
}

# import all required models here
# from app.models.sampleModel import sampleModel

class index(baseController):

	def __init__(self):
		self.__path = "/"

	def getPath(self):
		return self.__path

	"""This is sample controller"""
	def get(self, container):
		req = container.req
		resp = container.resp
		"""Handles GET requests"""
		resp.status = HTTP_200  # This is the default status

		params = api_info

		current_time = datetime.datetime.now()
		params["current_server_time"] = str(current_time)
		params["nodeName"] = req.env["uwsgi.node"].decode("utf-8")
		params["uwsgi_version"] = req.env["uwsgi.version"].decode("utf-8")
		# params["uwsgi_core"] = req.env["uwsgi.core"]

		params["running_from"] = str(current_time - server_start_time)

		app_api = self.getAPI(container)

		assync_call = [{
				"api_detail":{
					"method":"GET",
					"url":self.getAPIURL("/"),
				},
				"callback":self.callback1
			},{
				"api_detail":{
					"method":"GET",
					"url":self.getAPIURL("/"),
				},
				"callback":self.callback2
			},{
				"api_detail":{
					"method":"GET",
					"url":self.getAPIURL("/"),
				},
				"callback":self.callback2
			},{
				"api_detail":{
					"method":"GET",
					"url":self.getAPIURL("/"),
				},
				"callback":self.callback2
			}
		]

		app_api.executeAsync(assync_call)

		resp.body = self._render(view="test.sample_view")


	def callback1(self, httpcode, response, container):
		print("callback1")
		print(response)

	def callback2(self, httpcode, response, container):
		print("callback2")
		print(response)