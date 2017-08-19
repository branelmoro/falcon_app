# always extend your controller from base_controller
# always give controller class name same as filename
from ... import falcon
from ..controllers.base_controller import baseController
from ..controllers.base_controller import appException

from ...library import json

# import all required models here
from ...models.specialityModel import skillSearchModel
from ...models.specialityModel import skillSynonymModel
from ...models.specialityModel import skillParentModel

class resource(baseController):

	def __init__(self):
		self.__path = "/resource/"

	def getPath(self):
		return self.__path

	def post(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpPost(req)

		# this is valid request
		appResponce = {}

		resp.status = falcon.HTTP_200  # This is the default status

		resp.body = json.encode(appResponce)

	# function to handle all validation
	def __validateHttpPost(self, req):
		# token validation
		self.validateHTTPRequest(req)

		# data validation
		appResponce = {}



	def delete(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpDelete(req)

		# this is valid request
		appResponce = {}


		resp.body = json.encode(appResponce)

	def __validateHttpDelete(req):
		# token validation
		self.validateHTTPRequest(req)

		appResponce = {}
		if("skill_synonym_id" not in req.body or req.body["skill_synonym_id"] == "" or (not isinstance(req.body["skill_synonym_id"], int))):
			appResponce["skill_synonym_id"] = "Please provide valid skill"

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			#db level check
			#if skill synonym exists
			skill_synonym_model = skillSynonymModel()
			if not skill_synonym_model.ifValidSkillNameExists(req.body["skill_synonym_id"]):
				appResponce["skill_synonym_id"] = "Please provide valid skill name"
			if appResponce:
				raise appException.clientException_400(appResponce)
