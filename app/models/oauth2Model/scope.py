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

	def ifScopeNameExists(self, scope_name):
		qry = """
			SELECT exists(
				SELECT id
				FROM oauth2.scope
				WHERE scope_name = %s
			);
		"""
		resultCursor = self.pgSlave().query(qry,[scope_name])
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

	def ifScopeNameExistsInAnyOtherScope(self, scope_name, scope_id):
		qry = """
			SELECT exists(
				SELECT id
				FROM oauth2.scope
				WHERE scope_name = %s and id != %s
			);
		"""
		resultCursor = self.pgSlave().query(qry,[scope_name, scope_id])
		result = resultCursor.getOneRecord()
		return result[0]

	def createScope(self, scope_detail):
		dbObj = self.pgMaster()
		qry = """
			INSERT INTO oauth2.scope (
				scope_name,
				scope_info,
				allowed_resources,
				last_edit_time
			) VALUES (%s, %s, %s::int[], %s);
		"""
		resultCursor = dbObj.query(qry, [scope_detail["scope_name"], scope_detail["scope_info"], scope_detail["allowed_resources"], datetime.now()])
		# end transaction
		return resultCursor.getStatusMessage()


	def updateScope(self, scope_detail):
		dbObj = self.pgMaster()
		qry = """
			UPDATE oauth2.scope
			SET scope_name = %s, scope_info = %s, allowed_resources = %s::int[], last_edit_time = %s
			WHERE id = %s;
		"""
		resultCursor = dbObj.query(qry, [scope_detail["scope_name"], scope_detail["scope_info"], scope_detail["allowed_resources"], datetime.now(), scope_detail["id"]])
		# end transaction
		return resultCursor.getStatusMessage()

	def deleteScope(self, scope_id):
		dbObj = self.pgMaster()
		qry = """
			DELETE FROM oauth2.scope WHERE id = %s;
		"""
		resultCursor = dbObj.query(qry, [scope_id])
		# end transaction
		return resultCursor.getStatusMessage()