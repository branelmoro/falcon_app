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
		self.__next_api = None

	def get_buffer(self):
		return self.__buffer

	def set_callback(self, callback):
		self.__api_callback = callback

	def get_callback(self):
		return self.__api_callback

	def set_next(self, next):
		self.__next_api = next

	def get_next(self):
		return self.__next_api

	def __getResponseCode(self):
		httpcode = self.getinfo(self.HTTP_CODE);
		if httpcode in [500,501,502,503,504,505]:
			self.__doCleanUp()
			# throw backend api server error
			pass
		return httpcode;

	def __getResponseBody(self):
		return self.__buffer.getvalue()

	def getResponse(self):
		# os_errno = self.getinfo(self.OS_ERRNO);
		data = {
			"response":self.__getResponseBody(),
			# "error_no" => os_errno,
			"httpcode":self.__getResponseCode()
		}
		self.__doCleanUp()
		return data

	def __doCleanUp(self)
		self.__buffer.close()
		self.close()

	def __del__(self):
		self.__doCleanUp()




class BACKEND_API(object):

	@classmethod
	def get(cls, path, header={}, async=False):
		return cls.__excecute(method="GET", path=path, header=header, async=async)

	@classmethod
	def post(cls, path, data = None, header={}, async=False):
		return cls.__excecute(method="POST", path=path, data=data, header=header, async=async)

	@classmethod
	def put(cls, path, data = None, header={}, async=False):
		return cls.__excecute(method="PUT", path=path, data=data, header=header, async=async)

	@classmethod
	def delete(cls, path, data, header={}, async=False):
		return cls.__excecute(method="DELETE", path=path, data=data, header=header, async=async)

	@classmethod
	def __excecute(cls, method, path, data = None, header, async=False):
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