import math
# always extend your model from base_model
# always give model class name same as model name
from ..base_model import baseModel

class searchSkillModel(baseModel):
	"""entire code goes here"""

	def search(self, page, count_per_page, **criteria):

		params = []
		qry_condition = ''' FROM speciality.search_skill '''

		count_query = '''SELECT count(id) as cnt ''' + qry_condition

		resultCursor = self.pgSlave().query(count_query, params)
		result = resultCursor.getOneRecord()
		total_count = result[0]


		search_result = {
			'total' : total_count,
			'page' : page,
			'count_per_page':count_per_page,
			'found' : 0,
			'records' : []
		}

		if total_count > 0 and page <= math.ceil(total_count/count_per_page):

			# for i in criteria['fields']:
			# 	params.insert(0, i)
			# search_query = '''SELECT ''' + ('%s, '*(len(criteria['fields']) - 1) + '%s' ) + qry_condition + ''' LIMIT %s OFFSET %s'''
			search_query = '''SELECT ''' + (', '.join(criteria['fields'])) + qry_condition + ''' LIMIT %s OFFSET %s'''
			params.append(count_per_page)
			offset = (page - 1) * count_per_page
			params.append(offset)

			resultCursor = self.pgSlave().query(search_query, params)
			# result = resultCursor.getAllRecords()
			columns = resultCursor.getColumns()

			search_result['records'] = [{k:record[columns[k]] for k in columns} for record in resultCursor.getAllRecords()]
			# search_result['records'] = result
			search_result['found'] = len(search_result['records'])

		return search_result


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

	def updateSearchSkill(self, uid, data):
		params = []
		updateFields = []
		if 'search_count' in data:
			updateFields.append('search_count = search_count + %s')
			params.append(data['search_count'])
		if 'assigned_to' in data:
			updateFields.append('assigned_to = %s')
			params.append(data['assigned_to'])
		if 'status' in data:
			updateFields.append('status = %s')
			params.append(data['status'])
		qry = 'UPDATE speciality.search_skill SET '+(', '.join(updateFields))+' WHERE id = %s;'
		params.append(uid)
		resultCursor = self.pgMaster().query(qry, params)
		return resultCursor.getStatusMessage()

	def upsertSearchKeyword(self,search_skill_name, count):
		qry = '''
		INSERT INTO speciality.search_skill as e (search_word, search_count, last_edit_time) values (%s, %s, now())
		ON CONFLICT (search_word)
			DO UPDATE SET search_count = e.search_count + %s,
					last_edit_time = now();
				--WHERE status = s;
		'''
		# resultCursor = self.pgMaster().query(qry, [search_skill_name, count, count, 'pending'])
		resultCursor = self.pgMaster().query(qry, [search_skill_name, count, count])
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
