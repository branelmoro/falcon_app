# always extend your model from base_model
# always give model class name same as model name
from ..base_model import baseModel

class client(baseModel):
	"""entire code goes here"""

	def get_user_type_scope(self, app_id, client_secret):
		qry = """
			SELECT user_type, scope
			FROM oauth2.client
			WHERE app_id = %s AND client_secret = %s;
		"""
		resultCursor = self.pgSlave().query(qry,[app_id, client_secret])
		result = resultCursor.getOneRecord()
		if(result):
			return result
		else:
			return False

	def ifClientIdExists(self, id):
		qry = """
			SELECT exists(
				SELECT id
				FROM oauth2.client
				WHERE id = %s
			);
		"""
		resultCursor = self.pgSlave().query(qry,[id])
		result = resultCursor.getOneRecord()
		return result[0]

	def ifClientEditable(self, id):
		qry = """
			SELECT exists(
				SELECT id
				FROM oauth2.client
				WHERE id = %s and is_editable = %s
			);
		"""
		resultCursor = self.pgSlave().query(qry,[id, True])
		result = resultCursor.getOneRecord()
		return result[0]

	def ifAppIdExists(self, app_id, not_id=None):
		param = [app_id]
		strNotId = ""
		if not_id is not None:
			param.append(not_id)
			strNotId = " and id != %s"

		qry = """
			SELECT exists(
				SELECT id
				FROM oauth2.client
				WHERE app_id = %s """+strNotId+"""
			);
		"""
		resultCursor = self.pgSlave().query(qry,param)
		result = resultCursor.getOneRecord()
		return result[0]

	def createClient(self, client_detail):
		dbObj = self.pgMaster()
		qry = """
			INSERT INTO oauth2.client (
				app_id,
				app_secret,
				scope,
				user_type,
				last_edit_time
			) VALUES (%s, %s, %s::int[], %s, %s);
		"""
		resultCursor = dbObj.query(qry, [client_detail["app_id"], client_detail["app_secret"], client_detail["scope"], client_detail["user_type"], datetime.now()])
		# end transaction
		return resultCursor.getStatusMessage()

	def updateClient(self, client_detail):

		params = []
		listSet = []

		fieldList = ["app_id", "app_secret", "user_type"]
		for i in fieldList:
			if i in client_detail:
				listSet.append(i + " = %s")
				params.append(client_detail[i])

		if "scope" in client_detail:
			listSet.append("scope = %s::smallint[]")
			params.append(client_detail["scope"])

		listSet.append("last_edit_time = %s")
		params.extend([datetime.now(), client_detail["client_id"], True])

		qry = """UPDATE oauth2.client set """ + (','.join(listSet)) + """ where id = %s and is_editable = %s;"""

		# print(qry)
		dbObj = self.pgMaster()
		resultCursor = dbObj.query(qry, params)
		# end transaction
		return resultCursor.getStatusMessage()

	def deleteClient(self, id):
		dbObj = self.pgMaster()
		qry = """
			DELETE FROM oauth2.client WHERE id = %s and is_editable = %s;
		"""
		resultCursor = dbObj.query(qry, [id, True])
		# end transaction
		return resultCursor.getStatusMessage()


	def deleteScopeFromClient(self, scope_id, dbObj = None):
		if dbObj is None:
			dbObj = self.pgMaster()

		qry = """
			UPDATE oauth2.client
			SET scope = array_remove(scope, %s::smallint)
			WHERE %s::smallint = ANY(scope);
		"""
		resultCursor = dbObj.query(qry, [scope_id, scope_id])
		# end transaction

		return resultCursor.getStatusMessage()