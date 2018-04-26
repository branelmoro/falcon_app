# always extend your controller from base_controller
# always give controller class name same as filename
from falcon import HTTP_200
from ..base_controller import baseController
from ..base_controller import appException

from ...library import json

# import all required models here
from ...models.specialityModel import searchSkillModel
from ...models.specialityModel import skillSynonymModel
from ...models.specialityModel import skillParentModel

class skillSynonym(baseController):

	def __init__(self):
		self.__path = "/create-skill-sysnonym/"

	def getPath(self):
		return self.__path

	def post(self, container):
		req = container.req
		resp = container.resp
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

		appResponce["result"] = self.createSynonymForSkill(search_skill, req.body["skill_synonym_id"])

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

	def delete(self, container):
		req = container.req
		resp = container.resp
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


class skillSynonymStatus(baseController):

	def __init__(self):
		self.__path = "/skill-synonym-status/"

	def getPath(self):
		return self.__path

	def post(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpPost(req)

		appResponce = {}

		resp.status = HTTP_200  # This is the default status

		skill_synonym_model = skillSynonymModel()
		if req.body["status"] == "invalid":
			appResponce["result"] = skill_synonym_model.markSearchSkillInvalid(req.body["skill_synonym_id"])
		else:
			if "parent_skill_synonym_id" in req.body:
				appResponce["result"] = skill_synonym_model.createSynonymFromParentSkillSynonym(req.body["skill_synonym_id"], req.body["languages"], req.body["parent_skill_synonym_id"])
			else:
				search_skill_model = searchSkillModel()
				#create new parent skill and mark entry in skill_synonym
				arrLang = self.getAllLangs()

				skill_synonym_detail = skill_synonym_model.getSkillSynonymDetailFromId(req.body["skill_synonym_id"])

				search_words = [req.body["all_langs"][k] for k in req.body["all_langs"] if k in arrLang]

				search_skill_detail = search_skill_model.getSearchSkillDetailFromSearchWord(search_words)

				params = {k:req.body["all_langs"][k] for k in req.body["all_langs"] if k in arrLang}

				if "skill_info" in req.body:
					params["skill_info"] = req.body["skill_info"]

				if "skill_icon_path" in req.body:
					params["skill_icon_path"] = req.body["skill_icon_path"]

				if "skill_info" not in req.body:
					params["skill_info"] = ""

				skill_parent_model = skillParentModel()
				appResponce["result"] = skill_parent_model.createParentSkillFromSkillSynonym(params,search_skill_detail,skill_synonym_detail)

		resp.body = json.encode(appResponce)

	# function to handle all validation
	def __validateHttpPost(self, req):
		# token validation
		self.validateHTTPRequest(req)
		
		# data validation
		appResponce = {}
		if("skill_synonym_id" not in req.body or req.body["skill_synonym_id"] == "" or (not isinstance(req.body["skill_synonym_id"], int))):
			appResponce["skill_synonym_id"] = "Please provide valid skill"
		if("status" not in req.body or req.body["status"] == ""):
			appResponce["status"] = "Please provide skill status - valid or invalid"
		elif req.body["status"] != "valid" and req.body["status"] != "invalid":
			appResponce["status"] = "Please provide correct status - valid or invalid"
		elif req.body["status"] == "valid":
			arrLang = self.getAllLangs()

			if "parent_skill_synonym_id" not in req.body and "all_langs" not in req.body:
				appResponce["parent_skill_synonym_id"] = "Please provide new skill details or parent skill"
			elif "parent_skill_synonym_id" in req.body:
				if not isinstance(req.body["parent_skill_synonym_id"], int):
					appResponce["parent_skill_synonym_id"] = "Please provide valid skill synonym"

				if("languages" not in req.body or not isinstance(req.body["languages"], list) or len(req.body["languages"]) == 0):
					appResponce["languages"] = "Please provide languages for skill"
				elif:
					arrInvalidLangs = [item for item in req.body["languages"] if (not isinstance(item, str) or item not in arrLang]
					if arrNotFoundLang:
						appResponce["languages"] = "Invalid languages found - " + (",".join(arrInvalidLangs))

			elif "all_langs" in req.body:
				if isinstance(req.body["all_langs"], dict):
					arrNotFoundLang = [item for item in arrLang if item not in req.body["all_langs"] or (not isinstance(req.body["all_langs"][item], str)) or req.body["all_langs"][item] == ""]
					if arrNotFoundLang:
						appResponce["all_langs"] = "Please provide skill values for languages - " + (",".join(arrNotFoundLang))
				else:
					appResponce["all_langs"] = "Please provide valid languages for skill"

				if "skill_info" in req.body and (not isinstance(req.body["skill_info"], str)):
					appResponce["skill_info"] = "Please provide valid information of new skill"

				if "skill_icon_path" in req.body and (not isinstance(req.body["skill_icon_path"], str)):
					appResponce["skill_icon_path"] = "Please provide valid icon path of new skill"

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			# database level validation goes here
			skill_synonym_model = skillSynonymModel()
			if "skill_synonym_id" in req.body:
				skill_exists = skill_synonym_model.ifPendingSkillNameExists(req.body["skill_synonym_id"])
				if not skill_exists:
					appResponce["skill_synonym_id"] = "Please provide valid skill name"

			if "parent_skill_synonym_id" in req.body:
				if not skill_synonym_model.ifValidSkillNameExists(req.body["parent_skill_synonym_id"]):
					appResponce["parent_skill_synonym_id"] = "Please provide valid parent skill name"
			else:
				arrSearchSkill = [req.body["all_langs"][lang] for lang in req.body["all_langs"]];
				if not skill_synonym_model.ifValidLangProvidedForSkillSynonym(req.body["skill_synonym_id"],arrSearchSkill):
					appResponce["all_langs"] = "Please provide valid Language for skill!"
				else:
					arrSynonyms = skill_synonym_model.getSkillSynonymsByName(arrSearchSkill);
					if arrSynonyms:
						appResponce["all_langs"] = "Skill names already present in system! - " + (",".join(arrSynonyms))

			if appResponce:
				raise appException.clientException_400(appResponce)


class skillSynonymLanguages(baseController):

	def __init__(self):
		self.__path = "/skill-synonym-languages/"

	def getPath(self):
		return self.__path

	def put(self, container):
		req = container.req
		resp = container.resp
		"""Handles POST requests"""
		self.__validateHttpPut(req)

		# this is valid request
		appResponce = {}
		# add languages to synonym id
		skill_synonym_model = skillSynonymModel()
		appResponce["result"] = skill_synonym_model.addLanguagesToSkillSynonym(req.body["skill_synonym_id"],req.body["languages"])
		resp.body = json.encode(appResponce)


	def __validateHttpPut(req):
		# token validation
		self.validateHTTPRequest(req)
		
		# data validation
		appResponce = {}
		if("skill_synonym_id" not in req.body or req.body["skill_synonym_id"] == "" or (not isinstance(req.body["skill_synonym_id"], int))):
			appResponce["skill_synonym_id"] = "Please provide valid skill"

		if("languages" not in req.body or (not isinstance(req.body["languages"], list)) or len(req.body["languages"])):
			appResponce["languages"] = "Please provide language for synonym skill word"
		else:
			arrLangs = self.getAllLangs();
			invalidLangs = [a for a in req.body["languages"] if (not isinstance(a, str) or a not in arrLangs)]
			if(len(invalidLangs)):
				appResponce["languages"] = "Invalid languages found for synonym skill word".(",".join(invalidLangs))

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			#db level check
			skill_synonym_model = skillSynonymModel()
			if not skill_synonym_model.ifValidSkillNameExists(req.body["skill_synonym_id"]):
				appResponce["skill_synonym_id"] = "Please provide valid skill name"

			#if language already exists in skill synonym
			skill_langs = skill_synonym_model.ifSkillLanguagesExists(req.body["skill_synonym_id"],req.body["languages"])
			existingLangs = [a for a in skill_langs if a in req.body["languages"]]
			if(len(existingLangs)):
				appResponce["languages"] = "Languages already exists for synonym skill word".(",".join(existingLangs))

			if appResponce:
				raise appException.clientException_400(appResponce)


	def delete(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpDelete(req)

		# this is valid request
		appResponce = {}

		# remove language from synonym id
		skill_synonym_model = skillSynonymModel()
		appResponce["result"] = removeLanguageFromSkillSynonym(self,skill_synonym_id,language)
		resp.body = json.encode(appResponce)

	def __validateHttpDelete(req):
		# token validation
		self.validateHTTPRequest(req)

		appResponce = {}
		if("skill_synonym_id" not in req.body or req.body["skill_synonym_id"] == "" or (not isinstance(req.body["skill_synonym_id"], int))):
			appResponce["skill_synonym_id"] = "Please provide valid skill"

		if("language" not in req.body or (not isinstance(req.body["language"], str)) ):
			appResponce["language"] = "Please provide language for synonym skill word"

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			#db level check
			#if language does not exists in skill synonym
			skill_synonym_model = skillSynonymModel()
			if not skill_synonym_model.ifValidSkillNameExists(req.body["skill_synonym_id"]):
				appResponce["skill_synonym_id"] = "Please provide valid skill name"

			if skill_synonym_model.ifAlternateSkillSynonymExistsForLanguage(req.body["skill_synonym_id"],req.body["language"]):
				appResponce["skill_synonym_id"] = "Can't remove language from skill name, alternate skill synonym does not exists in language, Please create alternate skill synonym in language - "+req.body["language"]

			if appResponce:
				raise appException.clientException_400(appResponce)