# always extend your controller from base_controller
# always give controller class name same as filename
from falcon import HTTP_200
from ..base_controller import baseController, CRUDS
from ..base_controller import appException

from ...library import json

# import all required models here
from ...models.specialityModel import searchSkillModel
from ...models.specialityModel import skillSynonymModel
from ...models.specialityModel import skillParentModel



class SearchSkill(CRUDS):

	def __init__(self):
		self._search_template = '/search-skill/_find_'
		self._search_page_template = '/search-skill/_find_/{page:int}'
		self._create_template = '/search-skill/'
		self._crud_template = '/search-skill/{uid:int}'

	def getPath(self):
		return [
			self._create_template,
			self._search_template,
			self._search_page_template,
			self._crud_template
		]

	def _search(self, container, page=1):
		req = container.req
		resp = container.resp
		params = req.params
		params.update(req.body)

		params['page'] = page

		if 'count_per_page' not in params:
			params['count_per_page'] = 10

		if 'fields' not in params:
			params['fields'] = ['id']

		resp.status = HTTP_200
		resp.body = json.encode(searchSkillModel().search(**params))

	def _post(self, container):
		req = container.req
		resp = container.resp
		"""Handles POST requests"""
		self.__validateHttpPost(req)

		# this is valid request
		appResponce = {}

		resp.status = HTTP_200  # This is the default status

		if False:
			#exists in cache
			#increament cache count
			pass
		else:
			# create model object
			search_skill_model = searchSkillModel()
			appResponce["result"] = search_skill_model.upsertSearchKeyword(req.body["search_word"], 1)

		appResponce["acknowledge"] = True
		resp.body = json.encode(appResponce)

	# function to handle all validation
	def __validateHttpPost(self, req):
		# data validation
		appResponce = {}
		if("search_word" not in req.body or (not isinstance(req.body["search_word"], str)) or req.body["search_word"] == ""):
			appResponce["message"] = "Please provide search word"
			raise appException.clientException_400(appResponce)

	def _put(self, container, uid):
		req = container.req
		resp = container.resp

		self.__validateHttpPut(req, uid)

		appResponce = {}

		search_skill_detail = self._getFilteredRequestData(req, ["assigned_to", "search_count", "status"])
		search_skill_model = searchSkillModel()
		appResponce['result'] = search_skill_model.updateSearchSkill(uid, search_skill_detail)
		appResponce["acknowledge"] = True

		resp.status = HTTP_200

		resp.body = json.encode(appResponce)


	def __validateHttpPut(self, req, uid):
		appResponce = {}

		if not "assigned_to" in req.body and not "search_count" in req.body and not "status" in req.body:
			appResponce["search_skill_id"] = 'Please provide information to update'
		else:
			if 'assigned_to' in req.body and not isinstance(req.body['assigned_to'], int):
				appResponce["assigned_to"] = 'Please provide valid admin user id'
			if 'search_count' in req.body and not isinstance(req.body['search_count'], int):
				appResponce["search_count"] = 'Please provide valid search count'
			if 'status' in req.body and (not isinstance(req.body['status'], str) or req.body['status'] not in ['invalid', 'valid', 'pending']):
				appResponce["status"] = 'Please provide valid status - invalid, valid, pending'
		if appResponce:
			raise appException.clientException_400(appResponce)

		# database level validation goes here
		search_skill_model = searchSkillModel()

		if not search_skill_model.ifSkillAlreadyExists(uid):
			self.raise404()


	def _put1(self, container, uid):
		req = container.req
		resp = container.resp
		"""Handles POST requests"""
		self.__validateHttpPut1(req, uid)

		appResponce = {}

		resp.status = HTTP_200  # This is the default status

		if req.body["status"] == "invalid":
			search_skill_model = searchSkillModel()
			appResponce["result"] = search_skill_model.markSearchSkillInvalid(uid)
		else:
			search_skill_model = searchSkillModel()
			if "skill_synonym_id" in req.body:
				search_skill_detail = search_skill_model.getSearchSkillDetailFromId(uid)
				# insert in skill synonym
				skill_synonym_model = skillSynonymModel()
				appResponce["result"] = skill_synonym_model.createSynonymFromSearchSkill(search_skill_detail,req.body["languages"],req.body["skill_synonym_id"])
			else:
				#create new parent skill and mark entry in skill_synonym
				arrLang = self.getAllLangs()

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
				appResponce["result"] = skill_parent_model.createParentSkillFromSearchSkill(params,search_skill_detail)

		resp.body = json.encode(appResponce)


	# function to handle all validation
	def __validateHttpPut1(self, req, uid):
		self.__commonPreDBValidation1(req)
		self.__commonPostDBValidation1(req, uid)

	def __commonPreDBValidation1(self, req, uid):
		# data validation
		appResponce = {}

		if("status" not in req.body or req.body["status"] == ""):
			appResponce["status"] = "Please provide search word status - valid or invalid"
		elif req.body["status"] != "valid" and req.body["status"] != "invalid":
			appResponce["status"] = "Please provide correct status - valid or invalid"
		elif req.body["status"] == "valid":
			arrLang = self.getAllLangs()

			if "skill_synonym_id" not in req.body and "all_langs" not in req.body:
				appResponce["skill_synonym_id"] = "Please provide new skill details or synonym for search skill"
			elif "skill_synonym_id" in req.body:
				if not isinstance(req.body["skill_synonym_id"], int):
					appResponce["skill_synonym_id"] = "Please provide valid skill synonym"

				if("languages" not in req.body or not isinstance(req.body["languages"], list) or len(req.body["languages"]) == 0):
					appResponce["languages"] = "Please provide languages for skill"
				else:
					arrInvalidLangs = [item for item in req.body["languages"] if not isinstance(item, str) or item not in arrLang]
					if arrNotFoundLang:
						appResponce["languages"] = "Invalid languages found - " + (",".join(arrInvalidLangs))

			elif "all_langs" in req.body:
				if isinstance(req.body["all_langs"], dict):
					arrNotFoundLang = [item for item in arrLang if item not in req.body["all_langs"] or (not isinstance(req.body["all_langs"][item], str)) or req.body["all_langs"][item] == ""]
					if arrNotFoundLang:
						appResponce["all_langs"] = "Please provide skill values for languages - " + (",".join(arrNotFoundLang))
				else:
					appResponce["all_langs"] = "Please provide valid languages for new skill"

				if "skill_info" in req.body and (not isinstance(req.body["skill_info"], str)):
					appResponce["skill_info"] = "Please provide valid information of new skill"

				if "skill_icon_path" in req.body and (not isinstance(req.body["skill_icon_path"], str)):
					appResponce["skill_icon_path"] = "Please provide valid icon path of new skill"

		if appResponce:
			raise appException.clientException_400(appResponce)

	def __commonPostDBValidation1(self, req, uid):
		appResponce = {}
		# database level validation goes here
		search_skill_model = searchSkillModel()

		if not search_skill_model.ifSkillAlreadyExists(uid):
			appResponce["search_skill_id"] = "Please provide valid search skill"

		skill_synonym_model = skillSynonymModel()
		if "skill_synonym_id" in req.body:
			if not skill_synonym_model.ifValidSkillNameExists(req.body["skill_synonym_id"]):
				appResponce["skill_synonym_id"] = "Please provide valid skill synonym"
		else:
			arrSearchSkill = [req.body["all_langs"][lang] for lang in req.body["all_langs"]];
			if not search_skill_model.ifValidLangProvidedForSearchSkill(req.body["search_skill_id"],arrSearchSkill):
				appResponce["all_langs"] = "Please provide valid Language for search skill!"
			else:
				arrSynonyms = skill_synonym_model.getSkillSynonymsByName(arrSearchSkill);
				if arrSynonyms:
					appResponce["all_langs"] = "Skill synonyms already present in system! - " + (",".join(arrSynonyms))

		if appResponce:
			raise appException.clientException_400(appResponce)








