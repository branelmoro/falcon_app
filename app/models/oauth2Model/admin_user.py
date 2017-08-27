from datetime import datetime
# always extend your model from base_model
# always give model class name same as model name
from ..base_model import baseModel

class adminUser(baseModel):
	"""entire code goes here"""

	def get_user_scope(self, username, password):
		qry = """
			SELECT scope
			FROM oauth2.admin_user
			WHERE username = %s AND password = %s;
		"""
		resultCursor = self.pgSlave().query(qry,[username, password])
		result = resultCursor.getOneRecord()
		if(result):
			return result[0]
		else:
			return False

	def ifUserNameExists(self, username, not_id=None):
		param = [username]
		strNotId = ""
		if not_id is not None:
			param.append(not_id)
			strNotId = " and id != %s"

		qry = """
			SELECT exists(
				SELECT id
				FROM oauth2.admin_user
				WHERE username = %s """+strNotId+"""
			);
		"""
		resultCursor = self.pgSlave().query(qry,param)
		result = resultCursor.getOneRecord()
		return result[0]

	def ifAdminUserIdExists(self, id):
		qry = """
			SELECT exists(
				SELECT id
				FROM oauth2.admin_user
				WHERE id = %s
			);
		"""
		resultCursor = self.pgSlave().query(qry,[id])
		result = resultCursor.getOneRecord()
		return result[0]

	def ifAdminUserEditable(self, id):
		qry = """
			SELECT exists(
				SELECT id
				FROM oauth2.admin_user
				WHERE id = %s and is_editable = %s
			);
		"""
		resultCursor = self.pgSlave().query(qry,[id, True])
		result = resultCursor.getOneRecord()
		return result[0]

	def createAdminUser(self, user_detail):
		dbObj = self.pgMaster()
		qry = """
			INSERT INTO oauth2.admin_user (
				username,
				password,
				scope,
				last_edit_time
			) VALUES (%s, %s, %s::int[], %s);
		"""
		resultCursor = dbObj.query(qry, [user_detail["username"], user_detail["password"], user_detail["scope"], datetime.now()])
		# end transaction
		return resultCursor.getStatusMessage()
