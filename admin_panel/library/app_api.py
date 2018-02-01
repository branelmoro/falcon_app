try:
	from hashlib import blake2s
except ImportError:
	from pyblake2 import blake2s
from . import json

from ..resources.redis import redis as APPCACHE
from ..resources.backend_api import BACKEND_API, AUTH

from .. import exception as appException

from ..config import CLIENT_APP_CREDENTIALS


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

	def __init__(self, container):
		self.__container = container
		self.__session = container.getSession()

	def __addAsyncCurls(self, resources, multi_curl, async_next=None):
		if not isinstance(resources, list):
			resources = [resources]

		for resource in resources:

			if "async" in resource:
				next_api = async_next
				if "next_api" in resource:
					if next_api:
						next_api.append(NEXT_API(resource["next_api"]))
					else:
						next_api = [NEXT_API(resource["next_api"])]
				self.__addAsyncCurls(resources=resource, multi_curl=multi_curl, async_next=next_api)
			else:

				curl_obj = self.__getCurl(resource)

				if async_next is not None:
					curl_obj.add_next(async_next)

				multi_curl.add_handle(curl_obj)

	def __executeAsyncCurl(self, multi_curl):

		multi_curl.setopt(pycurl.M_PIPELINING, 1)

		unauthorised_curls = []

		# Perform multi-request.
		# This code copied from pycurl docs, modified to explicitly
		# set num_handles before the outer while loop.
		SELECT_TIMEOUT = 1.0
		num_handles = len(reqs)
		num_handles = 1
		old_handles = num_handles
		while num_handles:
			ret = m.select(SELECT_TIMEOUT)
			if ret == -1:
				continue
			while 1:
				ret, num_handles = multi_curl.perform()
				print(ret,num_handles)
				if old_handles != num_handles:
					# check completed request
					old_handles=num_handles
					queued_messages, successful_curls, failed_curls = multi_curl.info_read()
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
									self.executeAsync(next_api)
									curl_obj.update_next()

								curl_obj.doCleanUp()


				if ret != pycurl.E_CALL_MULTI_PERFORM: 
					break

		# print(multi_curl.info_read())

		# for req in reqs:
		# 	# print(req[1].getvalue())
		# 	req[2].close()


		if unauthorised_curls:
			self.__generateToken()
			m = pycurl.CurlMulti()
			for old_curl_obj in unauthorised_curls:

				api_detail = old_curl_obj.get_details()
				api_callback = old_curl_obj.get_callback()
				next_api = old_curl_obj.get_next()

				curl_obj = self.__getDataFromAPI(async=True, **api_detail)

				curl_obj.set_details(api_detail)
				curl_obj.set_callback(api_callback)
				curl_obj.add_next(next_api)

				m.add_handle(curl_obj)

			self.__executeAsyncCurl(m)

		multi_curl.close()

	def __getCurl(self, resource):

		if "api_detail" not in resource:
			# throw api server error
			raise appException.serverException_500({"app":"api details not provided"})

		if isinstance(resource["api_detail"], dict):
			api_detail = resource["api_detail"]
		else:
			api_detail = resource["api_detail"](**{container:self.__container})

		curl_obj = self.__getDataFromAPI(async=True, **api_detail)

		curl_obj.set_details(resource["api_detail"])

		if "api_callback" in resource:
			curl_obj.set_callback(resource["api_callback"])

		if "next_api" in resource:
			curl_obj.add_next(NEXT_API(resource["next_api"]))

		return curl_obj

	def executeAsync(self, resource):
		if isinstance(resource, list):
			# Build multi-request object.
			multi_curl = pycurl.CurlMulti()
			self.__addAsyncCurls(resources=resources)
			self.__executeAsyncCurl(multi_curl)
		else:

			if "api_detail" not in resource:
				# throw api server error
				raise appException.serverException_500({"app":"api details not provided"})
			if isinstance(resource["api_detail"], dict):
				api_detail = resource["api_detail"]
			else:
				api_detail = resource["api_detail"](**{container:self.__container})

			response = self.__getDataFromAPI(**api_detail)

			if resource["api_callback"]:
				resource["api_callback"](container=self.__container, **response)

			if "next_api" in resource:
				self.executeAsync(resource["next_api"])

	def get(self, url, header={}):
		return self.__getDataFromAPI(method="GET", url=url, header=header)

	def post(self, url, data = None, header={}):
		return self.__getDataFromAPI(method="POST", url=url, data=data, header=header)

	def put(self, url, data = None, header={}):
		return self.__getDataFromAPI(method="PUT", url=url, data=data, header=header)

	def delete(self, url, data, header={}):
		return self.__getDataFromAPI(method="DELETE", url=url, data=data, header=header)

	def __getDataFromAPI(self, method, url, data=None, header={}, async=False):
		header["access-token"] = self.__getToken()

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
		arrResponce = AUTH.grant_type_refresh_token()
		if arrResponce["httpcode"] == 400:
			self.__session.destory()
		else:
			self.__session.refresh(arrResponce["response"])

	def __generateToken(self):
		if self.__session.exists():
			self.__refreshUserToken()
		else:
			# client doesn't have right throw exception
			self.__generateClientToken()

	def __getToken(self):
		if self.__session.exists():
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
	def __generateClientToken(cls, conn=None):
		if conn is None:
			conn = APPCACHE.getConnection("appCache")

		client_session_id = cls.__getClientSessionId()
		bln_wait = False
		while conn.hget(client_session_id, "token_api_call")=="yes":
			time.sleep(0.1)
			bln_wait = True

		if bln_wait:
			cls.__client_session = conn.hgetall(client_session_id)
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
			conn.hmset(client_session_id,cls.__client_session)
		else:
			while conn.hget(client_session_id, "token_api_call")=="yes":
				time.sleep(0.1)
			cls.__client_session = conn.hgetall(client_session_id)

	@classmethod
	def startClientSession(cls):
		client_session_id = cls.__getClientSessionId()
		conn = APPCACHE.getConnection("appCache")
		if conn.exists(client_session_id):
			cls.__client_session = conn.hgetall(client_session_id)
		else:
			cls.__generateClientToken(conn)


# start client session
APP_API.startClientSession()