class saveSearchSkill(baseController):

	def __init__(self):
		self.__path = "/save-search-skill/"

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

		appResponce["woking"] = "fine"
		appResponce["body"] = req.body

		if False:
			#exists in cache
			#increament cache count
			pass
		else:
			# create model object
			search_skill_model = searchSkillModel()
			skill_status = search_skill_model.getSearchSkillStatus(req.body["search_word"])
			if skill_status:
				if skill_status == "pending" :
					# set cache count to 1
					appResponce["result"] = search_skill_model.increaseSearchCount(req.body["search_word"], 1)
			else:
				appResponce["result"] = search_skill_model.insertNewSearchKeyWord(req.body["search_word"])

		resp.body = json.encode(appResponce)

	# function to handle all validation
	def __validateHttpPost(self, req):
		# token validation
		self.validateHTTPRequest(req)

		# data validation
		appResponce = {}
		if("search_word" not in req.body or (not isinstance(req.body["search_word"], str)) or req.body["search_word"] == ""):
			appResponce["message"] = "Please provide search word"
			raise appException.clientException_400(appResponce)


class searchSkillStatus(baseController):

	def __init__(self):
		self.__path = "/search-skill-status/"

	def getPath(self):
		return self.__path

	def post(self, req, resp):
		"""Handles POST requests"""
		self.__validateHttpPost(req)

		appResponce = {}

		resp.status = HTTP_200  # This is the default status

		if req.body["status"] == "invalid":
			search_skill_model = searchSkillModel()
			appResponce["result"] = search_skill_model.markSearchSkillInvalid(req.body["search_skill_id"])
		else:
			search_skill_model = searchSkillModel()
			if "skill_synonym_id" in req.body:
				search_skill_detail = search_skill_model.getSearchSkillDetailFromId(req.body["search_skill_id"])
				# insert in skill synonym
				skill_synonym_model = skillSynonymModel()
				appResponce["result"] = skill_synonym_model.createSynonymFromSearchSkill(search_skill_detail,req.body["languages"],req.body["skill_synonym_id"])
			else:
				#create new parent skill and mark entry in skill_synonym
				arrLang = self.getAllLangs()

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
				appResponce["result"] = skill_parent_model.createParentSkillFromSearchSkill(params,search_skill_detail)

		resp.body = json.encode(appResponce)


	# function to handle all validation
	def __validateHttpPost(self, req):
		# token validation
		self.validateHTTPRequest(req)

		# data validation
		appResponce = {}
		if("search_skill_id" not in req.body or req.body["search_skill_id"] == "" or (not isinstance(req.body["search_skill_id"], int))):
			appResponce["search_skill_id"] = "Please provide valid search skill"
		if("status" not in req.body or req.body["status"] == ""):
			appResponce["status"] = "Please provide search word status - valid or invalid"
		elif req.body["status"] != "valid" and req.body["status"] != "invalid":
			appResponce["status"] = "Please provide correct status - valid or invalid"
		elif req.body["status"] == "valid":
			arrLang = self.getAllLangs()

			if "skill_synonym_id" not in req.body and "all_langs" not in req.body:
				appResponce["skill_synonym_id"] = "Please provide new skill details or synonym for search skill"
			elif "skill_synonym_id" in req.body:
				if not isinstance(req.body["skill_synonym_id"], int):
					appResponce["skill_synonym_id"] = "Please provide valid skill synonym"

				if("languages" not in req.body or not isinstance(req.body["languages"], list) or len(req.body["languages"]) == 0):
					appResponce["languages"] = "Please provide languages for skill"
				else:
					arrInvalidLangs = [item for item in req.body["languages"] if not isinstance(item, str) or item not in arrLang]
					if arrNotFoundLang:
						appResponce["languages"] = "Invalid languages found - " + (",".join(arrInvalidLangs))

			elif "all_langs" in req.body:
				if isinstance(req.body["all_langs"], dict):
					arrNotFoundLang = [item for item in arrLang if item not in req.body["all_langs"] or (not isinstance(req.body["all_langs"][item], str)) or req.body["all_langs"][item] == ""]
					if arrNotFoundLang:
						appResponce["all_langs"] = "Please provide skill values for languages - " + (",".join(arrNotFoundLang))
				else:
					appResponce["all_langs"] = "Please provide valid languages for new skill"

				if "skill_info" in req.body and (not isinstance(req.body["skill_info"], str)):
					appResponce["skill_info"] = "Please provide valid information of new skill"

				if "skill_icon_path" in req.body and (not isinstance(req.body["skill_icon_path"], str)):
					appResponce["skill_icon_path"] = "Please provide valid icon path of new skill"

		if appResponce:
			raise appException.clientException_400(appResponce)
		else:
			# database level validation goes here
			if "search_skill_id" in req.body:
				search_skill_model = searchSkillModel()
				skill_exists = search_skill_model.ifSkillAlreadyExists(req.body["search_skill_id"])
				if not skill_exists:
					appResponce["search_skill_id"] = "Please provide valid search skill"

			skill_synonym_model = skillSynonymModel()
			if "skill_synonym_id" in req.body:
				if not skill_synonym_model.ifValidSkillNameExists(req.body["skill_synonym_id"]):
					appResponce["skill_synonym_id"] = "Please provide valid skill synonym"
			else:
				arrSearchSkill = [req.body["all_langs"][lang] for lang in req.body["all_langs"]];
				if not search_skill_model.ifValidLangProvidedForSearchSkill(req.body["search_skill_id"],arrSearchSkill):
					appResponce["all_langs"] = "Please provide valid Language for search skill!"
				else:
					arrSynonyms = skill_synonym_model.getSkillSynonymsByName(arrSearchSkill);
					if arrSynonyms:
						appResponce["all_langs"] = "Skill synonyms already present in system! - " + (",".join(arrSynonyms))

			if appResponce:
				raise appException.clientException_400(appResponce)