# always extend your controller from base_controller
# always give controller class name same as filename
from falcon import HTTP_200, HTTP_302, HTTPFound
from ..base_controller import baseController

import datetime
from ...resources.backend_api import AUTH
from ...library import json
from html import unescape


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

	def get(self, container):
		req = container.req
		resp = container.resp
		print(req.params)
		# print(unescape(req.params["sampletext"]))

		if container.getSession().isUserLoggedIn():
			# collect data for home page
			resp.body = self._render(view="home")
		else:
			resp.body = self._render(view="login")

	def post(self, container):
		req = container.req
		resp = container.resp
		print(req.params)
		body_param = self._getBodyParams(container)
		print(body_param)
		print(body_param["sampletext456465"])
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

	"""This is sample controller"""
	def get_sample(self, container):
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
				"method":"GET",
				"url":self.getAPIURL("/"),
				"callback":self.callback1,
				"next":[{
						"method":"GET",
						"url":self.getAPIURL("/"),
						"callback":self.callback1
					},{
						"method":"GET",
						"url":self.getAPIURL("/"),
						"callback":self.callback2
					}
				]
			},{
				"method":"GET",
				"url":self.getAPIURL("/"),
				"callback":self.callback2,
				"next":{
					"method":"GET",
					"url":self.getAPIURL("/"),
					"callback":self.callback1
				}
			},{
				"method":"GET",
				"url":self.getAPIURL("/"),
				"callback":self.callback1,
				"next":{
					"async":[{
							"method":"GET",
							"url":self.getAPIURL("/"),
							"callback":self.callback1
						},{
							"method":"GET",
							"url":self.getAPIURL("/"),
							"callback":self.callback2
						}
					],
					"next":{
						"method":"GET",
						"url":self.getAPIURL("/"),
						"callback":self.callback1
					}
				}
			},{
				"method":"GET",
				"url":self.getAPIURL("/"),
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