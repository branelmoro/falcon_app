# always extend your controller from base_controller
# always give controller class name same as filename
from ... import falcon
from ..controllers.base_controller import baseController
from ..controllers.base_controller import appException

from ...library import json

# import all required models here
from ...models.oauth2Model import oauth2ResourceModel

class resource(baseController):

	def __init__(self):
		# resource_id = 1
		super.__init__(self,1)
		# self._path = "/resource/"

	def getPath(self):
		return self._path

	def post(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpPost(req)

		# this is valid request
		appResponce = {}

		data = {
			"resource_path": req.body["resource_path"],
			"resource_info" : req.body["resource_info"]
		}
		search_skill_model = oauth2ResourceModel()
		appResponce["result"] = search_skill_model.createNewResource(data)
		resp.status = falcon.HTTP_200  # This is the default status
		resp.body = json.encode(appResponce)

	# function to handle all validation
	def __validateHttpPost(self, req):
		# token validation
		self.validateHTTPRequest(req)

		# data validation
		appResponce = {}

		if("resource_path" not in req.body or req.body["resource_path"] == "" or (not isinstance(req.body["resource_path"], str)) or req.body["resource_path"].find("/") == 0):
			appResponce["resource_path"] = "Please provide valid resource path"
		if("resource_info" not in req.body or req.body["resource_info"] == ""):
			appResponce["resource_info"] = "Please provide some resource information"

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			# database level validation goes here
			search_skill_model = oauth2ResourceModel()

			if search_skill_model.ifResourcePathAlreadyExists(req.body["resource_path"]):
				appResponce["resource_path"] = "Resource path already exists"

			if appResponce:
				raise appException.clientException_400(appResponce)


	def put(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpPut(req)

		# this is valid request
		appResponce = {}

		data = {
			"resource_path": req.body["resource_path"],
			"resource_info" : req.body["resource_info"],
			"resource_id" : req.body["resource_id"]
		}
		search_skill_model = oauth2ResourceModel()
		appResponce["result"] = search_skill_model.updateResource(data)
		resp.status = falcon.HTTP_200  # This is the default status
		resp.body = json.encode(appResponce)

	# function to handle all validation
	def __validateHttpPut(self, req):
		# token validation
		self.validateHTTPRequest(req)

		# data validation
		appResponce = {}

		if("resource_path" not in req.body or req.body["resource_path"] == "" or (not isinstance(req.body["resource_path"], str)) or req.body["resource_path"].find("/") == 0):
			appResponce["resource_path"] = "Please provide valid resource path"
		if("resource_info" not in req.body or req.body["resource_info"] == ""):
			appResponce["resource_info"] = "Please provide some resource information"
		if("resource_id" not in req.body or (not isinstance(req.body["resource_id"], int))):
			appResponce["resource_id"] = "Please provide resource id"

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			# database level validation goes here
			search_skill_model = oauth2ResourceModel()

			if not search_skill_model.ifResourceIdAlreadyExists(appResponce["resource_id"]):
				appResponce["resource_id"] = "Please provide valid resource id"
			elif search_skill_model.ifResourcePathAlreadyExists(req.body["resource_path"], appResponce["resource_id"]):
				appResponce["resource_path"] = "Resource path already exists in another record"

			if appResponce:
				raise appException.clientException_400(appResponce)


	def delete(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpDelete(req)

		# this is valid request
		appResponce = {}

		data = {
			"resource_id" : req.body["resource_id"]
		}
		search_skill_model = oauth2ResourceModel()
		appResponce["result"] = search_skill_model.deleteResource(data)
		resp.status = falcon.HTTP_200  # This is the default status
		resp.body = json.encode(appResponce)

	def __validateHttpDelete(req):
		# token validation
		self.validateHTTPRequest(req)

		appResponce = {}

		if("resource_id" not in req.body or (not isinstance(req.body["resource_id"], int))):
			appResponce["resource_id"] = "Please provide resource id"

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			# database level validation goes here
			search_skill_model = oauth2ResourceModel()

			if not search_skill_model.ifResourceIdAlreadyExists(appResponce["resource_id"]):
				appResponce["resource_id"] = "Please provide valid resource id"

			if appResponce:
				raise appException.clientException_400(appResponce)
