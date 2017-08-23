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
		# resource_id = 1
		super.__init__(self,2)
		# self.__path = "/access-scope/"

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
			"allowed_get" : req.body["allowed_get"]
		}

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

		req.body["allowed_get"] = list(set(req.body["allowed_get"]))
		resource_model = oauth2ResourceModel()
		if not resource_model.ifValidResourceExists(req.body["allowed_get"]):
			appResponce["allowed_get"] = "Invalid resources provided"

		if appResponce:
			raise appException.clientException_400(appResponce)


	def __checkAllowedActionExist(self, req, appResponce, allowed_method):
		if(allowed_method in req.body):
			if(not isinstance(req.body[allowed_method], list)):
				appResponce[allowed_method] = "Please provide list of get resources"
			else:
				nonInt = [i for i in appResponce[allowed_method] if not isinstance(req.body[allowed_method], int)]
				if nonInt:
					appResponce[allowed_method] = "Please provide list of valid get resources"
		return appResponce


	def __commonValidation(self, req, scope_id_check = False):

		appResponce = {}

		if scope_id_check and ("scope_id" not in req.body or req.body["scope_id"] == "" or (not isinstance(req.body["scope_id"], int))):
			appResponce["scope_id"] = "Please provide valid scope"

		if("scope_name" not in req.body or req.body["scope_name"] == "" or (not isinstance(req.body["scope_name"], str))):
			appResponce["scope_name"] = "Please provide valid scope name"

		if("scope_info" not in req.body or req.body["scope_info"] == "" or (not isinstance(req.body["scope_info"], str))):
			appResponce["scope_info"] = "Please provide valid scope info"


		if("allowed_get" not in req.body and "allowed_post" not in req.body and "allowed_put" not in req.body and "allowed_delete" not in req.body):
			appResponce["scope_info"] = "Please provide list of resources"
		else:
			appResponce = self.__checkAllowedActionExist(req, appResponce, "allowed_get")
			appResponce = self.__checkAllowedActionExist(req, appResponce, "allowed_post")
			appResponce = self.__checkAllowedActionExist(req, appResponce, "allowed_put")
			appResponce = self.__checkAllowedActionExist(req, appResponce, "allowed_delete")

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
			"allowed_get" : req.body["allowed_get"],
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

		req.body["allowed_get"] = list(set(req.body["allowed_get"]))
		resource_model = oauth2ResourceModel()
		if not resource_model.ifValidResourceExists(req.body["allowed_get"]):
			appResponce["allowed_get"] = "Invalid resources provided"

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
