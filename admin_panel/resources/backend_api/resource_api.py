import pycurl
from io import BytesIO

from ...library import json
from ...config import BACKEND_API_URL

class CUSTOM_CURL(pycurl.Curl):

	def __init__(self):
		super.__init__()
		self.__buffer = BytesIO()
		self.setopt(self.WRITEDATA, self.__buffer)
		self.__api_callback = None
		self.__next_api = {}
		self.__details = {}

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
			obj_id = id(next_api)
			if obj_id not in self.__next_api:
				self.__next_api[obj_id] = self.__next_api
				i.addCount()

	def del_next(self):
		for i in self.__next_api:
			self.__next_api[i].delCount()

	def update_next(self):
		self.__next_api = {id(self.__next_api[i]):self.__next_api[i] for i in self.__next_api if self.__next_api[i].getCount() > 0}

	def get_next_executable(self):
		return [self.__next_api[i].get() for i in self.__next_api if self.__next_api[i].getCount() == 0]	

	def get_next(self):
		return [self.__next_api[i] for i in self.__next_api]

	def getResponse(self):
		# os_errno = self.getinfo(self.OS_ERRNO);
		data = {
			"response":self.__buffer.getvalue(),
			# "error_no" => os_errno,
			"httpcode":self.getinfo(self.HTTP_CODE)
		}
		return data

	def doCleanUp(self)
		self.__api_callback = None
		self.__next_api = {}
		self.__details = {}
		self.__buffer.close()
		self.close()

	def __del__(self):
		super.__del__()
		self.doCleanUp()




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
	def execute(cls, method, url, data = None, header, async=False):
		# if async:
		# 	c = CUSTOM_CURL()
		# else:
		# 	c = CUSTOM_CURL(pycurl.Curl)
		c = CUSTOM_CURL()
		c.setopt(c.CUSTOMREQUEST, method);

		default_headers = {
			"Content-Type":"application/json"
		}

		if data and method != "GET":
			data = json.encode(data);
			default_headers["Content-Length"] = len(data)
			c.setopt(c.POSTFIELDS, data);

		header.update(default_headers)

		c.setopt(c.HTTPHEADER, [i+": "+str(header[i]) for i in header])

		# c.setopt(c.HTTPHEADER, ["Content-Type: application/json"])
		c.setopt(c.URL, BACKEND_API_URL)

		if async:
			return c

		try:
			c.perform()
		except:
			# throw backend connection error
			pass

		return c.getResponse()