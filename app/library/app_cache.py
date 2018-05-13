# this class caches all static data
import sys
from .. import exception as appException

# from ..resources.redis import redis
from ..models.oauth2Model import oauth2ScopeModel
from ..models.staticTextModel import errorsModel

class APPCACHE(object):

	__cachedData = {}

	# __accessDb = redis('access_scopeDb')
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
		if 'error' not in cls.__cachedData:
			cls.__cachedData['error'] = {}
			error_model = errorsModel()
			result = error_model.getAllErrors()
			for error_detail in result:
				error_code = error_detail['code']
				del error_detail['code']
				for lang in error_detail:
					cls.addError(error_code, lang, error_detail[lang])


		# load all errors and languages

	@classmethod
	def getError(cls, error_code, lang = None):
		if 'error' in cls.__cachedData and error_code in cls.__cachedData['error']:
			if lang and lang in cls.__cachedData['error'][error_code]:
				return cls.__cachedData['error'][error_code][lang]
			elif 'english' in cls.__cachedData['error'][error_code]:
				return cls.__cachedData['error'][error_code]['english']

		# no error found... through error
		raise appException.serverException_500({'error_message':'Error message not found', 'error_code':error_code, 'lang':lang})


	@classmethod
	def addError(cls, error_code, lang, text):
		if not text:
			return
		if 'error' not in cls.__cachedData:
			cls.__cachedData['error'] = {}
		if error_code not in cls.__cachedData['error']:
			cls.__cachedData['error'][error_code] = {}

		cls.__cachedData['error'][error_code][lang] = text


	@classmethod
	def deleteError(cls, error_code):
		if 'error' in cls.__cachedData and error_code in cls.__cachedData['error']:
			del cls.__cachedData['error'][error_code]


	@classmethod
	def __loadAccessScopes(cls):
		if 'scope' not in cls.__cachedData:
			cls.__cachedData['scope'] = {}
			scope_model = oauth2ScopeModel()
			result = scope_model.getAllScopeDetails()

			for scope_detail in result:
				scope_code = str(scope_detail[0])
				cls.addScope(scope_code, 'GET', scope_detail[2])
				cls.addScope(scope_code, 'POST', scope_detail[3])
				cls.addScope(scope_code, 'PUT', scope_detail[4])
				cls.addScope(scope_code, 'DELETE', scope_detail[5])


	@classmethod
	def addScope(cls, scope_code, method, resources):
		if resources:
			cls.__addScopeMethod(scope_code, method, resources)
		else:
			cls.__deleteScopeMethod(scope_code, method)


	@classmethod
	def __addScopeMethod(cls, scope_code, method, resources):
		if 'scope' not in cls.__cachedData:
			cls.__cachedData['scope'] = {}
		if scope_code not in cls.__cachedData['scope']:
			cls.__cachedData['scope'][scope_code] = {}
		if method not in cls.__cachedData['scope'][scope_code]:
			cls.__cachedData['scope'][scope_code][method] = {}

		if isinstance(resources, list):

			# scopekey = str(scope_code) + '__' + method
			# if cls.__accessDb.exists(scopekey):
			# 	cls.__accessDb.delete(scopekey)
			# cls.__accessDb.sadd(scopekey, allowed_method)
			# cls.__accessDb.expire(scopekey, cls.__scopeKeyExpiry)
			# return

			for i in resources:
				cls.__cachedData['scope'][scope_code][method][i] = True


	@classmethod
	def __deleteScopeMethod(cls, scope_code, method):
		# scopekey = str(scope_code) + '__' + method
		# if cls.__accessDb.exists(scopekey):
		# 	cls.__accessDb.delete(scopekey)
		# 	return

		if (
			'scope' in cls.__cachedData
			and scope_code in cls.__cachedData['scope']
			and method in cls.__cachedData['scope'][scope_code]
		):
			del cls.__cachedData['scope'][scope_code][method]

		if not cls.__cachedData['scope'][scope_code]:
			del cls.__cachedData['scope'][scope_code]

		if not cls.__cachedData['scope']:
			del cls.__cachedData['scope']


	@classmethod
	def deleteScope(cls, scope_code):
		scope_code = str(scope_code)
		cls.__deleteScopeMethod(scope_code, 'GET')
		cls.__deleteScopeMethod(scope_code, 'POST')
		cls.__deleteScopeMethod(scope_code, 'PUT')
		cls.__deleteScopeMethod(scope_code, 'DELETE')


	@classmethod
	def ifResourceExistsInScopes(cls, scope_code, method, resource_id):
		scope_code = str(scope_code)
		# return cls.__accessDb.sismember(str(scope_code) + '__' + method, resource_id)
		return (
			'scope' in cls.__cachedData
			and scope_code in cls.__cachedData['scope']
			and method in cls.__cachedData['scope'][scope_code]
			and resource_id in cls.__cachedData['scope'][scope_code][method]
		)
