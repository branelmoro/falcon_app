try:
	from hashlib import blake2s
except ImportError:
	from pyblake2 import blake2s
from . import json

from ..resources.redis import redis as APPCACHE
from ..resources.backend_api import BACKEND_API, AUTH, ASYNC_CURL

from .. import exception as appException

from ..config import CLIENT_APP_CREDENTIALS

import pycurl


class NEXT_API(object):

	def __init__(self, next):
		self.__next = next
		self.__count = 0

	def addCount(self):
		self.__count = self.__count + 1

	def delCount(self):
		self.__count = self.__count - 1

	def getCount(self):
		return self.__count

	def get(self):
		return self.__next


class APP_API(object):

	__client_session = None

	__allowed_resources = {}

	def __init__(self, container):
		self.__container = container
		self.__session = container.getSession()

	def __addAsyncCurls(self, resources, async_curl, async_next=None):
		if not isinstance(resources, list):
			resources = [resources]

		for resource in resources:

			if "async" in resource:
				next_api = async_next
				if "next" in resource:
					if next_api:
						next_api.append(NEXT_API(resource["next"]))
					else:
						next_api = [NEXT_API(resource["next"])]
				self.__addAsyncCurls(resources=resource["async"], async_curl=async_curl, async_next=next_api)
			else:

				curl_obj = self.__getCurl(resource)

				if async_next is not None:
					curl_obj.add_next(async_next)

				async_curl.add_handle(curl_obj)

	def __executeAsyncCurl(self, async_curl):

		# async_curl.setopt(pycurl.M_PIPELINING, 1)

		unauthorised_curls = []

		# Perform multi-request.
		# This code copied from pycurl docs, modified to explicitly
		# set num_handles before the outer while loop.
		SELECT_TIMEOUT = 1.0
		# num_handles = len(reqs)
		num_handles = 1
		old_handles = num_handles
		while num_handles:
			ret = async_curl.select(SELECT_TIMEOUT)
			if ret == -1:
				continue
			while 1:
				ret, num_handles = async_curl.perform()
				print(ret,num_handles)
				if old_handles != num_handles:
					# check completed request
					old_handles=num_handles
					queued_messages, successful_curls, failed_curls = async_curl.info_read()
					if failed_curls:
						print("failed curls")
						print(failed_curls)
						# throw api server error
						raise appException.serverException_500({"app":"api server not reachable"})
					if successful_curls:
						for curl_obj in successful_curls:

							response = self.__handleAPIResponse(curl_obj.getResponse())

							if response is False:
								# unauthorised token found, regenerate token
								unauthorised_curls.append(curl_obj)
							else:
								curl_obj.del_next()
								callback = curl_obj.get_callback()
								if callback:
									callback(container=self.__container, **response)

								next_api = curl_obj.get_next_executable()
								if next_api:
									print(next_api)
									self.executeAsync(next_api)
									curl_obj.update_next()

								curl_obj.doCleanUp()


				if ret != pycurl.E_CALL_MULTI_PERFORM: 
					break

		# print(async_curl.info_read())

		# for req in reqs:
		# 	# print(req[1].getvalue())
		# 	req[2].close()


		if unauthorised_curls:
			self.__generateToken()
			m = pycurl.CurlMulti()
			for old_curl_obj in unauthorised_curls:

				api_detail = old_curl_obj.get_details()
				callback = old_curl_obj.get_callback()
				next_api = old_curl_obj.get_next()

				curl_obj = self.__getDataFromAPI(async=True, **api_detail)

				if not isinstance(api_detail, dict):
					api_detail = api_detail(**{container:self.__container})

				curl_obj.set_details(api_detail)
				curl_obj.set_callback(callback)
				curl_obj.add_next(next_api)

				m.add_handle(curl_obj)

			self.__executeAsyncCurl(m)

		# async_curl.close()

	def __getCurl(self, resource):

		api_detail = {}

		if "api_detail" in resource:
			api_detail = resource["api_detail"]
			# api_detail.update(resource["api_detail"](**{container:self.__container}))
		else:
			if "url" in resource:
				api_detail["url"] = resource["url"]
			if "method" in resource:
				api_detail["method"] = resource["method"]
			if "header" in resource:
				api_detail["header"] = resource["header"]
			if "data" in resource:
				api_detail["data"] = resource["data"]

		if not api_detail:
			print(resource)
			raise appException.serverException_500({"app":"api details - method,url not provided"})

		if not isinstance(api_detail, dict):
			api_data = api_detail(**{container:self.__container})
		else:
			api_data = api_detail

		curl_obj = self.__getDataFromAPI(async=True, **api_data)

		curl_obj.set_details(api_detail)

		if "callback" in resource:
			curl_obj.set_callback(resource["callback"])

		if "next" in resource:
			curl_obj.add_next(NEXT_API(resource["next"]))

		return curl_obj

	def executeAsync(self, resource):
		if isinstance(resource, list):
			# Build async-curl object.
			async_curl = ASYNC_CURL()
			self.__addAsyncCurls(resources=resource, async_curl=async_curl)
			self.__executeAsyncCurl(async_curl)
		else:

			api_detail = {}

			if "api_detail" in resource:
				api_detail = resource["api_detail"]
				# api_detail.update(resource["api_detail"](**{container:self.__container}))
			else:
				if "url" in resource:
					api_detail["url"] = resource["url"]
				if "method" in resource:
					api_detail["method"] = resource["method"]
				if "header" in resource:
					api_detail["header"] = resource["header"]
				if "data" in resource:
					api_detail["data"] = resource["data"]

			if not api_detail:
				raise appException.serverException_500({"app":"api details - method,url not provided"})

			if not isinstance(api_detail, dict):
				api_data = api_detail(**{container:self.__container})
			else:
				api_data = api_detail

			response = self.__getDataFromAPI(**api_data)

			if resource["callback"]:
				resource["callback"](container=self.__container, **response)

			if "next" in resource:
				self.executeAsync(resource["next"])

	def get(self, url, header={}):
		return self.__getDataFromAPI(method="GET", url=url, header=header)

	def post(self, url, data = None, header={}):
		return self.__getDataFromAPI(method="POST", url=url, data=data, header=header)

	def put(self, url, data = None, header={}):
		return self.__getDataFromAPI(method="PUT", url=url, data=data, header=header)

	def delete(self, url, data, header={}):
		return self.__getDataFromAPI(method="DELETE", url=url, data=data, header=header)

	def __getDataFromAPI(self, method, url, data=None, header={}, async=False):
		header["X-ACCESS-TOKEN"] = self.__getToken()

		response = BACKEND_API.execute(method=method, url=url, data=data, header=header, async=async)

		if async:
			return response

		data = self.__handleAPIResponse(response)
		if data == False:
			# unauthorised token found, regenerate token
			self.__generateToken()
			return self.__getDataFromAPI(method=method, url=url, data=data, header=header)
		else:
			return data

	def __handleAPIResponse(self, response):
		
		if response["httpcode"] == 401:
			# unauthorised token found, regenerate token
			return False
		elif response["httpcode"] == 404:
			# throw error, api does not exists
			raise appException.serverException_500({"app":"api does not exist"})
		elif int(response["httpcode"]/100) == 5:
			# throw api server error
			raise appException.serverException_500({"app":"api does not exist"})
		else:
			return response

	def __refreshUserToken(self):
		refresh_token = self.__session.get("refreshToken")
		arrResponce = AUTH.grant_type_refresh_token(refresh_token)
		if arrResponce["httpcode"] == 400:
			self.__session.destory()
		else:
			self.__session.refresh(arrResponce["response"])

	def __generateToken(self):
		if self.__session.isUserLoggedIn():
			self.__refreshUserToken()
		else:
			# client doesn't have right throw exception
			self.__generateClientToken()

	def __getToken(self):
		if self.__session.isUserLoggedIn():
			return self.__session.get("accessToken")
		else:
			return self.__client_session["accessToken"]

	@classmethod
	def __isTransactionLocked(cls, client_session_id, conn):
		pipe = conn.pipeline(transaction=True)
		pipe.watch(client_session_id)
		pipe.multi()
		pipe.hset(client_session_id, "token_api_call", "yes")
		pipe.execute()

	@classmethod
	def __getClientSessionId(cls):
		return blake2s(json.encode(CLIENT_APP_CREDENTIALS).encode('utf-8')).hexdigest()

	@classmethod
	def __setClientSession(cls,client_session_id, conn):
		data = conn.hgetall(client_session_id)
		cls.__client_session = {k.decode():data[k].decode() for k in data}
		cls.__allowed_resources['get'] = conn.smembers(client_session_id + '_get')
		cls.__allowed_resources['post'] = conn.smembers(client_session_id + '_post')
		cls.__allowed_resources['put'] = conn.smembers(client_session_id + '_put')
		cls.__allowed_resources['delete'] = conn.smembers(client_session_id + '_delete')


	@classmethod
	def __generateClientToken(cls, conn=None):
		if conn is None:
			conn = APPCACHE("appCache").getConnection()

		client_session_id = cls.__getClientSessionId()
		bln_wait = False
		while conn.hget(client_session_id, "token_api_call")=="yes":
			time.sleep(0.1)
			bln_wait = True

		if bln_wait:
			cls.__setClientSession(client_session_id, conn)
			return

		try:
			cls.__isTransactionLocked(client_session_id, conn)
			is_lock_aquired = True
		except:
			is_lock_aquired = False

		if is_lock_aquired:
			arrResponce = AUTH.grant_type_client_credentials()
			print(arrResponce)
			if arrResponce["httpcode"] == 500:
				raise appException.serverException_500({"app":"APP authorization server error"})
			if arrResponce["httpcode"] == 400:
				raise appException.serverException_500({"app":"APP authorization failed"})
			cls.__client_session = json.decode(arrResponce["response"])
			cls.__client_session["token_api_call"] = "no"

			if 'resources' in cls.__client_session:
				for method in cls.__client_session['resources']:
					cls.__allowed_resources[method] = set(cls.__client_session['resources'][method])
					conn.sadd(client_session_id + '_' + method, cls.__client_session['resources'][method])
					conn.expire(client_session_id + '_' + method, cls.__client_session['accessTokenExpiry'])
				del cls.__client_session['resources']

			conn.hmset(client_session_id,cls.__client_session)
			conn.expire(client_session_id, cls.__client_session['accessTokenExpiry'])
		else:
			while conn.hget(client_session_id, "token_api_call")=="yes":
				time.sleep(0.1)
			cls.__setClientSession(client_session_id, conn)

	@classmethod
	def startClientSession(cls):
		client_session_id = cls.__getClientSessionId()
		conn = APPCACHE("appCache").getConnection()
		if conn.exists(client_session_id):
			cls.__setClientSession(client_session_id, conn)
			print(cls.__client_session)
		else:
			cls.__generateClientToken(conn)

	@classmethod
	def is_allowed(cls, method, resource_code):
		return resource_code in cls.__allowed_resources[method]

# start client session
APP_API.startClientSession()