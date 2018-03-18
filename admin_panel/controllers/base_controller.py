# never change this file unless required

from falcon import HTTP_400, HTTP_401, HTTP_403, HTTP_404, HTTP_405, HTTP_406, HTTP_500, HTTPMovedPermanently, HTTPFound, HTTPSeeOther, HTTPTemporaryRedirect, HTTPPermanentRedirect
from .. import exception as appException
from ..library import json, BASE_HTML, SESSION, APP_API, APPCACHE
import sys
import traceback

from ..config import BACKEND_API_URL

from ..resources.redis import redis

from falcon.util import uri
from html import unescape
from urllib.parse import parse_qs

import cgi, io

TOKENDB = redis("token_scopeDb")

# APPCACHE.loadCache()

class container(object):

	def __init__(self, req, resp):
		self.req = req
		self.resp = resp
		self.data = {}
		self.__session = SESSION(self)

	def getSession(self):
		return self.__session



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
			if(TOKENDB.exists(req.headers["X-ACCESS-TOKEN"])):
				is_valid = True

		# req.headers["X-ACCESS-TOKEN"]
		if not is_valid:
			raise appException.clientException_401({"token":"Unauthorised User, Invalid Token Provided"})

	def __validateUrlAccessRights(self, req):
		# validate token here
		# path = self.getPath()
		is_valid = False

		scopes = TOKENDB.smembers(req.headers["X-ACCESS-TOKEN"])

		for scope in scopes:
			if APPCACHE.ifResourceExistsInScopes(scope, req.method, self.__resource_id):
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
		req = container.req
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
		resp.set_header("content-type", "text/html")
		return container(req=req, resp=resp)

	def on_get(self, req, resp):
		try:
			container = self.__defaultRequestSetup(req, resp)
			self.get(container)
		except appException.clientException as e:
			self.__sendError(container, e)
		except (HTTPMovedPermanently, HTTPFound, HTTPSeeOther, HTTPTemporaryRedirect, HTTPPermanentRedirect) as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			raise exc_type(str(exc_value))
		except:
			#catch error
			self.__internalServerError(container)

	def on_post(self, req, resp):
		try:
			container = self.__defaultRequestSetup(req, resp)
			self.post(container)
		except appException.clientException as e:
			self.__sendError(container, e)
		except (HTTPMovedPermanently, HTTPFound, HTTPSeeOther, HTTPTemporaryRedirect, HTTPPermanentRedirect) as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			raise exc_type(str(exc_value))
		except:
			#catch error
			self.__internalServerError(container)

	def on_put(self, req, resp):
		try:
			container = self.__defaultRequestSetup(req, resp)
			self.put(container)
		except appException.clientException as e:
			self.__sendError(container, e)
		except (HTTPMovedPermanently, HTTPFound, HTTPSeeOther, HTTPTemporaryRedirect, HTTPPermanentRedirect) as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			raise exc_type(str(exc_value))
		except:
			#catch error
			self.__internalServerError(container)

	def on_delete(self, req, resp):
		try:
			container = self.__defaultRequestSetup(req, resp)
			self.delete(container)
		except appException.clientException as e:
			self.__sendError(container, e)
		except (HTTPMovedPermanently, HTTPFound, HTTPSeeOther, HTTPTemporaryRedirect, HTTPPermanentRedirect) as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			raise exc_type(str(exc_value))
		except:
			#catch error
			self.__internalServerError(container)

	def get(self, req, resp):
		raise appException.clientException_405({"message" : "get method not allowed"})

	def post(self, req, resp):
		raise appException.clientException_405({"message" : "post method not allowed"})

	def put(self, req, resp):
		raise appException.clientException_405({"message" : "put method not allowed"})

	def delete(self, req, resp):
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

	def _render(self, view, body={}, head={}):
		return BASE_HTML.renderView(view=view, body=body, head=head, partial=False)

	def _renderPartial(self, view, body={}, head={}):
		return BASE_HTML.renderView(view=view, body=body, head=head, partial=True)

	def getAPI(self, container):
		return APP_API(container)

	def getAPIURL(self, path):
		return BACKEND_API_URL + path

	def _checkSession(self, container):
		if container.getSession().isUserLoggedIn():
			return
		else:
			# redirect to login
			pass


# static page - no need of api
	# 1) need session
	# 2) no need of session
# dynamic:
	# 1) api needed, no need of session
	# 2) session needed, no need of api
	# 3) session and api both needed