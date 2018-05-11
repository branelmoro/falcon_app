# always extend your controller from base_controller
# always give controller class name same as filename
from falcon import HTTP_200
from ..base_controller import baseController
from ..base_controller import appException

from ...library import json

# import all required models here
from ...models.staticTextModel import labelsModel

class labels(baseController):

	def __init__(self):
		# super().__init__(5)
		# self.__path = "/labels/"
		self._resources = {
			self._getResource('LB') : 'LB'
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

		label_model = labelsModel()

		arrFields = self.getAllLangs()
		arrFields.extend(["info"])
		label_detail = self._getFilteredRequestData(req, arrFields)

		appResponce["result"] = label_model.createLabel(label_detail)

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

		if is_put and ("label_id" not in req.body or (not isinstance(req.body["label_id"], int))):
			appResponce["label_id"] = self._getError('ER_VALID_ID')
			raise appException.clientException_400(appResponce)

		arrLangs = self.getAllLangs()
		langsToAdd = [a for a in arrLangs if a in req.body]
		if is_put and ("info" not in req.body and not langsToAdd):
			appResponce["label_id"] = self._getError('NEED_INFO')
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
			label_id = req.body["label_id"]
		else:
			label_id = None

		# data validation
		appResponce = {}

		#db level check
		label_model = labelsModel()

		if is_put and not label_model.ifLabelIdExists(label_id):
			appResponce["label_id"] = self._getError('ER_NO_EXISTS')
		elif is_put and not label_model.ifLabelEditable(label_id):
			appResponce["label_id"] = self._getError('ER_NO_EDIT')
		else:
			if "english" in req.body and label_model.ifEnglishLabelExists(req.body["english"], label_id):
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
		arrFields.extend(["label_id","info"])
		label_detail = self._getFilteredRequestData(req, arrFields)

		label_model = labelsModel()
		appResponce["result"] = label_model.updateLabel(label_detail)

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
		label_detail = labelsModel()

		appResponce["result"] = label_detail.deleteLabel(req.body["label_id"])

		resp.status = HTTP_200  # This is the default status

		resp.body = json.encode(appResponce)


	def __validateHttpDelete(self, req):
		# token validation
		self.validateHTTPRequest(req)

		appResponce = {}
		if("label_id" not in req.body or req.body["label_id"] == "" or (not isinstance(req.body["label_id"], int))):
			appResponce["label_id"] = self._getError('ER_VALID_ID')

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			#db level check
			#if skill synonym exists
			label_detail = labelsModel()

			if not label_detail.ifLabelIdExists(req.body["label_id"]):
				appResponce["label_id"] = self._getError('ER_NO_EXISTS')
			elif not label_detail.ifLabelEditable(req.body["label_id"]):
				appResponce["label_id"] = self._getError('ER_NO_EDIT')

		if appResponce:
			raise appException.clientException_400(appResponce)
