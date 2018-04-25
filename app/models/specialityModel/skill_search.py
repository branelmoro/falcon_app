# always extend your model from base_model
# always give model class name same as model name
from ..base_model import baseModel

class skillSearchModel(baseModel):
	"""entire code goes here"""

	def ifSkillAlreadyExists(self,search_skill_id):
		qry = """
			SELECT exists(
				SELECT id
				FROM speciality.search_skill
				WHERE id = %s
			);
		"""
		resultCursor = self.pgSlave().query(qry,[search_skill_id])
		result = resultCursor.getOneRecord()
		return result[0]

	def getSearchSkillStatus(self,search_skill_name):
		qry = """
			SELECT status
			FROM speciality.search_skill
			WHERE search_word = %s
			LIMIT 1;
		"""
		resultCursor = self.pgSlave().query(qry,[search_skill_name])
		result = resultCursor.getOneRecord()
		if result is not None:
			return result[0]
		else:
			return False

	def insertNewSearchKeyWord(self,search_skill_name):
		qry = """INSERT INTO speciality.search_skill (search_word, search_count) values (%s,%s);"""
		resultCursor = self.pgMaster().query(qry, [search_skill_name, 1])
		return resultCursor.getStatusMessage()

	def increaseSearchCount(self,search_skill_name, count):
		qry = """UPDATE speciality.search_skill SET search_count = search_count + %s WHERE search_word = %s;"""
		resultCursor = self.pgMaster().query(qry, [count, search_skill_name])
		return resultCursor.getStatusMessage()

	def markSearchSkillInvalid(self, search_skill_id):
		qry = """UPDATE speciality.search_skill SET status = %s WHERE id = %s;"""
		resultCursor = self.pgMaster().query(qry, ["invalid", search_skill_id])
		return resultCursor.getStatusMessage()

	def getSearchSkillDetailFromId(self,search_skill_id):
		qry = """
			SELECT *
			FROM speciality.search_skill
			WHERE id = %s;
		"""
		resultCursor = self.pgSlave().query(qry,[search_skill_id])
		result = resultCursor.getOneRecord()
		columns = resultCursor.getColumns()
		return {k:result[columns[k]] for k in columns}

	def getSearchSkillDetailFromSearchWord(self,search_words):
		values = '%s,'*(len(search_words) - 1) + '%s'
		qry = """
			SELECT id, search_word, search_count
			FROM speciality.search_skill
			WHERE search_word in ("""+values+""");
		"""
		resultCursor = self.pgSlave().query(qry,search_words)
		result = resultCursor.getAllRecords()
		columns = resultCursor.getColumns()
		return {
			"columns":columns,
			"records":result
		}

	def ifValidLangProvidedForSearchSkill(self,search_skill_id,skill_words):
		params = [search_skill_id]
		params.extend(skill_words)
		qry = """
			SELECT exists(
				SELECT id
				FROM speciality.search_skill
				WHERE id = %s AND search_word in ("""+('%s,'*(len(skill_words)-1))+"""%s)
			);
		"""
		resultCursor = self.pgSlave().query(qry,params)
		result = resultCursor.getOneRecord()
		return result[0]
