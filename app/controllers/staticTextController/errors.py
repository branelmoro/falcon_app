# always extend your controller from base_controller
# always give controller class name same as filename
from falcon import HTTP_200
from ..base_controller import baseController
from ..base_controller import appException

from ...library import json

# import all required models here
from ...models.staticTextModel import errorsModel

class errors(baseController):

	def __init__(self):
		# super().__init__(5)
		# self.__path = "/errors/"
		self._resources = {
			self._getResource('ER') : 'ER'
		}

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
			appResponce["error_id"] = self._getError('ER_VALID_ID')
			raise appException.clientException_400(appResponce)

		arrLangs = self.getAllLangs()
		langsToAdd = [a for a in arrLangs if a in req.body]
		if is_put and ("info" not in req.body and not langsToAdd):
			appResponce["error_id"] = self._getError('NEED_INFO')
			raise appException.clientException_400(appResponce)

		if(
			is_put
			and "info" in req.body
			and (req.body["info"] == "" or (not isinstance(req.body["info"], str)))
		) or (
			not is_put
			and ("info" not in req.body or req.body["info"] == "" or (not isinstance(req.body["info"], str)))
		):
			appResponce["info"] = self._getError('ER_INFO')

		if(
			is_put
			and "english" in req.body
			and (req.body["english"] == "" or (not isinstance(req.body["english"], str)))
		) or (
			not is_put
			and ("english" not in req.body or req.body["english"] == "" or (not isinstance(req.body["english"], str)))
		):
			appResponce["english"] = self._getError('ER_MSG', data={"language":"english"})

		if langsToAdd:
			invalidLangs = [a for a in langsToAdd if not isinstance(req.body[a], str) or req.body[a] == ""]
			if invalidLangs:
				for lang in invalidLangs:
					appResponce[lang] = self._getError('ER_MSG', data={"language":lang})

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
			appResponce["error_id"] = self._getError('ER_NO_EXISTS')
		elif is_put and not error_model.ifErrorEditable(error_id):
			appResponce["error_id"] = self._getError('ER_NO_EDIT')
		else:
			if "english" in req.body and error_model.ifEnglishErrorExists(req.body["english"], error_id):
				appResponce["english"] = self._getError('ER_EXISTS', data={"language":"english"})

		if appResponce:
			raise appException.clientException_400(appResponce)

	def put(self, container):
		req = container.req
		resp = container.resp
		"""Handles POST requests"""
		self.__validateHttpPut(req)

		# this is valid request
		appResponce = {}

		arrFields = self.getAllLangs()
		arrFields.extend(["error_id","info"])
		error_detail = self._getFilteredRequestData(req, arrFields)

		error_model = errorsModel()
		appResponce["result"] = error_model.updateError(error_detail)

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
		error_detail = errorsModel()

		appResponce["result"] = error_detail.deleteError(req.body["error_id"])

		resp.status = HTTP_200  # This is the default status

		resp.body = json.encode(appResponce)


	def __validateHttpDelete(self, req):
		# token validation
		self.validateHTTPRequest(req)

		appResponce = {}
		if("error_id" not in req.body or req.body["error_id"] == "" or (not isinstance(req.body["error_id"], int))):
			appResponce["error_id"] = self._getError('ER_VALID_ID')

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			#db level check
			#if skill synonym exists
			error_detail = errorsModel()

			if not error_detail.ifErrorIdExists(req.body["error_id"]):
				appResponce["error_id"] = self._getError('ER_NO_EXISTS')
			elif not error_detail.ifErrorEditable(req.body["error_id"]):
				appResponce["error_id"] = self._getError('ER_NO_EDIT')

		if appResponce:
			raise appException.clientException_400(appResponce)
