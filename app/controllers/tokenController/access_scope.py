# always extend your controller from base_controller
# always give controller class name same as filename
from falcon import HTTP_200
from ..base_controller import baseController
from ..base_controller import appException

from ...library import json

# import all required models here
from ...models.oauth2Model import oauth2ScopeModel
from ...models.oauth2Model import oauth2ResourceModel

class accessScope(baseController):

	def __init__(self):
		# resource_id = 1
		super().__init__(2)
		# self._path = "/access-scope/"

	def getPath(self):
		return self._path

	def post(self, container):
		req = container.req
		resp = container.resp
		"""Handles POST requests"""
		self.__validateHttpPost(req)

		# this is valid request
		appResponce = {}

		resp.status = HTTP_200  # This is the default status

		scope_model = oauth2ScopeModel()

		scope_detail = self._getFilteredRequestData(req, ["scope_name", "scope_info", "allowed_get", "allowed_post", "allowed_put", "allowed_delete"])

		appResponce["result"] = scope_model.createScope(scope_detail)

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
			scope_id = req.body["scope_id"]
		else:
			scope_id = None

		# data validation
		appResponce = {}

		#db level check
		scope_model = oauth2ScopeModel()

		if is_put and not scope_model.ifScopeIdExists(scope_id):
			appResponce["scope_id"] = self._getError(13)
		elif is_put and not scope_model.ifScopeEditable(scope_id):
			appResponce["scope_id"] = self._getError(14)
		else:
			if "scope_name" in req.body and scope_model.ifScopeNameExists(req.body["scope_name"], scope_id):
				appResponce["scope_name"] = self._getError(15)

			resource_model = oauth2ResourceModel()
			if "allowed_get" in req.body and len(req.body["allowed_get"]) > 0 and not resource_model.ifValidResourcesExists(req.body["allowed_get"]):
				appResponce["allowed_get"] = self._getError(16, data={"method":"get"})
			if "allowed_post" in req.body and len(req.body["allowed_post"]) > 0 and not resource_model.ifValidResourcesExists(req.body["allowed_post"]):
				appResponce["allowed_post"] = self._getError(16, data={"method":"post"})
			if "allowed_put" in req.body and len(req.body["allowed_put"]) > 0 and not resource_model.ifValidResourcesExists(req.body["allowed_put"]):
				appResponce["allowed_put"] = self._getError(16, data={"method":"put"})
			if "allowed_delete" in req.body and len(req.body["allowed_delete"]) > 0 and not resource_model.ifValidResourcesExists(req.body["allowed_delete"]):
				appResponce["allowed_delete"] = self._getError(16, data={"method":"delete"})

			# for update scope case
			if is_put:
				# check if atleast once resource is given
				lstAllowedScopes = ["allowed_get", "allowed_post", "allowed_put", "allowed_delete"]
				receivedScopes = [i for i in lstAllowedScopes if i in req.body]
				receivedNonEmptyScopes = [i for i in receivedScopes if len(req.body[i]) > 0]
				if receivedScopes and not receivedNonEmptyScopes:
					checkDbScopes = [i for i in lstAllowedScopes if i not in req.body]
					if checkDbScopes:
						# run query to check if atleat one resource access exists
						if not scope_model.ifAtleastOneResourceAccessIsGiven(scope_id, checkDbScopes):
							appResponce["allowed_resource"] = self._getError(12)
					else:
						appResponce["allowed_resource"] = self._getError(12)

		if appResponce:
			raise appException.clientException_400(appResponce)


	def __checkAllowedActionList(self, req, appResponce, allowed_method, is_put):
		if(allowed_method in req.body):
			if(not isinstance(req.body[allowed_method], list)):
				appResponce[allowed_method] = self._getError(16, data={"method":allowed_method})
			else:
				nonInt = [i for i in req.body[allowed_method] if not isinstance(i, int)]
				if nonInt:
					appResponce[allowed_method] = self._getError(16, data={"method":allowed_method})
		else:
			if not is_put:
				req.body[allowed_method] = []
		return appResponce


	def __commonPreDBValidation(self, req):

		is_put = (req.method == "PUT")

		appResponce = {}

		if is_put and ("scope_id" not in req.body or req.body["scope_id"] == "" or (not isinstance(req.body["scope_id"], int))):
			appResponce["scope_id"] = self._getError(8)

		if is_put:
			editableFields = ["scope_name", "scope_info", "allowed_get", "allowed_post", "allowed_put", "allowed_delete"]
			fieldReceived = [i for i in editableFields if i in req.body]
			if not fieldReceived:
				appResponce["scope_id"] = self._getError(9)

		if(
			is_put
			and "scope_name" in req.body
			and (req.body["scope_name"] == "" or (not isinstance(req.body["scope_name"], str)))
		) or (
			not is_put
			and ("scope_name" not in req.body or req.body["scope_name"] == "" or (not isinstance(req.body["scope_name"], str)))
		):
			appResponce["scope_name"] = self._getError(10)


		if(
			is_put
			and "scope_info" in req.body
			and (req.body["scope_info"] == "" or (not isinstance(req.body["scope_info"], str)))
		) or (
			not is_put
			and ("scope_info" not in req.body or req.body["scope_info"] == "" or (not isinstance(req.body["scope_info"], str)))
		):
			appResponce["scope_info"] = self._getError(11)


		if(not is_put and "allowed_get" not in req.body and "allowed_post" not in req.body and "allowed_put" not in req.body and "allowed_delete" not in req.body):
			appResponce["allowed_resource"] = self._getError(12)
		else:
			appResponce = self.__checkAllowedActionList(req, appResponce, "allowed_get", is_put)
			appResponce = self.__checkAllowedActionList(req, appResponce, "allowed_post", is_put)
			appResponce = self.__checkAllowedActionList(req, appResponce, "allowed_put", is_put)
			appResponce = self.__checkAllowedActionList(req, appResponce, "allowed_delete", is_put)

			# for create scope case
			if not is_put:
				lstAllowedScopes = ["allowed_get", "allowed_post", "allowed_put", "allowed_delete"]
				receivedScopes = [i for i in lstAllowedScopes if i in req.body and len(req.body[i]) > 0]
				if not receivedScopes:
					appResponce["allowed_resource"] = self._getError(12)


		if appResponce:
			raise appException.clientException_400(appResponce)

	def put(self, container):
		req = container.req
		resp = container.resp
		"""Handles POST requests"""
		self.__validateHttpPut(req)

		# this is valid request
		appResponce = {}


		scope_detail = self._getFilteredRequestData(req, ["scope_name", "scope_info", "allowed_get", "allowed_post", "allowed_put", "allowed_delete"])
		scope_detail["id"] = req.body["scope_id"]

		scope_model = oauth2ScopeModel()
		appResponce["result"] = scope_model.updateScope(scope_detail)

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
		scope_model = oauth2ScopeModel()

		appResponce["result"] = scope_model.deleteScope(req.body["scope_id"])

		resp.status = HTTP_200  # This is the default status

		resp.body = json.encode(appResponce)


	def __validateHttpDelete(self, req):
		# token validation
		self.validateHTTPRequest(req)

		appResponce = {}
		if("scope_id" not in req.body or req.body["scope_id"] == "" or (not isinstance(req.body["scope_id"], int))):
			appResponce["scope_id"] = self._getError(8)

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			#db level check
			#if skill synonym exists
			scope_model = oauth2ScopeModel()
			if not scope_model.ifScopeIdExists(req.body["scope_id"]):
				appResponce["scope_id"] = self._getError(13)
			elif not scope_model.ifScopeEditable(req.body["scope_id"]):
				appResponce["scope_name"] = self._getError(14)

		if appResponce:
			raise appException.clientException_400(appResponce)
