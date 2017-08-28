from datetime import datetime
# always extend your model from base_model
# always give model class name same as model name
from ..base_model import baseModel

from . import oauth2ScopeModel

class resource(baseModel):
	"""entire code goes here"""

	def createNewResource(self, data):
		qry = """INSERT INTO oauth2.resource (resource_path, resource_info) values (%s,%s);"""
		resultCursor = self.pgMaster().query(qry, [data["resource_path"], data["resource_path"]])
		return resultCursor.getStatusMessage()

	def updateResource(self, data):
		qry = """UPDATE oauth2.resource set resource_path = %s, resource_info = %s where id = %s and is_editable = %s;"""
		resultCursor = self.pgMaster().query(qry, [data["resource_path"], data["resource_path"], data["resource_id"], True])
		return resultCursor.getStatusMessage()

	def deleteResource(self, data):
		dbTansaction = self.pgTransaction()
		qry = """DELETE FROM oauth2.resource where id = %s and is_editable = %s;"""
		resultCursor = dbTansaction.query(qry, [data["resource_id"], True])
		if True:
			# remove from scopes
			scope_model = oauth2ScopeModel()
			scope_model.deleteResourceFromScope(data["resource_id"])
		dbTansaction.commit()
		return resultCursor.getStatusMessage()

	def ifValidResourcesExists(self, ids):
		values = "%s,"*(len(ids)-1) + "%s"
		qry = """
			SELECT count(id) as cnt
			FROM oauth2.resource
			WHERE id in ("""+values+""");
		"""
		resultCursor = self.pgSlave().query(qry,ids)
		result = resultCursor.getOneRecord()
		return (len(ids) == result[0])

	def getResourcePathById(self, id):
		qry = """
			SELECT resource_path
			FROM oauth2.resource
			WHERE id = %s;
		"""
		resultCursor = self.pgSlave().query(qry,[id])
		result = resultCursor.getOneRecord()
		if result:
			return result[0]
		else:
			return None

	def ifResourcePathAlreadyExists(self, path, not_id=None):
		params = [path]
		strNotId = ""
		if not_id is not None:
			params.append(not_id)
			strNotId = " and id != %s"

		qry = """
			SELECT exists(
				SELECT id
				FROM oauth2.resource
				WHERE resource_path = %s"""+strNotId+"""
			);
		"""
		resultCursor = self.pgSlave().query(qry,params)
		result = resultCursor.getOneRecord()
		return result[0]

	def ifResourceIdExists(self,id):
		qry = """
			SELECT exists(
				SELECT id
				FROM oauth2.resource
				WHERE id = %s
			);
		"""
		resultCursor = self.pgSlave().query(qry,[id])
		result = resultCursor.getOneRecord()
		return result[0]

	def ifResourceEditable(self,id):
		qry = """
			SELECT is_editable
			FROM oauth2.resource
			WHERE id = %s;
		"""
		resultCursor = self.pgSlave().query(qry,[id])
		result = resultCursor.getOneRecord()
		if result:
			return result[0]
		else:
			return None