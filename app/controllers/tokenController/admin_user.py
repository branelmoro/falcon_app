# always extend your controller from base_controller
# always give controller class name same as filename
from ... import falcon
from ..base_controller import baseController
from ..base_controller import appException

from ...library import json

# import all required models here
from ...models.oauth2Model import oauth2ScopeModel
from ...models.oauth2Model import oauth2AdminUserModel

class adminUser(baseController):

	def __init__(self):
		# resource_id = 3
		super().__init__(3)
		# self._path = "/access-scope/"

	def getPath(self):
		return self._path

	def post(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpPost(req)

		# this is valid request
		appResponce = {}

		resp.status = falcon.HTTP_200  # This is the default status

		admin_user_model = oauth2AdminUserModel()

		admin_user_detail = self._getFilteredRequestData(req, ["username", "password", "scope"])

		appResponce["result"] = admin_user_model.createAdminUser(admin_user_detail)

		# insert into redis set

		resp.body = json.encode(appResponce)

	# function to handle all validation
	def __validateHttpPost(self, req):
		# token validation
		self.validateHTTPRequest(req)

		self.__commonPreDBValidation(req)

		self.__commonPostDBValidation(req)


	def __commonPostDBValidation(self, req):

		is_put = (req.method == "PUT")

		if is_put:
			admin_user_id = req.body["admin_user_id"]
		else:
			admin_user_id = None

		# data validation
		appResponce = {}

		#db level check
		admin_user_model = oauth2AdminUserModel()

		if is_put and not admin_user_model.ifAdminUserIdExists(admin_user_id):
			appResponce["admin_user_id"] = self._getError(24)
		elif is_put and not admin_user_model.ifAdminUserEditable(admin_user_id):
			appResponce["username"] = self._getError(25)
		else:
			if "username" in req.body and admin_user_model.ifUserNameExists(req.body["username"], admin_user_id):
				appResponce["username"] = self._getError(26)

			scope_model = oauth2ScopeModel()
			if "scope" in req.body and len(req.body["scope"]) > 0 and not scope_model.ifValidScopesExists(req.body["scope"]):
				appResponce["scope"] = self._getError(27)

		if appResponce:
			raise appException.clientException_400(appResponce)


	def __commonPreDBValidation(self, req):

		is_put = (req.method == "PUT")

		appResponce = {}

		if is_put and ("admin_user_id" not in req.body or req.body["admin_user_id"] == "" or (not isinstance(req.body["admin_user_id"], int))):
			appResponce["admin_user_id"] = self._getError(18)

		if is_put:
			editableFields = ["username", "password", "scope"]
			fieldReceived = [i for i in editableFields if i in req.body]
			if not fieldReceived:
				appResponce["admin_user_id"] = self._getError(19)

		if(
			is_put
			and "username" in req.body
			and (req.body["username"] == "" or (not isinstance(req.body["username"], str)))
		) or (
			not is_put
			and ("username" not in req.body or req.body["username"] == "" or (not isinstance(req.body["username"], str)))
		):
			appResponce["username"] = self._getError(20)

		if(
			is_put
			and "password" in req.body
			and (req.body["password"] == "" or (not isinstance(req.body["password"], str)))
		) or (
			not is_put
			and ("password" not in req.body or req.body["password"] == "" or (not isinstance(req.body["password"], str)))
		):
			appResponce["password"] = self._getError(21)

		if(
			is_put
			and "scope" in req.body
			and not isinstance(req.body["scope"], list)
		) or (
			not is_put
			and ("scope" not in req.body or not isinstance(req.body["scope"], list))
		):
			appResponce["scope"] = self._getError(22)
		else:
			if "scope" in req.body:
				if req.body["scope"]:
					nonInt = [i for i in req.body["scope"] if not isinstance(i, int)]
					if nonInt:
						appResponce["scope"] = self._getError(22)
				else:
					appResponce["scope"] = self._getError(23)

		if appResponce:
			raise appException.clientException_400(appResponce)


	def put(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpPut(req)

		# this is valid request
		appResponce = {}

		admin_user_detail = self._getFilteredRequestData(req, ["admin_user_id", "username", "password", "scope"])

		admin_user_model = oauth2AdminUserModel()
		appResponce["result"] = admin_user_model.updateAdminUser(admin_user_detail)

		# update in redis

		resp.body = json.encode(appResponce)


	def __validateHttpPut(self, req):
		# token validation
		self.validateHTTPRequest(req)

		self.__commonPreDBValidation(req)

		self.__commonPostDBValidation(req)


	def delete(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpDelete(req)

		# this is valid request
		appResponce = {}
		admin_user_model = oauth2AdminUserModel()

		appResponce["result"] = admin_user_model.deleteAdminUser(req.body["admin_user_id"])

		# delete in redis

		resp.body = json.encode(appResponce)


	def __validateHttpDelete(self, req):
		# token validation
		self.validateHTTPRequest(req)

		appResponce = {}
		if("admin_user_id" not in req.body or req.body["admin_user_id"] == "" or (not isinstance(req.body["admin_user_id"], int))):
			appResponce["admin_user_id"] = self._getError(18)

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			#db level check
			#if skill synonym exists
			admin_user_model = oauth2AdminUserModel()

			if not admin_user_model.ifAdminUserIdExists(req.body["admin_user_id"]):
				appResponce["admin_user_id"] = self._getError(24)
			elif not admin_user_model.ifAdminUserEditable(req.body["admin_user_id"]):
				appResponce["username"] = self._getError(25)

		if appResponce:
			raise appException.clientException_400(appResponce)
