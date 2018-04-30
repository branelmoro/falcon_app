# always extend your controller from base_controller
# always give controller class name same as filename
from falcon import HTTP_200
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

	def post(self, container):
		req = container.req
		resp = container.resp
		"""Handles POST requests"""
		self.__validateHttpPost(req)

		# this is valid request
		appResponce = {}

		data = self._getFilteredRequestData(req, ["code", "resource_path", "resource_info"])

		oauth2_resource = oauth2ResourceModel()
		appResponce["result"] = oauth2_resource.createNewResource(data)
		resp.status = HTTP_200  # This is the default status
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
			appResponce["resource_path"] = self._getError(1)
			# appResponce["resource_path"] = "Resource path already exists in database!"

		if oauth2_resource.ifResourceCodeAlreadyExists(req.body["code"]):
			appResponce["code"] = "Resource code already exists in database!"

		if appResponce:
			raise appException.clientException_400(appResponce)

	def __commonValidation(self, req):

		is_put = (req.method == "PUT")

		appResponce = {}

		if is_put and ("resource_id" not in req.body or (not isinstance(req.body["resource_id"], int))):
			# appResponce["resource_id"] = "Please provide a valid resource id"
			appResponce["resource_id"] = self._getError(2)

		if is_put and ("code" not in req.body and "resource_path" not in req.body and "resource_info" not in req.body):
			# appResponce["resource_id"] = "Please provide some information to update"
			appResponce["resource_id"] = self._getError(3)

		if(
			is_put
			and "resource_path" in req.body
			and (req.body["resource_path"] == "" or (not isinstance(req.body["resource_path"], str)) or req.body["resource_path"].find("/") != 0)
		) or (
			not is_put
			and ("resource_path" not in req.body or req.body["resource_path"] == "" or (not isinstance(req.body["resource_path"], str)) or req.body["resource_path"].find("/") != 0)
		):
			# appResponce["resource_path"] = "Please provide valid resource path"
			appResponce["resource_path"] = self._getError(4)

		if(
			is_put
			and "resource_info" in req.body
			and req.body["resource_info"] == ""
		) or (
			not is_put
			and ("resource_info" not in req.body or req.body["resource_info"] == "")
		):
			# appResponce["resource_info"] = "Please provide some resource information"
			appResponce["resource_info"] = self._getError(4)

		if(
			is_put
			and "code" in req.body
			and req.body["code"] == ""
		) or (
			not is_put
			and ("code" not in req.body or req.body["code"] == "")
		):
			appResponce["code"] = "Please provide resource code"

		if appResponce:
			raise appException.clientException_400(appResponce)

	def put(self, container):
		req = container.req
		resp = container.resp
		"""Handles POST requests"""
		self.__validateHttpPut(req)

		# this is valid request
		appResponce = {}

		data = self._getFilteredRequestData(req, ["code", "resource_path", "resource_info", "resource_id"])

		oauth2_resource = oauth2ResourceModel()
		appResponce["result"] = oauth2_resource.updateResource(data)
		resp.status = HTTP_200  # This is the default status
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
			# appResponce["resource_id"] = "Please provide a valid resource id"
			appResponce["resource_id"] = self._getError(7)
		elif not oauth2_resource.ifResourceEditable(req.body["resource_id"]):
			# appResponce["resource_id"] = "This resource is not editable"
			appResponce["resource_id"] = self._getError(6)
		else:
			if "resource_path" in req.body and oauth2_resource.ifResourcePathAlreadyExists(req.body["resource_path"], req.body["resource_id"]):
				# appResponce["resource_path"] = "Resource path already exists in another record"
				appResponce["resource_path"] = self._getError(1)
			if "code" in req.body and oauth2_resource.ifResourceCodeAlreadyExists(req.body["code"], req.body["resource_id"]):
				appResponce["code"] = "Resource code already exists in another record"

		if appResponce:
			raise appException.clientException_400(appResponce)

	def delete(self, container):
		req = container.req
		resp = container.resp
		"""Handles POST requests"""
		self.__validateHttpDelete(req)

		# this is valid request
		appResponce = {}

		data = self._getFilteredRequestData(req, ["resource_id"])

		oauth2_resource = oauth2ResourceModel()
		appResponce["result"] = oauth2_resource.deleteResource(data["resource_id"])
		resp.status = HTTP_200  # This is the default status
		resp.body = json.encode(appResponce)

	def __validateHttpDelete(self, req):
		# token validation
		self.validateHTTPRequest(req)

		appResponce = {}

		if("resource_id" not in req.body or (not isinstance(req.body["resource_id"], int))):
			# appResponce["resource_id"] = "Please provide a valid resource id"
			appResponce["resource_id"] = self._getError(2)

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			# database level validation goes here
			oauth2_resource = oauth2ResourceModel()

			if not oauth2_resource.ifResourceIdExists(req.body["resource_id"]):
				# appResponce["resource_id"] = "Please provide a valid resource id"
				appResponce["resource_id"] = self._getError(7)
			elif not oauth2_resource.ifResourceEditable(req.body["resource_id"]):
				# appResponce["resource_id"] = "Resource is not editable"
				appResponce["resource_id"] = self._getError(6)

			if appResponce:
				raise appException.clientException_400(appResponce)
