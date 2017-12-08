# this class caches all static data
import sys
from .. import exception as appException

# from ..models.oauth2Model import oauth2ScopeModel
# from ..models.staticTextModel import errorsModel

class APPCACHE(object):

	__cachedData = {}

	# __accessDb = redis("access_scopeDb")
	# __scopeKeyExpiry = 1200

	@classmethod
	def getSize(cls):
		return sys.getsizeof(cls.__cachedData)

	@classmethod
	def getData(cls):
		return cls.__cachedData

	@classmethod
	def loadCache(cls):
		if not cls.__cachedData:
			# load static data
			cls.__loadErrors()
			cls.__loadAccessScopes()
			pass
		else:
			return

	@classmethod
	def __loadErrors(cls):
		if "error" not in cls.__cachedData:
			cls.__cachedData["error"] = {}
			error_model = errorsModel()
			result = error_model.getAllErrors()
			for error_detail in result:
				error_id = error_detail["id"]
				del error_detail["id"]
				for lang in error_detail:
					cls.addError(error_id, lang, error_detail[lang])


		# load all errors and languages

	@classmethod
	def getError(cls, error_id, lang = None):
		if "error" in cls.__cachedData and error_id in cls.__cachedData["error"]:
			if lang and lang in cls.__cachedData["error"][error_id]:
				return cls.__cachedData["error"][error_id][lang]
			elif "english" in cls.__cachedData["error"][error_id]:
				return cls.__cachedData["error"][error_id]["english"]

		# no error found... through error
		raise appException.serverException_500({"error_message":"Error message not found", "error_id":error_id, "lang":lang})


	@classmethod
	def addError(cls, error_id, lang, text):
		if not text:
			return
		if "error" not in cls.__cachedData:
			cls.__cachedData["error"] = {}
		if error_id not in cls.__cachedData["error"]:
			cls.__cachedData["error"][error_id] = {}

		cls.__cachedData["error"][error_id][lang] = text


	@classmethod
	def deleteError(cls, error_id):
		if "error" in cls.__cachedData and error_id in cls.__cachedData["error"]:
			del cls.__cachedData["error"][error_id]


	@classmethod
	def __loadAccessScopes(cls):
		if "scope" not in cls.__cachedData:
			cls.__cachedData["scope"] = {}
			scope_model = oauth2ScopeModel()
			result = scope_model.getAllScopeDetails()

			for scope_detail in result:
				scope_id = str(scope_detail[1])
				cls.addScope(scope_id, "GET", scope_detail[2])
				cls.addScope(scope_id, "POST", scope_detail[3])
				cls.addScope(scope_id, "PUT", scope_detail[4])
				cls.addScope(scope_id, "DELETE", scope_detail[5])


	@classmethod
	def addScope(cls, scope_id, method, resources):
		if resources:
			cls.__addScopeMethod(scope_id, method, resources)
		else:
			cls.__deleteScopeMethod(scope_id, method)


	@classmethod
	def __addScopeMethod(cls, scope_id, method, resources):
		if "scope" not in cls.__cachedData:
			cls.__cachedData["scope"] = {}
		if scope_id not in cls.__cachedData["scope"]:
			cls.__cachedData["scope"][scope_id] = {}
		if method not in cls.__cachedData["scope"][scope_id]:
			cls.__cachedData["scope"][scope_id][method] = {}

		if isinstance(resources, list):

			# scopekey = str(scope_id) + "__" + method
			# if cls.__accessDb.exists(scopekey):
			# 	cls.__accessDb.delete(scopekey)
			# cls.__accessDb.sadd(scopekey, allowed_method)
			# cls.__accessDb.expire(scopekey, cls.__scopeKeyExpiry)
			# return

			for i in resources:
				cls.__cachedData["scope"][scope_id][method][i] = True


	@classmethod
	def __deleteScopeMethod(cls, scope_id, method):
		# scopekey = str(scope_id) + "__" + method
		# if cls.__accessDb.exists(scopekey):
		# 	cls.__accessDb.delete(scopekey)
		# 	return

		if (
			"scope" in cls.__cachedData
			and scope_id in cls.__cachedData["scope"]
			and method in cls.__cachedData["scope"][scope_id]
		):
			del cls.__cachedData["scope"][scope_id][method]

		if not cls.__cachedData["scope"][scope_id]:
			del cls.__cachedData["scope"][scope_id]

		if not cls.__cachedData["scope"]:
			del cls.__cachedData["scope"]


	@classmethod
	def deleteScope(cls, scope_id):
		scope_id = str(scope_id)
		cls.__deleteScopeMethod(scope_id, "GET")
		cls.__deleteScopeMethod(scope_id, "POST")
		cls.__deleteScopeMethod(scope_id, "PUT")
		cls.__deleteScopeMethod(scope_id, "DELETE")


	@classmethod
	def ifResourceExistsInScopes(cls, scope_id, method, resource_id):
		scope_id = str(scope_id)
		# return cls.__accessDb.sismember(str(scope_id) + "__" + method, resource_id)
		return (
			"scope" in cls.__cachedData
			and scope_id in cls.__cachedData["scope"]
			and method in cls.__cachedData["scope"][scope_id]
			and resource_id in cls.__cachedData["scope"][scope_id][method]
		)
