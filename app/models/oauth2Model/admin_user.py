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
