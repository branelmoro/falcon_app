from datetime import datetime
# always extend your model from base_model
# always give model class name same as model name
from ..base_model import baseModel

class skillParentModel(baseModel):
	"""entire code goes here"""

	def createParentSkillFromSkillSynonym(self, data, search_skill_details, skill_synonym_detail):
		# start transaction
		dbTansaction = self.pgTransaction()

		skill_parent_id = self.createParentSkillFromSearchSkill(data, search_skill_details, dbTansaction)

		languages = []

		for lang in data:
			if data[lang] == skill_synonym_detail["skill_name"]:
				languages.append(lang)

		params = ['valid', languages, skill_parent_id, skill_synonym_id]
		qry = """
			UPDATE speciality.search_synonym set status=%s, written_language=%s, skill_parent_id = %s
			WHERE id = %s
		"""
		resultCursor = self.pgMaster.query(qry, params)

		# end transaction
		dbTansaction.commit()
		
		return skill_parent_id


	def createParentSkillFromSearchSkill(self, data, search_skill_details, dbTansaction=None):

		# start transaction
		blnCommit = True
		if dbTansaction is None:
			dbTansaction = self.pgTransaction()
			blnCommit = False

		searchSkillIds = [row[search_skill_details["columns"]["id"]] for row in search_skill_details["records"]]

		values = '%s,'*(len(searchSkillIds) - 1) + '%s'

		qry = """
			DELETE FROM speciality.search_skill WHERE id in ("""+values+""")
		"""

		resultCursor = dbTansaction.query(qry,searchSkillIds)

		queryData = self.__getInsertQuery_Params(data)

		resultCursor = dbTansaction.query(queryData['query'], queryData['params'])

		insertId = resultCursor.getLastInsertId();

		self.__createSkillSynonymsFromParentSkill(insertId, data, search_skill_details, dbTansaction)

		# msg = resultCursor.getStatusMessage()

		# end transaction
		if blnCommit:
			dbTansaction.commit()

		return insertId


	def __getInsertQuery_Params(self, data):

		arrColumns = [column for column in data]
		columns = (",".join(arrColumns)) + ',last_edit_time'

		values = ('%s,'*(len(data)-1)) + '%s,%s'
		params = [data[item] for item in data]

		params.append(datetime.now())

		qry = """
			INSERT INTO speciality.skill_parent ("""+ columns +""") VALUES ("""+ values +""") RETURNING id;
		"""

		return {
			"query" : qry,
			"params" : params
		}

	def __createSkillSynonymsFromParentSkill(self, parent_skill_id, data, search_skill_details, dbTansaction):
		arrLang = ['english','hindi','marathi','gujarati','malayalam','bengali','oriya','tamil','telugu','panjabi','urdu','chinese_simplified','chinese_traditional','mandarin_chinese','arabic','russian','portuguese','japanese','german','korean','french','turkish','italian','polish','ukrainian','persian','romanian','serbian','croatian','thai','dutch','amharic','catalan','danish','greek','spanish','estonian','finnish','armenian','khmer','kannada','malay','nepali','norwegian','slovak','albanian','swedish','tagalog']

		search_skill_count = {row[search_skill_details["columns"]["search_word"]]:row[search_skill_details["columns"]["search_count"]] for row in search_skill_details["records"]}

		arrValues = []

		params = []

		skillArr = {}
		for lang in data:
			if lang in arrLang:
				if data[lang] in skillArr:
					skillArr[data[lang]].append(lang)
				else:
					skillArr[data[lang]] = [lang]

		for skill_name in skillArr:
			if skill_name in search_skill_count:
				search_count = search_skill_count[skill_name]
			else:
				search_count = 0

			assigned_to = 0
			params.append(parent_skill_id)
			params.append(skill_name)
			params.append(skillArr[skill_name])
			params.append(search_count)
			params.append(assigned_to)
			params.append("valid")
			params.append(datetime.now())

			if "skill_icon_path" in data:
				params.append(data["skill_icon_path"])
				arrValues.append('(%s,%s,%s::lang[],false,%s,%s,%s,%s,%s)')
			else:
				arrValues.append('(%s,%s,%s::lang[],false,%s,%s,%s,%s)')


		if "skill_icon_path" in data:
			strColumns = 'skill_parent_id,skill_name,written_language,profile_exists,search_count,assigned_to,status,skill_icon_path,last_edit_time'
		else:
			strColumns = 'skill_parent_id,skill_name,written_language,profile_exists,search_count,assigned_to,status,last_edit_time'

		qry = """
			INSERT INTO speciality.skill_synonym ("""+strColumns+""") VALUES """+ (",".join(arrValues)) +""";
		"""

		resultCursor = dbTansaction.query(qry,params)

		return resultCursor.getStatusMessage()