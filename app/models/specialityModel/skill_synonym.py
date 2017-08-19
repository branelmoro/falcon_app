from datetime import datetime
# always extend your model from base_model
# always give model class name same as model name
from ..base_model import baseModel

class skillSynonymModel(baseModel):
	"""entire code goes here"""

	def ifValidSkillNameExists(self,skill_synonym_id):
		qry = """
			SELECT exists(
				SELECT id
				FROM speciality.skill_synonym
				WHERE id = %s AND skill_parent_id IS NOT null
			);
		"""
		resultCursor = self.pgSlave().query(qry,[skill_synonym_id])
		result = resultCursor.getOneRecord()
		return result[0]

	def ifPendingSkillNameExists(self,skill_synonym_id):
		qry = """
			SELECT exists(
				SELECT id
				FROM speciality.skill_synonym
				WHERE id = %s AND skill_parent_id IS null
			);
		"""
		resultCursor = self.pgSlave().query(qry,[skill_synonym_id])
		result = resultCursor.getOneRecord()
		return result[0]

	def ifSkillSynonymAlreadyExists(self,skill_synonym_word):
		qry = """
			SELECT exists(
				SELECT id
				FROM speciality.skill_synonym
				WHERE skill_name = %s
			);
		"""
		resultCursor = self.pgSlave().query(qry,[skill_synonym_id])
		result = resultCursor.getOneRecord()
		return result[0]

	def createSynonymFromSearchSkill(self, search_skill, languages, skill_synonym_id):

		# start transaction
		dbTansaction = self.pgTransaction()

		resultCursor = self.deleteSearchSkillById(search_skill["id"],dbTansaction)

		skill_detail = {
			"skill_name" : search_skill["skill_name"],
			"languages" : languages,
			"search_count" : search_skill["search_count"],
			"assigned_to" : search_skill["assigned_to"]
		}

		response = self.createSynonymForSkill(search_skill, skill_synonym_id, dbTansaction)

		# end transaction
		dbTansaction.commit()

		return response

	def deleteSearchSkillById(self,search_skill_id,dbTansaction=None):
		if dbTansaction is None:
			dbTansaction = self.pgMaster()

		#delete from into skill synonym
		qry = """
			DELETE FROM speciality.search_skill WHERE id = %s
		"""
		return dbTansaction.query(qry, [search_skill_id])


	def createSynonymForSkill(self, synonym_skill_detail, skill_synonym_id, dbObj=None):

		if dbObj is None:
			dbObj = self.pgMaster()

		if "search_count" not in synonym_skill_detail:
			synonym_skill_detail["search_count"] = 0;

		qry = """
			INSERT INTO speciality.search_synonym (
				skill_parent_id,
				skill_name,
				written_language,
				profile_exists,
				search_count,
				assigned_to,
				status,
				skill_icon_path,
				last_edit_time
			) SELECT skill_parent_id,
				%s as skill_name,
				%s::lang[] as written_language,
				FALSE as profile_exists,
				%s as search_count,
				%s as assigned_to,
				status,
				skill_icon_path,
				%s as last_edit_time
				FROM search_synonym
				WHERE id = %s;
		"""
		resultCursor = dbObj.query(qry, [synonym_skill_detail["skill_name"], synonym_skill_detail["languages"], synonym_skill_detail["search_count"], synonym_skill_detail["assigned_to"], datetime.now(), skill_synonym_id])
		# end transaction
		return resultCursor.getStatusMessage()

	def getSkillSynonymsByName(self,skill_synonyms):
		values = "%s,"*(len(skill_synonyms)-1) + "%s"
		qry = """
			SELECT skill_name
			FROM speciality.skill_synonym
			WHERE skill_name IN ("""+values+""")
		"""
		resultCursor = self.pgSlave().query(qry,skill_synonyms)
		result = resultCursor.getAllRecords()
		return [result[i][0] for i in result]


	def ifValidLangProvidedForSkillSynonym(self,skill_synonym_id,skill_words):
		params = [skill_synonym_id]
		params.extend(skill_words)
		qry = """
			SELECT exists(
				SELECT id
				FROM speciality.skill_synonym
				WHERE id = %s AND skill_name in ("""+('%s,'*(len(skill_words)-1))+"""%s)
			);
		"""
		resultCursor = self.pgSlave().query(qry,params)
		result = resultCursor.getOneRecord()
		return result[0]


	def markSkillSynonymInvalid(self, skill_synonym_id):

		# start transaction
		dbTansaction = self.pgTransaction()


		resultCursor = self.moveSkillSynonymToSearchSkill(skill_synonym_id, dbTansaction)

		#delete from skill synonym
		resultCursor = self.deleteSkillSynonymById(skill_synonym_id, dbTansaction)

		#delete skill_synonym_id from profile skills and make profile temporarily inactive where no skill mentioned


		dbTansaction.commit()
		return True


	def moveSkillSynonymToSearchSkill(self, skill_synonym_id, dbTansaction = None):
		if dbTansaction is None:
			dbTansaction = self.pgMaster()

		#insert into skill search
		qry = """
			INSERT INTO speciality.search_skill (
				search_word,
				assigned_to,
				status,
				search_count
			)  SELECT skill_name,
				assigned_to,
				%s as status,
				search_count
			FROM search_synonym
			WHERE id = %s;
		"""

		return dbTansaction.query(qry, ["invalid",skill_synonym_id])


	def createSynonymFromParentSkillSynonym(self, skill_synonym_id, languages, parent_skill_synonym_id):

		skill_parent_id = self.getSkillParentIdFromSkillSynonymId(skill_synonym_id)

		params = ['valid', languages, result[0], skill_synonym_id, datetime.now()]
		qry = """
			UPDATE speciality.search_synonym set status=%s, written_language=%s, skill_parent_id = %s, last_edit_time = %s
			WHERE id = %s
		"""
		resultCursor = self.pgMaster.query(qry, params)
		
		return resultCursor.getStatusMessage()

	def getSkillParentIdFromSkillSynonymId(self, skill_synonym_id):
		qry = """
			SELECT skill_parent_id
			FROM speciality.search_synonym
			WHERE id = %s;
		"""
		resultCursor = self.pgSlave().query(qry,[parent_skill_synonym_id])
		result = resultCursor.getOneRecord()
		return result[0]


	def getSkillSynonymDetailFromId(self,skill_synonym_id):
		qry = """
			SELECT *
			FROM speciality.search_synonym
			WHERE id = %s;
		"""
		resultCursor = self.pgSlave().query(qry,[skill_synonym_id])
		result = resultCursor.getOneRecord()
		columns = resultCursor.getColumns()
		return {k:result[columns[k]] for k in columns}

	def ifSkillLanguagesExists(self,skill_synonym_id,languages):
		qry = """
			SELECT written_language
			FROM speciality.skill_synonym
			WHERE id = %s
				AND skill_parent_id IS NOT null
				AND written_language && %s::lang[];
		"""
		resultCursor = self.pgSlave().query(qry,[skill_synonym_id,languages])
		result = resultCursor.getOneRecord()
		if(result):
			return result[0]
		else:
			return False

	def addLanguagesToSkillSynonym(self,skill_synonym_id,languages):
		qry = """
			UPDATE speciality.skill_synonym
			SET written_language = array_cat(written_language, %s::lang[]),
				last_edit_time = %s
			WHERE id = %s
				AND skill_parent_id IS NOT null
		"""
		resultCursor = self.pgMaster().query(qry,[skill_synonym_id,languages,datetime.now()])
		return resultCursor.getStatusMessage()

	def ifAlternateSkillSynonymExistsForLanguage(self,skill_synonym_id,language):

		skill_parent_id = self.getSkillParentIdFromSkillSynonymId(skill_synonym_id)

		qry = """
			SELECT count(id)
			FROM speciality.skill_synonym
			WHERE skill_parent_id = %s
				AND written_language && %s::lang[];
		"""
		resultCursor = self.pgMaster().query(qry,[skill_parent_id,[language]])
		result = resultCursor.getOneRecord()
		return (result[0] >= 2)

	def removeLanguageFromSkillSynonym(self,skill_synonym_id,language):
		qry = """
			UPDATE speciality.skill_synonym
			SET written_language = array_remove(written_language, %s),
				last_edit_time = %s
			WHERE id = %s
				AND skill_parent_id IS NOT null
		"""
		resultCursor = self.pgMaster().query(qry,[skill_synonym_id,language,datetime.now()])
		return resultCursor.getStatusMessage()

	def deleteSkillSynonymById(self,skill_synonym_id,dbTansaction=None):
		if dbTansaction is None:
			dbTansaction = self.pgMaster()

		# insert into another table marking as deleted, usefull in elasticsearch import process

		#delete from into skill synonym
		qry = """
			DELETE FROM speciality.search_synonym WHERE id = %s;
		"""
		return dbTansaction.query(qry, [skill_synonym_id])


	def removeSkillSynonymById(self,skill_synonym_id):
		
		return self.markSkillSynonymInvalid(skill_synonym_id)