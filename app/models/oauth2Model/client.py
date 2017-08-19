# always extend your model from base_model
# always give model class name same as model name
from ..base_model import baseModel

class client(baseModel):
	"""entire code goes here"""

	def get_user_type_scope(self, client_id, client_secret):
		qry = """
			SELECT user_type, scope
			FROM oauth2.client
			WHERE client_id = %s AND client_secret = %s;
		"""
		resultCursor = self.pgSlave().query(qry,[client_id, client_secret])
		result = resultCursor.getOneRecord()
		if(result):
			return result
		else:
			return False
