import hashlib
from . import APPCACHE
from ..resources.backend_api import BACKEND_API, Auth

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

	__session = None

	__client_session = None

	def __init__(self, session = None):
		self.__session = session

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

				if "api_detail" not in resource:
					# throw api server error
					pass

				if isinstance(resource["api_detail"], dict):
					api_detail = resource["api_detail"]
				else:
					api_detail = resource["api_detail"]()

				curl_obj = self.__getDataFromAPI(async=True, **api_detail)

				if "api_callback" in resource:
					curl_obj.set_callback(resource["api_callback"])

				if async_next is not None:
					curl_obj.add_next(async_next)

				if "next_api" in resource:
					curl_obj.add_next(NEXT_API(resource["next_api"]))

				multi_curl.add_handle(curl_obj)

	def __executeAsyncCurl(self, resources):
		# Build multi-request object.
		m = pycurl.CurlMulti()

		self.__addAsyncCurls(resources=resources, multi_curl=m)

		m.setopt(pycurl.M_PIPELINING, 1)

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
				ret, num_handles = m.perform()
				print(ret,num_handles)
				if old_handles != num_handles:
					# check completed request
					old_handles=num_handles
					queued_messages, successful_curls, failed_curls = m.info_read()
					if failed_curls:
						print("failed curls")
						print(failed_curls)
						# throw api server error
						pass
					if successful_curls:
						for curl_obj in successful_curls:


							response = self.handleResponse(curl_obj.getResponse())

							if response is False:
								# unauthorised token found, regenerate token
								raise "hbjnj"

							callback = curl_obj.get_callback()
							if callback:
								callback(response)


							next_api = curl_obj.get_next()
							if next_api:
								self.async(next_api)
								pass

				if ret != pycurl.E_CALL_MULTI_PERFORM: 
					break

		# print(m.info_read())

		# for req in reqs:
		# 	# print(req[1].getvalue())
		# 	req[2].close()

		m.close()

	def async(self, resources):
		while True
			try:
				self.__executeAsyncCurl(resources)
				break
			except:
				self.__generateToken()

	def get(self, path, header={}):
		return self.__getDataFromAPI(method="GET", path=path, header=header)

	def post(self, path, data = None, header={}):
		return self.__getDataFromAPI(method="POST", path=path, data=data, header=header)

	def put(self, path, data = None, header={}):
		return self.__getDataFromAPI(method="PUT", path=path, data=data, header=header)

	def delete(self, path, data, header={}):
		return self.__getDataFromAPI(method="DELETE", path=path, data=data, header=header)

	def __getDataFromAPI(self, method, path, data=None, header={}, async=False):
		header["access-token"] = self.__getToken()
		if method == "GET":
			response = BACKEND_API.get(path=path, header=header, async=async)
		elif method == "POST":
			response = BACKEND_API.post(path=path, data=data, header=header, async=async)
		elif method == "PUT":
			response = BACKEND_API.put(path=path, data=data, header=header, async=async)
		elif method == "DELETE":
			response = BACKEND_API.delete(path=path, data=data, header=header, async=async)

		if async:
			return response



		data = self.handleResponse(response)
		if data == False:
			# unauthorised token found, regenerate token
			self.__generateToken()
			return self.__getDataFromAPI(method=method, path=path, data=data, header=header)
		else:
			return data

	def handleResponse(self, response, callback=None):
		if response["httpcode"] == 401:
			# unauthorised token found, regenerate token
			return False
		elif response["httpcode"] == 404:
			# throw error, api does not exists
			pass
		else:
			if int(response["httpcode"]/100) == 5:
				# throw api server error
				exit()
				pass

			if callback:
				return callback(response)
			else:
				return response

	def __refreshUserToken(self):
		refresh_token = self.__session.get("refreshToken")
		arrResponce = Auth.grant_type_refresh_token()
		if arrResponce["httpcode"] == 400:
			self.__session.destory()
		else:
			self.__session.refresh(arrResponce["response"])

	def __generateToken(self):
		if self.__session is not None and self.__session.exists():
			self.__refreshUserToken()
		else:
			# client doesn't have right throw exception
			self.__generateClientToken()

	def __getToken(self):
		if self.__session is not None and self.__session.exists():
			return self.__session.get("accessToken")
		else:
			return self.__client_session["accessToken"]

	@classmethod
	def __isTransactionLocked(cls, client_session_id):
		conn = APPCACHE.getConnection("appcache")
		pipe = conn.pipeline(transaction=True)
		pipe.watch(client_session_id)
		pipe.multi()
		pipe.hset(client_session_id, "token_api_call", "yes")
		pipe.execute()

	@classmethod
	def __generateClientToken(cls):
		client_session_id = hashlib.md5(json.encode(CLIENT_APP_CREDENTIALS))
		bln_wait = False
		while APPCACHE.hget(client_session_id, "token_api_call")=="yes":
			time.sleep(0.1)
			bln_wait = True

		if bln_wait:
			cls.__client_session = APPCACHE.hgetall(client_session_id)
			return

		try:
			cls.__isTransactionLocked(client_session_id)
			is_lock_aquired = True
		except:
			is_lock_aquired = False

		if is_lock_aquired:
			arrResponce = Auth.grant_type_client_credentials()
			if arrResponce["httpcode"] == 400:
				raise appException.serverException_500({"app":"APP authorization failed"})
			cls.__client_session = arrResponce["response"]
			cls.__client_session["token_api_call"] = "no"
			APPCACHE.hmset(client_session_id,cls.__client_session)
		else
			while APPCACHE.hget(client_session_id, "token_api_call")=="yes":
				time.sleep(0.1)
			cls.__client_session = APPCACHE.hgetall(client_session_id)

	@classmethod
	def startClientSession(cls):
		client_session_id = hashlib.md5(json.encode(CLIENT_APP_CREDENTIALS))
		if APPCACHE.exists(client_session_id):
			cls.__client_session = APPCACHE.hgetall(client_session_id)
		else:
			cls.__generateClientToken()


# start client session
APP_API.startClientSession()