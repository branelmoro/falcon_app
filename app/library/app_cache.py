# this class caches all static data
import sys
from .. import exception as appException

class APPCACHE(object):

	__cachedData = {}

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
		# load all errors and languages



	@classmethod
	def ifResourceExistsInScopes(cls, scope_id, method, resource_id):
		return (
			"scope" in cls.__cachedData
			and scope_id in cls.__cachedData["scope"]
			and method in cls.__cachedData["scope"][scope_id]
			and resource_id in cls.__cachedData["scope"][scope_id][method]
		)
