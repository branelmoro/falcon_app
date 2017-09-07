# always extend your controller from base_controller
# always give controller class name same as filename
from ... import falcon
from ..base_controller import baseController
from ..base_controller import appException

from ...library import json

# import all required models here
from ...models.oauth2Model import oauth2ResourceModel

class resource(baseController):

	def __init__(self):
		# resource_id = 1
		super().__init__(1)
		# self._path = "/resource/"

	def getPath(self):
		return self._path

	def post(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpPost(req)

		# this is valid request
		appResponce = {}

		data = self._getFilteredRequestData(req, ["resource_path", "resource_info"])

		oauth2_resource = oauth2ResourceModel()
		appResponce["result"] = oauth2_resource.createNewResource(data)
		resp.status = falcon.HTTP_200  # This is the default status
		resp.body = json.encode(appResponce)

	# function to handle all validation
	def __validateHttpPost(self, req):
		# token validation
		self.validateHTTPRequest(req)

		self.__commonValidation(req)

		# data validation
		appResponce = {}

		# database level validation goes here
		oauth2_resource = oauth2ResourceModel()

		if oauth2_resource.ifResourcePathAlreadyExists(req.body["resource_path"]):
			appResponce["resource_path"] = "Resource path already exists"

		if appResponce:
			raise appException.clientException_400(appResponce)

	def __commonValidation(self, req):

		is_put = (req.method == "PUT")

		appResponce = {}

		if is_put and ("resource_id" not in req.body or (not isinstance(req.body["resource_id"], int))):
			appResponce["resource_id"] = "Please provide resource id"

		if is_put and ("resource_path" not in req.body and "resource_info" not in req.body):
			appResponce["resource_id"] = "Please provide information to update"

		if(
			is_put
			and "resource_path" in req.body
			and (req.body["resource_path"] == "" or (not isinstance(req.body["resource_path"], str)) or req.body["resource_path"].find("/") != 0)
		) or (
			not is_put
			and ("resource_path" not in req.body or req.body["resource_path"] == "" or (not isinstance(req.body["resource_path"], str)) or req.body["resource_path"].find("/") != 0)
		):
			appResponce["resource_path"] = "Please provide valid resource path"

		if(
			is_put
			and "resource_info" in req.body
			and req.body["resource_info"] == ""
		) or (
			not is_put
			and ("resource_info" not in req.body or req.body["resource_info"] == "")
		):
			appResponce["resource_info"] = "Please provide some resource information"

		if appResponce:
			raise appException.clientException_400(appResponce)


	def put(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpPut(req)

		# this is valid request
		appResponce = {}

		data = self._getFilteredRequestData(req, ["resource_path", "resource_info", "resource_id"])

		oauth2_resource = oauth2ResourceModel()
		appResponce["result"] = oauth2_resource.updateResource(data)
		resp.status = falcon.HTTP_200  # This is the default status
		resp.body = json.encode(appResponce)

	# function to handle all validation
	def __validateHttpPut(self, req):
		# token validation
		self.validateHTTPRequest(req)

		self.__commonValidation(req)

		# data validation
		appResponce = {}

		# database level validation goes here
		oauth2_resource = oauth2ResourceModel()

		if not oauth2_resource.ifResourceIdExists(req.body["resource_id"]):
			appResponce["resource_id"] = "Please provide valid resource id"
		elif not oauth2_resource.ifResourceEditable(req.body["resource_id"]):
			appResponce["resource_id"] = "Resource is not editable"
		elif "resource_path" in req.body and oauth2_resource.ifResourcePathAlreadyExists(req.body["resource_path"], req.body["resource_id"]):
			appResponce["resource_path"] = "Resource path already exists in another record"

		if appResponce:
			raise appException.clientException_400(appResponce)


	def delete(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpDelete(req)

		# this is valid request
		appResponce = {}

		data = self._getFilteredRequestData(req, ["resource_id"])

		oauth2_resource = oauth2ResourceModel()
		appResponce["result"] = oauth2_resource.deleteResource(data)
		resp.status = falcon.HTTP_200  # This is the default status
		resp.body = json.encode(appResponce)

	def __validateHttpDelete(self, req):
		# token validation
		self.validateHTTPRequest(req)

		appResponce = {}

		if("resource_id" not in req.body or (not isinstance(req.body["resource_id"], int))):
			appResponce["resource_id"] = "Please provide resource id"

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			# database level validation goes here
			oauth2_resource = oauth2ResourceModel()

			if not oauth2_resource.ifResourceIdExists(req.body["resource_id"]):
				appResponce["resource_id"] = "Please provide valid resource id"
			elif not oauth2_resource.ifResourceEditable(req.body["resource_id"]):
				appResponce["resource_id"] = "Resource is not editable"

			if appResponce:
				raise appException.clientException_400(appResponce)
