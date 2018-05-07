# never change this file unless required

from falcon import HTTP_400, HTTP_401, HTTP_403, HTTP_404, HTTP_405, HTTP_406, HTTP_500
from .. import exception as appException
from ..library import json
from ..library import APPCACHE
import sys
import traceback


from ..resources.redis import redis as SESSION
from ..models.oauth2Model import oauth2ResourceModel


APPCACHE.loadCache()

class container(object):

	def __init__(self, req, resp):
		self.req = req
		self.resp = resp
		self.data = {}


class baseController(object):
	"""This is base controller and all other controllers will be child"""

	def __init__(self, resource_id=None):
		if resource_id is None:
			raise appException.serverException_500({"resource_id":"Resource Id not Provided"})
		oauth2_resource = oauth2ResourceModel()
		self._path = oauth2_resource.getResourcePathById(resource_id)
		if self._path is None:
			raise appException.serverException_500({"resource_id":"Resource not found in authdb"})

		self.__resource_id = resource_id

	def _getResource(self, code=None):
		if code is None:
			raise appException.serverException_500({"resource_code":"Resource Codde not Provided"})
		oauth2_resource = oauth2ResourceModel()
		path = oauth2_resource.getResourceFieldByCode('resource_path', code)
		if path is None:
			raise appException.serverException_500({"resource_code":"Resource not found in authdb"})
		return path

	def getAllLangs(self):
		return ['english', 'hindi', 'marathi', 'gujarati', 'malayalam', 'bengali', 'oriya', 'tamil', 'telugu', 'panjabi', 'urdu', 'chinese_simplified', 'chinese_traditional', 'arabic', 'russian', 'portuguese', 'japanese', 'german', 'korean', 'french', 'turkish', 'italian', 'polish', 'ukrainian', 'persian', 'romanian', 'serbian', 'croatian', 'thai', 'dutch', 'amharic', 'catalan', 'danish', 'greek', 'spanish', 'estonian', 'finnish', 'armenian', 'khmer', 'kannada', 'malay', 'nepali', 'norwegian', 'slovak', 'albanian', 'swedish', 'tagalog']

	def __validateRequestHeaders(self, req):
		# validate request headers here
		is_valid = True
		if not is_valid:
			raise appException.clientException_406({"header":"Invalid Headers in request"})

	def __validateToken(self, req):
		# validate token here
		is_valid = False
		
		if("X-ACCESS-TOKEN" in req.headers):
			aTokenDb = SESSION("token_scopeDb");
			if(aTokenDb.exists(req.headers["X-ACCESS-TOKEN"])):
				is_valid = True

		# req.headers["X-ACCESS-TOKEN"]
		if not is_valid:
			raise appException.clientException_401({"token":"Unauthorised User, Invalid Token Provided"})

	def __validateUrlAccessRights(self, req):
		# validate token here
		# path = self.getPath()
		is_valid = False

		aTokenDb = SESSION("token_scopeDb");
		scopes = aTokenDb.smembers(req.headers["X-ACCESS-TOKEN"])

		for scope in scopes:
			if APPCACHE.ifResourceExistsInScopes(scope, req.method, self._resources[req.uri_template]):
			# if APPCACHE.ifResourceExistsInScopes(scope, req.method, self.__resource_id):
				is_valid = True
				break

		if not is_valid:
			raise appException.clientException_403({"url":"Access denied! You don't have right to resource url."})

	def __validateRequestBody(self, req):
		# validate request body here
		reqBody = req.stream.read().decode("utf-8")
		if reqBody == '':
			req.body = {}
		else:
			try:
				req.body = json.decode(reqBody)
			except Exception as e:
				raise appException.clientException_400({"request_body":"Invalid json provided"})

	def validateHTTPRequest(self, req, blnValidateToken = False):
		self.__validateRequestHeaders(req)
		if blnValidateToken:
			self.__validateToken(req)
			self.__validateUrlAccessRights(req)
		self.__validateRequestBody(req)

		# if request is valid then we get below params
		# params = {
		# 	"woking" : "fine",
		# 	"headers" : req.headers,
		# 	"params" : req.params,
		# 	# "options" : req.options,
		# 	"cookies" : req.cookies,
		# 	"protocol" : req.protocol,
		# 	"method" : req.method,
		# 	"host" : req.host,
		# 	"subdomain" : req.subdomain,
		# 	# "env" : req.env,
		# 	"app" : req.app,
		# 	"access_route" : req.access_route,
		# 	"remote_addr" : req.remote_addr,
		# 	"context" : req.context,
		# 	"uri" : req.uri,
		# 	"url" : req.url,
		# 	"relative_uri" : req.relative_uri,
		# 	"path" : req.path,
		# 	"query_string" : req.query_string,
		# 	"uri_template" : req.uri_template,
		# 	"accept" : req.accept,
		# 	"auth" : req.auth,
		# 	"body" : req.body
		# }

		return True

	def __internalServerError(self, container):
		resp = container.resp
		resp.status = HTTP_500
		params = {
			"nodename" : "node1",
			"version" : "0.0.1",
			"message" : "Error occured on server while processing"
		}
		exc_type, exc_value, exc_traceback = sys.exc_info()
		tb = traceback.format_list(traceback.extract_tb(exc_traceback))
		exception_message = traceback.format_exception_only(exc_type, exc_value)
		if True:#debugging enabled
			params["traceback"] = tb
			params["exception_message"] = exception_message
		else:
			#log server error tb, exception_message, req
			pass

		resp.body = json.encode(params)

	def __sendError(self, container, exc_value):
		resp = container.resp
		http_status = exc_value.getHttpStatus()
		if http_status == 401:
			resp.status = HTTP_401
		elif http_status == 403:
			resp.status = HTTP_403
		elif http_status == 404:
			resp.status = HTTP_404
		elif http_status == 405:
			resp.status = HTTP_405
		elif http_status == 406:
			resp.status = HTTP_406
		elif http_status == 500:
			resp.status = HTTP_500
		else:
			resp.status = HTTP_400
		# resp.status = falcon['HTTP_' + str(http_status)]
		params = exc_value.getErrorMessages();
		resp.body = json.encode(params)

	def __defaultRequestSetup(self, req, resp):
		resp.set_header("content-type", "application/json")
		return container(req=req, resp=resp)

	def on_get(self, req, resp, **kargs):
		try:
			container = self.__defaultRequestSetup(req, resp)
			self.get(container, **kargs)
		except appException.clientException as e:
			self.__sendError(container, e)
		except:
			#catch error
			self.__internalServerError(container)

	def on_post(self, req, resp, **kargs):
		try:
			container = self.__defaultRequestSetup(req, resp)
			self.post(container, **kargs)
		except appException.clientException as e:
			self.__sendError(container, e)
		except:
			#catch error
			self.__internalServerError(container)

	def on_put(self, req, resp, **kargs):
		try:
			container = self.__defaultRequestSetup(req, resp)
			self.put(container, **kargs)
		except appException.clientException as e:
			self.__sendError(container, e)
		except:
			#catch error
			self.__internalServerError(container)

	def on_delete(self, req, resp, **kargs):
		try:
			container = self.__defaultRequestSetup(req, resp)
			self.delete(container, **kargs)
		except appException.clientException as e:
			self.__sendError(container, e)
		except:
			#catch error
			self.__internalServerError(container)

	def get(self, container, **kargs):
		raise appException.clientException_405({"message" : "get method not allowed"})

	def post(self, container, **kargs):
		raise appException.clientException_405({"message" : "post method not allowed"})

	def put(self, container, **kargs):
		raise appException.clientException_405({"message" : "put method not allowed"})

	def delete(self, container, **kargs):
		raise appException.clientException_405({"message" : "delete method not allowed"})

	def _getFilteredRequestData(self, req, fieldList):
		data = {}
		for field in fieldList:
			if field in req.body:
				data[field] = req.body[field]
		return data

	def _getError(self, error_id, lang = None, data = None):
		message = APPCACHE.getError(error_id, lang)
		if data:
			message = message.format(**data)
		return message

	def raise404(self):
		raise appException.clientException_404({"message" : "Url does not exists"})


