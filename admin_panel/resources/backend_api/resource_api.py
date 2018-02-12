import pycurl
from io import BytesIO

from ...library import json

class ASYNC_CURL():

	def __init__(self):
		self.__multi_curl = pycurl.CurlMulti()
		self.__multi_curl.setopt(pycurl.M_PIPELINING, 1)
		self.__custom_curls = {}

	def getHandleLength(self):
		return len(self.__custom_curls)

	def add_handle(self, custom_curl):
		curl = custom_curl.getCurl()
		self.__multi_curl.add_handle(curl)
		self.__custom_curls[id(curl)] = custom_curl

	def select(self, select):
		return self.__multi_curl.select(select)

	def perform(self):
		return self.__multi_curl.perform()

	def info_read(self):
		# multi_curl.info_read()
		queued_messages, successful_curls, failed_curls = self.__multi_curl.info_read()

		successful = []
		for i in successful_curls:
			uid = id(i)
			successful.append(self.__custom_curls[uid])
			del self.__custom_curls[uid]

		failed = []
		for i in failed_curls:
			uid = id(i)
			failed.append(self.__custom_curls[uid])
			del self.__custom_curls[uid]

		return (queued_messages, successful, failed)

	def __del__(self):
		self.__multi_curl.close()
		print("multicurl closed")


class CUSTOM_CURL():

	def __init__(self):
		self.__curl = pycurl.Curl()
		self.__buffer = BytesIO()
		self.__curl.setopt(self.__curl.WRITEDATA, self.__buffer)
		self.__api_callback = None
		self.__next_api = {}
		self.__details = {}

	def getCurl(self):
		return self.__curl

	def set_details(self, details):
		self.__details = details

	def get_details(self):
		return self.__details

	def get_buffer(self):
		return self.__buffer

	def set_callback(self, callback):
		self.__api_callback = callback

	def get_callback(self):
		return self.__api_callback

	def add_next(self, next_api):
		if not isinstance(next_api, list):
			next_api = [next_api]
		for i in next_api:
			obj_id = id(i)
			if obj_id not in self.__next_api:
				self.__next_api[obj_id] = i
				i.addCount()

	def del_next(self):
		for i in self.__next_api:
			self.__next_api[i].delCount()

	def update_next(self):
		self.__next_api = {i:self.__next_api[i] for i in self.__next_api if self.__next_api[i].getCount() > 0}

	def get_next_executable(self):
		executable = []
		for i in self.__next_api:
			if self.__next_api[i].getCount() == 0:
				resource = self.__next_api[i].get()
				if isinstance(resource, list):
					executable.extend(resource)
				else:
					executable.append(resource)
		return executable
		# return [self.__next_api[i].get() for i in self.__next_api if self.__next_api[i].getCount() == 0]

	def get_next(self):
		return [self.__next_api[i] for i in self.__next_api]

	def getResponse(self):
		# os_errno = self.getinfo(self.OS_ERRNO);
		data = {
			"response":self.__buffer.getvalue().decode("utf-8"),
			# "error_no" => os_errno,
			"httpcode":self.__curl.getinfo(self.__curl.HTTP_CODE)
		}
		return data

	def doCleanUp(self):
		self.__api_callback = None
		self.__next_api = {}
		self.__details = {}
		self.__buffer.close()
		self.__curl.close()

	def setMethod(self, method):
		self.__curl.setopt(self.__curl.CUSTOMREQUEST, method)

	def setUrl(self, url):
		self.__curl.setopt(self.__curl.URL, url)

	def setData(self, data):
		self.__curl.setopt(self.__curl.POSTFIELDS, data)

	def setHeader(self, header):
		self.__curl.setopt(self.__curl.HTTPHEADER, header)

	def execute(self):
		self.__curl.perform()

	def __del__(self):
		self.doCleanUp()
		print("done cleanup")




class BACKEND_API(object):

	@classmethod
	def get(cls, url, header={}, async=False):
		return cls.execute(method="GET", url=url, header=header, async=async)

	@classmethod
	def post(cls, url, data = None, header={}, async=False):
		return cls.execute(method="POST", url=url, data=data, header=header, async=async)

	@classmethod
	def put(cls, url, data = None, header={}, async=False):
		return cls.execute(method="PUT", url=url, data=data, header=header, async=async)

	@classmethod
	def delete(cls, url, data, header={}, async=False):
		return cls.execute(method="DELETE", url=url, data=data, header=header, async=async)

	@classmethod
	def execute(cls, method, url, header, data = None, async=False):
		# if async:
		# 	c = CUSTOM_CURL()
		# else:
		# 	c = CUSTOM_CURL(pycurl.Curl)
		c = CUSTOM_CURL()
		c.setMethod(method);

		default_headers = {
			"Content-Type":"application/json"
		}

		if data and method != "GET":
			if isinstance(data, dict):
				data = json.encode(data)
			default_headers["Content-Length"] = len(data)
			c.setData(data)

		header.update(default_headers)

		c.setHeader([i+": "+str(header[i]) for i in header])

		c.setUrl(url)

		if async:
			return c

		try:
			c.execute()
		except:
			# throw backend connection error
			pass

		return c.getResponse()