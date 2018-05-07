# always extend your controller from base_controller
# always give controller class name same as filename
from falcon import HTTP_200
from ..base_controller import baseController
from ..base_controller import appException

from ...library import json

# import all required models here
from ...models.oauth2Model import oauth2ScopeModel
from ...models.oauth2Model import oauth2ClientModel

class client(baseController):

	def __init__(self):
		# resource_id = 3
		# super().__init__(4)
		# self._path = "/access-scope/"

		self._resources = {
			self._getResource('CL') : 'CL'
		}

		self.__allowed_user_types =  ["guest","registered_user","admin"]

	def getPath(self):
		return [i for i in self._resources]

	def post(self, container):
		req = container.req
		resp = container.resp
		"""Handles POST requests"""
		self.__validateHttpPost(req)

		# this is valid request
		appResponce = {}

		resp.status = HTTP_200  # This is the default status

		client_model = oauth2ClientModel()

		client_detail = self._getFilteredRequestData(req, ["app_id", "app_secret", "scope", "user_type"])

		appResponce["result"] = client_model.createClient(client_detail)

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
			client_id = req.body["client_id"]
		else:
			client_id = None

		# data validation
		appResponce = {}

		#db level check
		client_model = oauth2ClientModel()

		if is_put and not client_model.ifClientIdExists(client_id):
			appResponce["client_id"] = self._getError(28)
		elif is_put and not client_model.ifClientEditable(client_id):
			appResponce["client_id"] = self._getError(29)
		else:
			if "app_id" in req.body and client_model.ifAppIdExists(req.body["app_id"], client_id):
				appResponce["app_id"] = self._getError(30)

			scope_model = oauth2ScopeModel()
			if "scope" in req.body and len(req.body["scope"]) > 0 and not scope_model.ifValidScopesExists(req.body["scope"]):
				appResponce["scope"] = self._getError(27)

		if appResponce:
			raise appException.clientException_400(appResponce)


	def __commonPreDBValidation(self, req):

		is_put = (req.method == "PUT")

		appResponce = {}

		if is_put and ("client_id" not in req.body or req.body["client_id"] == "" or (not isinstance(req.body["client_id"], int))):
			appResponce["client_id"] = self._getError(32)

		if is_put:
			editableFields = ["app_id", "app_secret", "scope", "user_type"]
			fieldReceived = [i for i in editableFields if i in req.body]
			if not fieldReceived:
				appResponce["app_id"] = self._getError(31)

		if(
			is_put
			and "app_id" in req.body
			and (req.body["app_id"] == "" or (not isinstance(req.body["app_id"], str)))
		) or (
			not is_put
			and ("app_id" not in req.body or req.body["app_id"] == "" or (not isinstance(req.body["app_id"], str)))
		):
			appResponce["app_id"] = self._getError(33)


		if(
			is_put
			and "user_type" in req.body
			and (req.body["user_type"] == "" or (not isinstance(req.body["user_type"], str)) or req.body["user_type"] not in self.__allowed_user_types)
		) or (
			not is_put
			and ("user_type" not in req.body or req.body["user_type"] == "" or (not isinstance(req.body["user_type"], str)) or req.body["user_type"] not in self.__allowed_user_types)
		):
			appResponce["user_type"] = self._getError(34)


		if(
			is_put
			and "app_secret" in req.body
			and (req.body["app_secret"] == "" or (not isinstance(req.body["app_secret"], str)))
		) or (
			not is_put
			and ("app_secret" not in req.body or req.body["app_secret"] == "" or (not isinstance(req.body["app_secret"], str)))
		):
			appResponce["app_secret"] = self._getError(35)

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
						appResponce["scope"] = self._getError(27)
				else:
					appResponce["scope"] = self._getError(23, data={"endpoint":"client"})

		if appResponce:
			raise appException.clientException_400(appResponce)

	def put(self, container):
		req = container.req
		resp = container.resp
		"""Handles POST requests"""
		self.__validateHttpPut(req)

		# this is valid request
		appResponce = {}

		client_detail = self._getFilteredRequestData(req, ["client_id", "app_id", "app_secret", "scope", "user_type"])

		client_model = oauth2ClientModel()
		appResponce["result"] = client_model.updateClient(client_detail)

		resp.status = HTTP_200  # This is the default status

		resp.body = json.encode(appResponce)


	def __validateHttpPut(self, req):
		# token validation
		self.validateHTTPRequest(req)

		self.__commonPreDBValidation(req)

		self.__commonPostDBValidation(req)

	def delete(self, container):
		req = container.req
		resp = container.resp
		"""Handles POST requests"""
		self.__validateHttpDelete(req)

		# this is valid request
		appResponce = {}
		client_model = oauth2ClientModel()

		appResponce["result"] = client_model.deleteClient(req.body["client_id"])

		resp.status = HTTP_200  # This is the default status

		resp.body = json.encode(appResponce)


	def __validateHttpDelete(self, req):
		# token validation
		self.validateHTTPRequest(req)

		appResponce = {}
		if("client_id" not in req.body or req.body["client_id"] == "" or (not isinstance(req.body["client_id"], int))):
			appResponce["client_id"] = self._getError(32)

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			#db level check
			#if skill synonym exists
			client_model = oauth2ClientModel()

			if not client_model.ifClientIdExists(req.body["client_id"]):
				appResponce["client_id"] = self._getError(28)
			elif not client_model.ifClientEditable(req.body["client_id"]):
				appResponce["client_id"] = self._getError(29)

		if appResponce:
			raise appException.clientException_400(appResponce)
