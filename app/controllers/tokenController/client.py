# always extend your controller from base_controller
# always give controller class name same as filename
from ... import falcon
from ..base_controller import baseController
from ..base_controller import appException

from ...library import json

# import all required models here
from ...models.oauth2Model import oauth2ScopeModel
from ...models.oauth2Model import oauth2ClientModel

class client(baseController):

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

		client_model = oauth2ClientModel()

		client_detail = self._getFilteredRequestData(req, ["client_id", "client_secret", "scope"])

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
			appResponce["client_id"] = "Client id does not exist"
		elif is_put and not client_model.ifClientEditable(client_id):
			appResponce["client_id"] = "Client is not editable"
		else:
			if "client_id" in req.body and client_model.ifClientIdExists(req.body["client_id"], client_id):
				appResponce["client_id"] = "ClientId already exists in database"

			scope_model = oauth2ScopeModel()
			if "scope" in req.body and len(req.body["scope"]) > 0 and not scope_model.ifValidScopesExists(req.body["scope"]):
				appResponce["scope"] = "Invalid scopes provided"

		if appResponce:
			raise appException.clientException_400(appResponce)


	def __commonPreDBValidation(self, req):

		is_put = (req.method == "PUT")

		appResponce = {}

		if is_put and ("client_id" not in req.body or req.body["client_id"] == "" or (not isinstance(req.body["client_id"], int))):
			appResponce["client_id"] = "Please provide valid client id"

		if is_put:
			editableFields = ["client_id", "client_secret", "scope"]
			fieldReceived = [i for i in editableFields if i in req.body]
			if not fieldReceived:
				appResponce["client_id"] = "Please provide information to edit"

		if(
			is_put
			and "client_id" in req.body
			and (req.body["client_id"] == "" or (not isinstance(req.body["client_id"], str)))
		) or (
			not is_put
			and ("client_id" not in req.body or req.body["client_id"] == "" or (not isinstance(req.body["client_id"], str)))
		):
			appResponce["client_id"] = "Please provide valid client id"

		if(
			is_put
			and "client_secret" in req.body
			and (req.body["client_secret"] == "" or (not isinstance(req.body["client_secret"], str)))
		) or (
			not is_put
			and ("client_secret" not in req.body or req.body["client_secret"] == "" or (not isinstance(req.body["client_secret"], str)))
		):
			appResponce["client_secret"] = "Please provide valid client secret"

		if(
			is_put
			and "scope" in req.body
			and not isinstance(req.body["scope"], list)
		) or (
			not is_put
			and ("scope" not in req.body or not isinstance(req.body["scope"], list))
		):
			appResponce["scope"] = "Please provide list of scopes"
		else:
			if "scope" in req.body:
				if req.body["scope"]:
					nonInt = [i for i in req.body["scope"] if not isinstance(i, int)]
					if nonInt:
						appResponce["scope"] = "Please provide list of valid scopes"
				else:
					appResponce["scope"] = "Please provide at least one access scope"

		if appResponce:
			raise appException.clientException_400(appResponce)


	def put(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpPut(req)

		# this is valid request
		appResponce = {}

		client_detail = self._getFilteredRequestData(req, ["client_id", "client_id", "client_secret", "scope"])

		client_model = oauth2ClientModel()
		appResponce["result"] = client_model.updateClient(client_detail)

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
		client_model = oauth2ClientModel()

		appResponce["result"] = client_model.deleteClient(req.body["client_id"])

		# delete in redis

		resp.body = json.encode(appResponce)


	def __validateHttpDelete(self, req):
		# token validation
		self.validateHTTPRequest(req)

		appResponce = {}
		if("client_id" not in req.body or req.body["client_id"] == "" or (not isinstance(req.body["client_id"], int))):
			appResponce["client_id"] = "Please provide valid user id"

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			#db level check
			#if skill synonym exists
			client_model = oauth2ClientModel()

			if not client_model.ifClientIdExists(req.body["client_id"]):
				appResponce["client_id"] = "Client id does not exist"
			elif not client_model.ifClientEditable(req.body["client_id"]):
				appResponce["client_id"] = "Client is not editable"

		if appResponce:
			raise appException.clientException_400(appResponce)
