from datetime import datetime
# always extend your model from base_model
# always give model class name same as model name
from ..base_model import baseModel

from . import oauth2ScopeModel

class resource(baseModel):
	"""entire code goes here"""

	def createNewResource(self, data):
		qry = """INSERT INTO oauth2.resource (code, resource_path, resource_info) values (%s,%s,%s);"""
		resultCursor = self.pgMaster().query(qry, [data["code"], data["resource_path"], data["resource_info"]])
		return resultCursor.getStatusMessage()

	def updateResource(self, data):
		param = []
		# qry = """UPDATE oauth2.resource set resource_path = %s, resource_info = %s where id = %s and is_editable = %s;"""
		listSet = []
		if "code" in data:
			listSet.append("code = %s")
			param.append(data["code"])
		if "resource_path" in data:
			listSet.append("resource_path = %s")
			param.append(data["resource_path"])
		if "resource_info" in data:
			listSet.append("resource_info = %s")
			param.append(data["resource_info"])
		qry = """UPDATE oauth2.resource set """ + (','.join(listSet)) + """ where id = %s and is_editable = %s;"""
		listSet.append("last_edit_time = %s")
		param.extend([datetime.now(), data["resource_id"], True])
		resultCursor = self.pgMaster().query(qry, param)
		return resultCursor.getStatusMessage()

	def deleteResource(self, uid):
		resource_code = self.__getResourceFieldById('code', uid)
		dbTansaction = self.pgTransaction()
		qry = """DELETE FROM oauth2.resource where id = %s and is_editable = %s;"""
		resultCursor = dbTansaction.query(qry, [uid, True])
		if True:
			# remove from scopes
			scope_model = oauth2ScopeModel()
			scope_model.deleteResourceFromScope(resource_code)
		dbTansaction.commit()
		return resultCursor.getStatusMessage()

	def ifValidResourcesExists(self, recource_codes):
		values = "%s,"*(len(recource_codes)-1) + "%s"
		qry = """
			SELECT count(id) as cnt
			FROM oauth2.resource
			WHERE code in ("""+values+""");
		"""
		resultCursor = self.pgSlave().query(qry,recource_codes)
		result = resultCursor.getOneRecord()
		return (len(recource_codes) == result[0])

	def getResourceFieldByCode(self, field, code):
		qry = """
			SELECT """+field+"""
			FROM oauth2.resource
			WHERE code = %s;
		"""
		resultCursor = self.pgSlave().query(qry,[code])
		result = resultCursor.getOneRecord()
		if result:
			return result[0]
		else:
			return None

	def __getResourceFieldById(self, field, uid):
		qry = """
			SELECT """+field+"""
			FROM oauth2.resource
			WHERE id = %s;
		"""
		resultCursor = self.pgSlave().query(qry,[uid])
		result = resultCursor.getOneRecord()
		if result:
			return result[0]
		else:
			return None

	def getResourcePathById(self, uid):
		return self.__getResourceFieldById('resource_path', uid)

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

	def ifResourceCodeAlreadyExists(self, code, not_id=None):
		params = [code]
		strNotId = ""
		if not_id is not None:
			params.append(not_id)
			strNotId = " and id != %s"

		qry = """
			SELECT exists(
				SELECT id
				FROM oauth2.resource
				WHERE code = %s"""+strNotId+"""
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

	def ifResourceEditable(self,uid):
		return self.__getResourceFieldById('is_editable', uid)