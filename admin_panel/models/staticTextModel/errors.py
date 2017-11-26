from datetime import datetime
# always extend your model from base_model
# always give model class name same as model name
from ..base_model import baseModel
# import uwsgi
# uwsgi.reload()


class errors(baseModel):
	"""entire code goes here"""

	def getAllErrors(self):
		qry = """
			SELECT id, english, hindi, marathi, gujarati, malayalam, bengali, oriya, tamil, telugu, panjabi, urdu, chinese_simplified, chinese_traditional, arabic, russian, portuguese, japanese, german, korean, french, turkish, italian, polish, ukrainian, persian, romanian, serbian, croatian, thai, dutch, amharic, catalan, danish, greek, spanish, estonian, finnish, armenian, khmer, kannada, malay, nepali, norwegian, slovak, albanian, swedish, tagalog
			FROM static_text.errors;
		"""
		resultCursor = self.pgSlave().query(qry,[])

		result = resultCursor.getAllRecords()
		columns = resultCursor.getColumns()

		data = []
		for i in result:
			data.append({k:i[columns[k]] for k in columns})
		
		return data

	def ifErrorIdExists(self, id):
		qry = """
			SELECT exists(
				SELECT id
				FROM static_text.errors
				WHERE id = %s
			);
		"""
		resultCursor = self.pgSlave().query(qry,[id])
		result = resultCursor.getOneRecord()
		return result[0]

	def ifErrorEditable(self, id):
		qry = """
			SELECT exists(
				SELECT id
				FROM static_text.errors
				WHERE id = %s and is_editable = %s
			);
		"""
		resultCursor = self.pgSlave().query(qry,[id, True])
		result = resultCursor.getOneRecord()
		return result[0]

	def ifEnglishErrorExists(self, english, not_id=None):
		param = [english]
		strNotId = ""
		if not_id is not None:
			param.append(not_id)
			strNotId = " and id != %s"

		qry = """
			SELECT exists(
				SELECT id
				FROM static_text.errors
				WHERE english = %s """+strNotId+"""
			);
		"""
		resultCursor = self.pgSlave().query(qry,param)
		result = resultCursor.getOneRecord()
		return result[0]

	def createError(self, error_detail):
		dbObj = self.pgMaster()
		values = '%s,'*(len(error_detail) - 1) + '%s'
		fieldList = list(error_detail)
		params = [error_detail[field] for field in fieldList]
		params.extend([datetime.now()])
		values = values + ',%s'
		qry = """
			INSERT INTO static_text.errors (
				""" + (','.join(fieldList)) + """, last_edit_time
			) VALUES ("""+ values +""");
		"""
		resultCursor = dbObj.query(qry, params)
		# end transaction
		return resultCursor.getStatusMessage()

	def updateError(self, error_detail):

		params = []
		listSet = []
		error_id = error_detail["error_id"]

		del error_detail["error_id"]

		fieldList = list(error_detail)
		for i in fieldList:
			listSet.append(i + " = %s")
			params.append(error_detail[i])

		listSet.append("last_edit_time = %s")
		params.extend([datetime.now(), error_id, True])

		qry = """UPDATE static_text.errors set """ + (','.join(listSet)) + """ where id = %s and is_editable = %s;"""

		# print(qry)
		dbObj = self.pgMaster()
		resultCursor = dbObj.query(qry, params)
		# end transaction
		return resultCursor.getStatusMessage()

	def deleteError(self, id):
		dbObj = self.pgMaster()
		qry = """
			DELETE FROM static_text.errors WHERE id = %s and is_editable = %s;
		"""
		resultCursor = dbObj.query(qry, [id, True])
		# end transaction
		return resultCursor.getStatusMessage()