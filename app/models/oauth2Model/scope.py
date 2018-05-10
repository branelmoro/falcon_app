from datetime import datetime
# always extend your model from base_model
# always give model class name same as model name
from ..base_model import baseModel

from . import oauth2AdminUserModel
from . import oauth2ClientModel
# import uwsgi
# uwsgi.reload()

class scope(baseModel):
	"""entire code goes here"""

	def __init__(self):
		# from ...library import APPCACHE
		# self.__APPCACHE = APPCACHE
		pass


	def getAllScopeDetails(self):
		qry = """
			SELECT code,
				id,
				allowed_get,
				allowed_post,
				allowed_put,
				allowed_delete
			FROM oauth2.scope;
		"""
		resultCursor = self.pgSlave().query(qry,[])

		return resultCursor.getAllRecords()

	def __getScopeDetails(self, ids):
		values = "%s,"*(len(ids)-1) + "%s"
		qry = """
			SELECT code,
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

		return [i[0] for i in result]


	def getAllowedResourcesFromScopeIds(self, ids):

		result = self.__getScopeDetails(ids)

		get = []
		post = []
		put = []
		delete = []

		for row in result:
			get = get + row[2]
			post = post + row[3]
			put = put + row[4]
			delete = delete + row[5]

		return {
			"get" : list(set(get)),
			"post" : list(set(post)),
			"put" : list(set(put)),
			"delete" : list(set(delete))
		}



	def __addScopeToCache(self, result):
		return

		# for scope_detail in result:
		# 	scope_id = str(scope_detail[1])
		# 	self.__APPCACHE.addScope(scope_id, "GET", scope_detail[2])
		# 	self.__APPCACHE.addScope(scope_id, "POST", scope_detail[3])
		# 	self.__APPCACHE.addScope(scope_id, "PUT", scope_detail[4])
		# 	self.__APPCACHE.addScope(scope_id, "DELETE", scope_detail[5])


	def __deleteScopeFromCache(self,scope_id):
		return
		# self.__APPCACHE.deleteScope(scope_id)


	def ifScopeCodeExists(self, code, not_id=None):
		param = [code]
		strNotId = ""
		if not_id is not None:
			param.append(not_id)
			strNotId = " and id != %s"

		qry = """
			SELECT exists(
				SELECT id
				FROM oauth2.scope
				WHERE code = %s """+strNotId+"""
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
				code,
				scope_info,
				allowed_get,
				allowed_post,
				allowed_put,
				allowed_delete,
				last_edit_time
			) VALUES (%s, %s, %s::int[], %s::int[], %s::int[], %s::int[], %s);
		"""
		resultCursor = dbObj.query(qry, [scope_detail["code"], scope_detail["scope_info"], scope_detail["allowed_get"], scope_detail["allowed_post"], scope_detail["allowed_put"], scope_detail["allowed_delete"], datetime.now()])
		# end transaction

		insertId = resultCursor.getLastInsertId();

		self.__addScopeToCache(self.__getScopeDetails([insertId]))

		return resultCursor.getStatusMessage()


	def updateScope(self, scope_detail):

		params = []
		listSet = []

		fieldList = ["code", "scope_info"]
		for i in fieldList:
			if i in scope_detail:
				listSet.append(i + " = %s")
				params.append(scope_detail[i])


		fieldList = ["allowed_get", "allowed_post", "allowed_put", "allowed_delete"]
		for i in fieldList:
			if i in scope_detail:
				listSet.append(i + " = %s::text[]")
				params.append(scope_detail[i])

		listSet.append("last_edit_time = %s")
		qry = """UPDATE oauth2.scope set """ + (','.join(listSet)) + """ where id = %s and is_editable = %s;"""
		params.extend([datetime.now(), scope_detail["id"], True])
		dbObj = self.pgMaster()
		resultCursor = dbObj.query(qry, params)

		self.__addScopeToCache(self.__getScopeDetails([scope_detail["id"]]))
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
			client_model.deleteScopeFromClient(scope_id, dbTansaction)

		self.__deleteScopeFromCache(scope_id)
		dbTansaction.commit()
		# end transaction
		return resultCursor.getStatusMessage()

	def ifValidScopeCodeExists(self, codes):
		values = "%s,"*(len(codes)-1) + "%s"
		qry = """
			SELECT count(id) as cnt
			FROM oauth2.scope
			WHERE code in ("""+values+""");
		"""
		resultCursor = self.pgSlave().query(qry,codes)
		result = resultCursor.getOneRecord()
		return (len(codes) == result[0])

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

		allowed_resource = [i+" != %s::text[]" for i in allowed_resource]
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

	def deleteResourceFromScope(self, resource_code, dbObj = None):
		if dbObj is None:
			dbObj = self.pgMaster()

		params = [resource_code, resource_code, resource_code, resource_code]

		qry = """
			SELECT id
			FROM oauth2.scope
			WHERE %s::text = ANY(allowed_get)
				or %s::text = ANY(allowed_post)
				or %s::text = ANY(allowed_put)
				or %s::text = ANY(allowed_delete);
		"""
		resultCursor = self.pgSlave().query(qry,params)
		result = resultCursor.getAllRecords()

		ids = [result[i][0] for i in result]

		qry = """
			UPDATE oauth2.scope
			SET allowed_get = array_remove(allowed_get, %s::text),
				allowed_post = array_remove(allowed_post, %s::text),
				allowed_put = array_remove(allowed_put, %s::text),
				allowed_delete = array_remove(allowed_delete, %s::text)
			WHERE %s::text = ANY(allowed_get)
				or %s::text = ANY(allowed_post)
				or %s::text = ANY(allowed_put)
				or %s::text = ANY(allowed_delete);
		"""
		params = params + params
		resultCursor = dbObj.query(qry, params)
		# end transaction

		if ids:
			self.__addScopeToCache(self.__getScopeDetails(ids))

		return resultCursor.getStatusMessage()