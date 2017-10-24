# always extend your controller from base_controller
# always give controller class name same as filename
from falcon import HTTP_200
from ..base_controller import baseController
from ..base_controller import appException

from ...library import json

# import all required models here
from ...models.staticTextModel import errorsModel

class skillParent(baseController):

	def __init__(self):
		super().__init__(5)
		# self.__path = "/errors/"

	def getPath(self):
		return self.__path

	def post(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpPost(req)

		# this is valid request
		appResponce = {}

		resp.status = falcon.HTTP_200  # This is the default status

		error_model = errorsModel()

		arrFields = self.getAllLangs()
		arrFields.extend(["info"])
		error_detail = self._getFilteredRequestData(req, arrFields)

		appResponce["result"] = error_model.createError(error_detail)

		resp.body = json.encode(appResponce)

	# function to handle all validation
	def __validateHttpPost(self, req):
		# token validation
		self.validateHTTPRequest(req)

		self.__commonPreDBValidation(req)

		self.__commonPostDBValidation(req)


	def __commonPreDBValidation(self, req):

		is_put = (req.method == "PUT")

		appResponce = {}

		if is_put and ("error_id" not in req.body or (not isinstance(req.body["error_id"], int))):
			appResponce["error_id"] = self._getError(36)
			raise appException.clientException_400(appResponce)

		arrLangs = self.getAllLangs()
		langsToAdd = [a for a in arrLangs if a in req.body]
		if is_put and ("info" not in req.body and not langsToAdd):
			appResponce["error_id"] = self._getError(37)
			raise appException.clientException_400(appResponce)

		if(
			is_put
			and "info" in req.body
			and (req.body["info"] == "" or (not isinstance(req.body["info"], str)))
		) or (
			not is_put
			and ("info" not in req.body or req.body["info"] == "" or (not isinstance(req.body["info"], str)))
		):
			appResponce["info"] = self._getError(38)

		if(
			is_put
			and "english" in req.body
			and (req.body["english"] == "" or (not isinstance(req.body["english"], str)))
		) or (
			not is_put
			and ("english" not in req.body or req.body["english"] == "" or (not isinstance(req.body["english"], str)))
		):
			appResponce["english"] = self._getError(39, data={"language":"english"})

		if langsToAdd:
			invalidLangs = [a for a in langsToAdd if not isinstance(a, str) or a == ""]
			if invalidLangs:
				for lang in invalidLangs:
					appResponce[lang] = self._getError(39, data={"language":lang})

		if appResponce:
			raise appException.clientException_400(appResponce)


	def __commonPostDBValidation(self, req):

		is_put = (req.method == "PUT")

		if is_put:
			error_id = req.body["error_id"]
		else:
			error_id = None

		# data validation
		appResponce = {}

		#db level check
		error_model = errorsModel()

		if is_put and not error_model.ifErrorIdExists(error_id):
			appResponce["error_id"] = self._getError(40)
		elif is_put and not error_model.ifErrorEditable(error_id):
			appResponce["error_id"] = self._getError(41)
		else:
			if "english" in req.body and error_model.ifEnglishErrorExists(req.body["english"], error_id):
				appResponce["english"] = self._getError(42, data={"language":"english"})

		if appResponce:
			raise appException.clientException_400(appResponce)


	def put(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpPut(req)

		# this is valid request
		appResponce = {}

		arrFields = self.getAllLangs()
		arrFields.extend(["error_id","info"])
		error_detail = self._getFilteredRequestData(req, arrFields)

		error_detail = errorsModel()
		appResponce["result"] = error_detail.updateError(error_detail)

		# update in redis
		resp.body = json.encode(appResponce)


	def delete(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpDelete(req)

		# this is valid request
		appResponce = {}
		error_detail = errorsModel()

		appResponce["result"] = error_detail.deleteError(req.body["error_id"])

		# delete in redis

		resp.body = json.encode(appResponce)


	def __validateHttpDelete(self, req):
		# token validation
		self.validateHTTPRequest(req)

		appResponce = {}
		if("error_id" not in req.body or req.body["error_id"] == "" or (not isinstance(req.body["error_id"], int))):
			appResponce["error_id"] = self._getError(36)

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			#db level check
			#if skill synonym exists
			error_detail = errorsModel()

			if not error_detail.ifErrorIdExists(req.body["error_id"]):
				appResponce["error_id"] = self._getError(40)
			elif not error_detail.ifErrorEditable(req.body["error_id"]):
				appResponce["error_id"] = self._getError(41)

		if appResponce:
			raise appException.clientException_400(appResponce)
