# always extend your controller from base_controller
# always give controller class name same as filename
from ... import falcon
from ..controllers.base_controller import baseController
from ..controllers.base_controller import appException

from ...library import json

# import all required models here
from ...models.oauth2Model import oauth2ScopeModel

class accessScope(baseController):

	def __init__(self):
		self.__path = "/access-scope/"

	def getPath(self):
		return self.__path

	def post(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpPost(req)

		# this is valid request
		appResponce = {}

		resp.status = falcon.HTTP_200  # This is the default status

		scope_model = oauth2ScopeModel()

		scope_detail = {
			"scope_name" : req.body["scope_name"],
			"scope_info" : req.body["scope_info"],
			"allowed_resources" : req.body["allowed_resources"]
		}app.models

		appResponce["result"] = scope_model.createScope(scope_detail)

		# insert into redis set

		resp.body = json.encode(appResponce)

	# function to handle all validation
	def __validateHttpPost(self, req):
		# token validation
		self.validateHTTPRequest(req)

		self.__commonValidation(req)

		# data validation
		appResponce = {}

		#db level check
		scope_model = oauth2ScopeModel()
		if scope_model.ifScopeNameExists(req.body["scope_name"]):
			appResponce["scope_name"] = "Scope name already exists in database"

		req.body["allowed_resources"] = list(set(req.body["allowed_resources"]))
		resource_model = oauth2ResourceModel()
		if not resource_model.ifValidResourceExists(req.body["allowed_resources"]):
			appResponce["allowed_resources"] = "Invalid resources provided"

		if appResponce:
			raise appException.clientException_400(appResponce)


	def __commonValidation(self, req, scope_id_check = False):

		appResponce = {}

		if scope_id_check and ("scope_id" not in req.body or req.body["scope_id"] == "" or (not isinstance(req.body["scope_id"], int))):
			appResponce["scope_id"] = "Please provide valid scope"

		if("scope_name" not in req.body or req.body["scope_name"] == "" or (not isinstance(req.body["scope_name"], str))):
			appResponce["scope_name"] = "Please provide valid scope name"

		if("scope_info" not in req.body or req.body["scope_info"] == "" or (not isinstance(req.body["scope_info"], str))):
			appResponce["scope_info"] = "Please provide valid scope info"

		if("allowed_resources" not in req.body or req.body["allowed_resources"] == "" or (not isinstance(req.body["allowed_resources"], list))):
			appResponce["allowed_resources"] = "Please provide list of valid resources"
		else:
			invalid_resource = [resource_id for resource_id in req.body["allowed_resources"] if resource_id == "" or (not isinstance(resource_id, int))]
			if(invalid_resource):
				appResponce["allowed_resources"] = "Please provide list of valid resources"

		if appResponce:
			raise appException.clientException_400(appResponce)


	def put(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpPut(req)

		# this is valid request
		appResponce = {}

		scope_detail = {
			"scope_name" : req.body["scope_name"],
			"scope_info" : req.body["scope_info"],
			"allowed_resources" : req.body["allowed_resources"],
			"id" : req.body["scope_id"]
		}

		appResponce["result"] = scope_model.updateScope(scope_detail)

		# update in redis

		resp.body = json.encode(appResponce)


	def __validateHttpPut(self, req):
		# token validation
		self.validateHTTPRequest(req)

		self.__commonValidation(req)

		# data validation
		appResponce = {}

		#db level check
		scope_model = oauth2ScopeModel()

		if scope_model.ifScopeNameExistsInAnyOtherScope(req.body["scope_name"], req.body["scope_id"]):
			appResponce["scope_name"] = "Scope name already exists in database"

		req.body["allowed_resources"] = list(set(req.body["allowed_resources"]))
		resource_model = oauth2ResourceModel()
		if not resource_model.ifValidResourceExists(req.body["allowed_resources"]):
			appResponce["allowed_resources"] = "Invalid resources provided"

		if appResponce:
			raise appException.clientException_400(appResponce)

	def delete(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpDelete(req)

		# this is valid request
		appResponce = {}
		scope_model = oauth2ScopeModel()

		appResponce["result"] = scope_model.createScope(req.body["scope_id"])

		# delete in redis

		resp.body = json.encode(appResponce)

	def __validateHttpDelete(req):
		# token validation
		self.validateHTTPRequest(req)

		appResponce = {}
		if("scope_id" not in req.body or req.body["scope_id"] == "" or (not isinstance(req.body["scope_id"], int))):
			appResponce["scope_id"] = "Please provide valid scope"

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			#db level check
			#if skill synonym exists
			scope_model = oauth2ScopeModel()
			if scope_model.ifScopeIdExists(req.body["scope_id"]):
				appResponce["scope_id"] = "Scope does not exists"
			if appResponce:
				raise appException.clientException_400(appResponce)
