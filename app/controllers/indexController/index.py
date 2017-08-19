# always extend your controller from base_controller
# always give controller class name same as filename
from ... import falcon
from ..base_controller import baseController

from ...library import json

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

	def demo(self):
		print("workng")
		sampleModel().test()

	"""This is sample controller"""
	def on_get(self, req, resp):
		"""Handles GET requests"""
		resp.status = falcon.HTTP_200  # This is the default status

		params = api_info

		current_time = datetime.datetime.now()
		params["current_server_time"] = str(current_time)
		params["nodeName"] = req.env["uwsgi.node"].decode("utf-8")
		params["uwsgi_version"] = req.env["uwsgi.version"].decode("utf-8")
		# params["uwsgi_core"] = req.env["uwsgi.core"]

		params["running_from"] = str(current_time - server_start_time)

		resp.body = json.encode(params)
