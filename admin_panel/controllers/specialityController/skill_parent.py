# always extend your controller from base_controller
# always give controller class name same as filename
from falcon import HTTP_200
from ..base_controller import baseController
from ..base_controller import appException

from ...library import json

# import all required models here
from ...models.specialityModel import skillSearchModel
from ...models.specialityModel import skillSynonymModel
from ...models.specialityModel import skillParentModel

class skillParent(baseController):

	def __init__(self):
		self.__path = "/create-skill-parent/"

	def getPath(self):
		return self.__path

	def post(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpPost(req)

		# this is valid request
		appResponce = {}

		resp.status = HTTP_200  # This is the default status

		# create model object
		skill_synonym_model = skillSynonymModel()

		skill_detail = {
			"skill_name" : req.body["skill_synonym_word"],
			"language" : req.body["languages"],
			"search_count" : 0,
			"assigned_to" : 0
		}

		appResponce["result"] = skill_synonym_model.createSynonymForSkill(search_skill, req.body["skill_synonym_id"])

		resp.body = json.encode(appResponce)

	# function to handle all validation
	def __validateHttpPost(self, req):
		# token validation
		self.validateHTTPRequest(req)

		# data validation
		appResponce = {}

		if("skill_synonym_word" not in req.body or (not isinstance(req.body["skill_synonym_word"], str)) or req.body["skill_synonym_word"] == ""):
			appResponce["skill_synonym_word"] = "Please provide synonym search word"
		if("languages" not in req.body or (not isinstance(req.body["languages"], list)) or len(req.body["languages"])):
			appResponce["languages"] = "Please provide languages for synonym skill word"
		else:
			arrLangs = self.getAllLangs();
			invalidLangs = [a for a in req.body["languages"] if (not isinstance(a, str) or a not in arrLangs)]
			if(len(invalidLangs)):
				appResponce["skill_synonym_id"] = "Invalid languages found for synonym skill word".(",".join(invalidLangs))
		if("skill_synonym_id" not in req.body or (not isinstance(req.body["skill_synonym_id"], int))):
			appResponce["skill_synonym_id"] = "Please provide parent synonym skill word"

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			# db level checks
			skill_synonym_model = skillSynonymModel()
			if skill_synonym_model.ifSkillSynonymAlreadyExists(appResponce["skill_synonym_word"]):
				appResponce["skill_synonym_word"] = "Skill Synonym already exists in database!"
			if not skill_synonym_model.ifValidSkillNameExists(req.body["skill_synonym_id"]):
				appResponce["skill_synonym_id"] = "Please provide valid parent skill name"
			if appResponce:
				raise appException.clientException_400(appResponce)


	def delete(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpDelete(req)

		# this is valid request
		appResponce = {}

		skill_synonym_model = skillSynonymModel()
		appResponce["result"] = skill_synonym_model.removeSkillSynonymById(req.body["skill_synonym_id"])
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