class CRUDS(baseController):

	def get(self, container, **kwarg):
		if container.req.uri_template == self._crud_template:
			self.validateHTTPRequest(container.req)
			self._get(container, **kwarg)
		elif container.req.uri_template == self._search_template or container.req.uri_template == self._search_page_template:
			self.validateHTTPRequest(container.req)
			self._search(container, **kwarg)
		else:
			self.raise404()

	def post(self, container, **kwarg):
		# if container.req.uri_template == self._create_template:
		if container.req.uri_template == self._crud_template or container.req.uri_template == self._create_template:
			self.validateHTTPRequest(container.req)
			self._post(container, **kwarg)
		elif container.req.uri_template == self._search_template or container.req.uri_template == self._search_page_template:
			self.validateHTTPRequest(container.req)
			self._search(container, **kwarg)
		else:
			self.raise404()

	def put(self, container, **kwarg):
		if container.req.uri_template == self._crud_template:
			self.validateHTTPRequest(container.req)
			self._put(container, **kwarg)
		else:
			self.raise404()

	def delete(self, container, **kwarg):
		if container.req.uri_template == self._crud_template:
			self.validateHTTPRequest(container.req)
			self._delete(container, **kwarg)
		else:
			self.raise404()

	def _get(self, container, **kwarg):
		self.raise404()

	def _post(self, container, **kwarg):
		self.raise404()

	def _put(self, container, **kwarg):
		self.raise404()

	def _delete(self, container, **kwarg):
		self.raise404()

	def _search(self, container):
		self.raise404()