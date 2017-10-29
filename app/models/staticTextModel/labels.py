from datetime import datetime
# always extend your model from base_model
# always give model class name same as model name
from ..base_model import baseModel
# import uwsgi
# uwsgi.reload()


class labels(baseModel):
	"""entire code goes here"""

	def getAllLabels(self):
		qry = """
			SELECT id, english, hindi, marathi, gujarati, malayalam, bengali, oriya, tamil, telugu, panjabi, urdu, chinese_simplified, chinese_traditional, arabic, russian, portuguese, japanese, german, korean, french, turkish, italian, polish, ukrainian, persian, romanian, serbian, croatian, thai, dutch, amharic, catalan, danish, greek, spanish, estonian, finnish, armenian, khmer, kannada, malay, nepali, norwegian, slovak, albanian, swedish, tagalog
			FROM static_text.labels;
		"""
		resultCursor = self.pgSlave().query(qry,[])

		result = resultCursor.getAllRecords()
		columns = resultCursor.getColumns()

		data = []
		for i in result:
			data.append({k:i[columns[k]] for k in columns})
		
		return data

	def ifLabelIdExists(self, id):
		qry = """
			SELECT exists(
				SELECT id
				FROM static_text.labels
				WHERE id = %s
			);
		"""
		resultCursor = self.pgSlave().query(qry,[id])
		result = resultCursor.getOneRecord()
		return result[0]

	def ifLabelEditable(self, id):
		qry = """
			SELECT exists(
				SELECT id
				FROM static_text.labels
				WHERE id = %s and is_editable = %s
			);
		"""
		resultCursor = self.pgSlave().query(qry,[id, True])
		result = resultCursor.getOneRecord()
		return result[0]

	def ifEnglishLabelExists(self, english, not_id=None):
		param = [english]
		strNotId = ""
		if not_id is not None:
			param.append(not_id)
			strNotId = " and id != %s"

		qry = """
			SELECT exists(
				SELECT id
				FROM static_text.labels
				WHERE english = %s """+strNotId+"""
			);
		"""
		resultCursor = self.pgSlave().query(qry,param)
		result = resultCursor.getOneRecord()
		return result[0]

	def createLabel(self, label_detail):
		dbObj = self.pgMaster()
		values = '%s,'*(len(label_detail) - 1) + '%s'
		fieldList = list(label_detail)
		params = [label_detail[field] for field in fieldList]
		params.extend([datetime.now()])
		values = values + ',%s'
		qry = """
			INSERT INTO static_text.labels (
				""" + (','.join(fieldList)) + """, last_edit_time
			) VALUES ("""+ values +""");
		"""
		resultCursor = dbObj.query(qry, params)
		# end transaction
		return resultCursor.getStatusMessage()

	def updateLabel(self, label_detail):

		params = []
		listSet = []
		label_id = label_detail["label_id"]

		del label_detail["label_id"]

		fieldList = list(label_detail)
		for i in fieldList:
			listSet.append(i + " = %s")
			params.append(label_detail[i])

		listSet.append("last_edit_time = %s")
		params.extend([datetime.now(), label_id, True])

		qry = """UPDATE static_text.labels set """ + (','.join(listSet)) + """ where id = %s and is_editable = %s;"""

		# print(qry)
		dbObj = self.pgMaster()
		resultCursor = dbObj.query(qry, params)
		# end transaction
		return resultCursor.getStatusMessage()

	def deleteLabel(self, id):
		dbObj = self.pgMaster()
		qry = """
			DELETE FROM static_text.labels WHERE id = %s and is_editable = %s;
		"""
		resultCursor = dbObj.query(qry, [id, True])
		# end transaction
		return resultCursor.getStatusMessage()