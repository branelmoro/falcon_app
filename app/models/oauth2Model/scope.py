from datetime import datetime
# always extend your model from base_model
# always give model class name same as model name
from ..base_model import baseModel

class scope(baseModel):
	"""entire code goes here"""

	def getScopeNamesFromIds(self, ids):
		values = "%s,"*(len(ids)-1) + "%s"
		qry = """
			SELECT scope_name
			FROM oauth2.scope
			WHERE id in ("""+values+""");
		"""
		resultCursor = self.pgSlave().query(qry,ids)
		result = resultCursor.getAllRecords()
		return [result[i][0] for i in result]

	def ifScopeNameExists(self, scope_name, not_id=None):
		param = [scope_name]
		strNotId = ""
		if not_id is not None:
			param.append(not_id)
			strNotId = " and id != %s"

		qry = """
			SELECT exists(
				SELECT id
				FROM oauth2.scope
				WHERE scope_name = %s """+strNotId+"""
			);
		"""
		resultCursor = self.pgSlave().query(qry,param)
		result = resultCursor.getOneRecord()
		return result[0]

	def ifScopeIdExists(self, id):
		qry = """
			SELECT exists(
				SELECT id
				FROM oauth2.scope
				WHERE id = %s
			);
		"""
		resultCursor = self.pgSlave().query(qry,[id])
		result = resultCursor.getOneRecord()
		return result[0]

	def createScope(self, scope_detail):
		dbObj = self.pgMaster()
		qry = """
			INSERT INTO oauth2.scope (
				scope_name,
				scope_info,
				allowed_get,
				allowed_post,
				allowed_put,
				allowed_delete,
				last_edit_time
			) VALUES (%s, %s, %s::int[], %s::int[], %s::int[], %s::int[], %s);
		"""
		resultCursor = dbObj.query(qry, [scope_detail["scope_name"], scope_detail["scope_info"], scope_detail["allowed_get"], scope_detail["allowed_post"], scope_detail["allowed_put"], scope_detail["allowed_delete"], datetime.now()])
		# end transaction
		return resultCursor.getStatusMessage()


	def updateScope(self, scope_detail):

		params = [scope_detail["scope_name"], scope_detail["scope_info"]]

		allowedList = ["allowed_get", "allowed_post", "allowed_put", "allowed_delete"]
		strAllowed = ""
		for allowed_method in allowedList:
			if allowed_method in scope_detail:
				strAllowed = strAllowed + """
				"""+allowed_method+""" = %s::int[],"""
				params.append(scope_detail[allowed_method])

		params.extend([datetime.now(), scope_detail["id"], True])

		qry = """
			UPDATE oauth2.scope
			SET scope_name = %s,
				scope_info = %s,"""+strAllowed+"""
				last_edit_time = %s
			WHERE id = %s and is_editable = %s;
		"""
		dbObj = self.pgMaster()
		resultCursor = dbObj.query(qry, params)
		# end transaction
		return resultCursor.getStatusMessage()

	def deleteScope(self, scope_id):
		dbObj = self.pgMaster()
		qry = """
			DELETE FROM oauth2.scope WHERE id = %s and is_editable = %s;
		"""
		resultCursor = dbObj.query(qry, [scope_id, True])
		# end transaction
		return resultCursor.getStatusMessage()

	def ifValidScopesExists(self, ids):
		values = "%s,"*(len(ids)-1) + "%s"
		qry = """
			SELECT count(id) as cnt
			FROM oauth2.scope
			WHERE id in ("""+values+""");
		"""
		resultCursor = self.pgSlave().query(qry,ids)
		result = resultCursor.getOneRecord()
		return (len(ids) == result[0])

	def ifScopeEditable(self, scope_id):
		qry = """
			SELECT exists(
				SELECT id
				FROM oauth2.scope
				WHERE id = %s and is_editable = %s
			);
		"""
		resultCursor = self.pgSlave().query(qry,[scope_id, True])
		result = resultCursor.getOneRecord()
		return result[0]
