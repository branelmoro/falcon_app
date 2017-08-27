# always extend your controller from base_controller
# always give controller class name same as filename
from ... import falcon
from ..controllers.base_controller import baseController
from ..controllers.base_controller import appException

from ...library import json

# import all required models here
from ...models.oauth2Model import oauth2ScopeModel
from ...models.oauth2Model import oauth2AdminUserModel

class adminUser(baseController):

	def __init__(self):
		# resource_id = 3
		super.__init__(self,3)
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
			"username" : req.body["username"],
			"password" : req.body["password"],
			"scope" : req.body["scope"]
		}

		appResponce["result"] = scope_model.createScope(scope_detail)

		# insert into redis set

		resp.body = json.encode(appResponce)

	# function to handle all validation
	def __validateHttpPost(self, req):
		# token validation
		self.validateHTTPRequest(req)

		self.__commonPreDBValidation(req)

		self.__commonPostDBValidation(req)


	def __commonPostDBValidation(self, req, admin_user_id_check = None):
		# data validation
		appResponce = {}

		#db level check
		admin_user_model = oauth2AdminUserModel()
		if admin_user_model.ifUserNameExists(req.body["username"], admin_user_id_check):
			appResponce["username"] = "Username already exists in database"

		scope_model = oauth2ScopeModel()
		if len(req.body["scope"]) > 0 and not scope_model.ifValidScopesExists(req.body["scope"]):
			appResponce["scope"] = "Invalid scopes provided"

		if appResponce:
			raise appException.clientException_400(appResponce)


	def __commonPreDBValidation(self, req, admin_user_id_check = False):

		appResponce = {}

		if admin_user_id_check and ("admin_user_id" not in req.body or req.body["admin_user_id"] == "" or (not isinstance(req.body["admin_user_id"], int))):
			appResponce["admin_user_id"] = "Please provide valid admin id"

		if("username" not in req.body or req.body["username"] == "" or (not isinstance(req.body["username"], str))):
			appResponce["username"] = "Please provide valid user name"

		if("password" not in req.body or req.body["password"] == "" or (not isinstance(req.body["password"], str))):
			appResponce["password"] = "Please provide valid password"

		if("scope" not in req.body and not isinstance(req.body["scope"], list)):
			appResponce["scope"] = "Please provide list of scopes"
		else:
			nonInt = [i for i in appResponce["scope"] if not isinstance(req.body["scope"], int)]
			if nonInt:
				appResponce["scope"] = "Please provide list of valid scopes"

		if appResponce:
			raise appException.clientException_400(appResponce)


	def put(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpPut(req)

		# this is valid request
		appResponce = {}

		scope_detail = {
			"username" : req.body["username"],
			"password" : req.body["password"],
			"scope" : req.body["scope"],
			"id" : req.body["admin_user_id"]
		}

		appResponce["result"] = scope_model.updateScope(scope_detail)

		# update in redis

		resp.body = json.encode(appResponce)


	def __validateHttpPut(self, req):
		# token validation
		self.validateHTTPRequest(req)

		self.__commonPreDBValidation(req, True)

		self.__commonPostDBValidation(req, req.body["admin_user_id"])


	def delete(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpDelete(req)

		# this is valid request
		appResponce = {}
		admin_user_model = oauth2AdminUserModel()

		appResponce["result"] = admin_user_model.deleteAdminUser(req.body["admin_user_id"])

		# delete in redis

		resp.body = json.encode(appResponce)


	def __validateHttpDelete(req):
		# token validation
		self.validateHTTPRequest(req)

		appResponce = {}
		if("admin_user_id" not in req.body or req.body["admin_user_id"] == "" or (not isinstance(req.body["admin_user_id"], int))):
			appResponce["admin_user_id"] = "Please provide valid scope"

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			#db level check
			#if skill synonym exists
			scope_model = oauth2ScopeModel()
			if scope_model.ifScopeIdExists(req.body["admin_user_id"]):
				appResponce["admin_user_id"] = "Scope does not exists"
			if appResponce:
				raise appException.clientException_400(appResponce)
