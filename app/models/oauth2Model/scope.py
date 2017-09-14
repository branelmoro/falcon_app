from datetime import datetime
# always extend your model from base_model
# always give model class name same as model name
from ..base_model import baseModel

from ...resources.redis import redis as appCache

from . import oauth2AdminUserModel
from . import oauth2ClientModel

class scope(baseModel):
	"""entire code goes here"""

	def __init__(self):
		self.__scopeKeyExpiry = 1200
		self.__accessDb = appCache("access_scopeDb");


	def __getScopeDetails(self, ids):
		values = "%s,"*(len(ids)-1) + "%s"
		qry = """
			SELECT scope_name,
				id,
				allowed_get,
				allowed_post,
				allowed_put,
				allowed_delete
			FROM oauth2.scope
			WHERE id in ("""+values+""");
		"""
		resultCursor = self.pgSlave().query(qry,ids)

		# return [list(i) for i in resultCursor.getAllRecords()]
		return resultCursor.getAllRecords()


	def getScopeNamesFromIds(self, ids):
		result = self.__getScopeDetails(ids)

		self.__addScopeToCache(result)

		return [result[i][0] for i in result]


	def __removeFromCache(self, scopekey):
		if self.__accessDb.exists(scopekey):
			self.__accessDb.delete(scopekey)


	def __storeInCache(self, scopekey, allowed_method, blnReplace = False):
		if allowed_method:
			if blnReplace or not self.__accessDb.exists(scopekey):
				self.__accessDb.sadd(scopekey, allowed_method)
			self.__accessDb.expire(scopekey, self.__scopeKeyExpiry)
		elif blnReplace:
			self.__removeFromCache(scopekey)


	def __addScopeToCache(self, result, blnReplace = False):
		for scope_detail in result:

			scope_id = str(scope_detail[1])

			self.__storeInCache(scope_id + "__GET", scope_detail[2], blnReplace)

			self.__storeInCache(scope_id + "__POST", scope_detail[3], blnReplace)

			self.__storeInCache(scope_id + "__PUT", scope_detail[4], blnReplace)

			self.__storeInCache(scope_id + "__DELETE", scope_detail[5], blnReplace)


	def __deleteScopeFromCache(self,scope_id):
		scope_id = str(scope_id)
		self.__removeFromCache(scope_id + "__GET")
		self.__removeFromCache(scope_id + "__POST")
		self.__removeFromCache(scope_id + "__PUT")
		self.__removeFromCache(scope_id + "__DELETE")


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

		insertId = resultCursor.getLastInsertId();

		self.__addScopeToCache(self.__getScopeDetails([insertId]))

		return resultCursor.getStatusMessage()


	def updateScope(self, scope_detail):

		params = []
		listSet = []

		fieldList = ["scope_name", "scope_info"]
		for i in fieldList:
			if i in scope_detail:
				listSet.append(i + " = %s")
				params.append(scope_detail[i])


		fieldList = ["allowed_get", "allowed_post", "allowed_put", "allowed_delete"]
		for i in fieldList:
			if i in scope_detail:
				listSet.append(i + " = %s::smallint[]")
				params.append(scope_detail[i])

		listSet.append("last_edit_time = %s")
		qry = """UPDATE oauth2.scope set """ + (','.join(listSet)) + """ where id = %s and is_editable = %s;"""
		params.extend([datetime.now(), scope_detail["id"], True])
		dbObj = self.pgMaster()
		resultCursor = dbObj.query(qry, params)

		self.__addScopeToCache(self.__getScopeDetails([scope_detail["id"]]), True)
		# end transaction
		return resultCursor.getStatusMessage()

	def deleteScope(self, scope_id):
		dbTansaction = self.pgTransaction()
		qry = """
			DELETE FROM oauth2.scope WHERE id = %s and is_editable = %s;
		"""
		resultCursor = dbTansaction.query(qry, [scope_id, True])

		if True:
			admin_user_model = oauth2AdminUserModel()
			admin_user_model.deleteScopeFromAdminUser(scope_id, dbTansaction)
			client_model = oauth2ClientModel()
			client_model.deleteScopeFromAdminUser(scope_id, dbTansaction)

		self.__deleteScopeFromCache(scope_id)
		dbTansaction.commit()
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

	def ifAtleastOneResourceAccessIsGiven(self, scope_id, allowed_resource):
		params = [scope_id]

		# allowed_resource = ["cardinality("+i+") > 0" for i in allowed_resource]

		allowed_resource = [i+" != %s::smallint[]" for i in allowed_resource]
		params.extend([[] for i in allowed_resource])

		qry = """
			SELECT exists(
				SELECT id
				FROM oauth2.scope
				WHERE id = %s and (""" + (' or '.join(allowed_resource)) + """)
			);
		"""

		resultCursor = self.pgSlave().query(qry,params)
		result = resultCursor.getOneRecord()
		return result[0]

	def deleteResourceFromScope(self, resource_id, dbObj = None):
		if dbObj is None:
			dbObj = self.pgMaster()

		params = [resource_id, resource_id, resource_id, resource_id]

		qry = """
			SELECT id
			FROM oauth2.scope
			WHERE %s::smallint = ANY(allowed_get)
				or %s::smallint = ANY(allowed_post)
				or %s::smallint = ANY(allowed_put)
				or %s::smallint = ANY(allowed_delete);
		"""
		resultCursor = self.pgSlave().query(qry,params)
		result = resultCursor.getAllRecords()

		ids = [result[i][0] for i in result]

		qry = """
			UPDATE oauth2.scope
			SET allowed_get = array_remove(allowed_get, %s::smallint),
				allowed_post = array_remove(allowed_post, %s::smallint),
				allowed_put = array_remove(allowed_put, %s::smallint),
				allowed_delete = array_remove(allowed_delete, %s::smallint)
			WHERE %s::smallint = ANY(allowed_get)
				or %s::smallint = ANY(allowed_post)
				or %s::smallint = ANY(allowed_put)
				or %s::smallint = ANY(allowed_delete);
		"""
		params = params + params
		resultCursor = dbObj.query(qry, params)
		# end transaction

		if ids:
			self.__addScopeToCache(self.__getScopeDetails(ids), True)

		return resultCursor.getStatusMessage()