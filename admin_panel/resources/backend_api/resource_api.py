import pycurl
from io import BytesIO

class BACKEND_API(object):

	@classmethod
	def get(cls, path):
		return cls.getDataFromApi("GET", path)

	@classmethod
	def post(cls, path, data = null):
		return cls.getDataFromApi("POST", path, data)

	@classmethod
	def put(cls, path, data = null):
		return cls.getDataFromApi("PUT", path, data)

	@classmethod
	def delete(cls, path, data):
		return cls.getDataFromApi("DELETE", path, data)

	@classmethod
	def __excecute(cls):
		http_buffer = BytesIO()
		c = pycurl.Curl()
		c.setopt(c.URL, 'http://pycurl.io/')
		c.setopt(c.WRITEDATA, http_buffer)
		c.perform()
		c.close()

		body = http_buffer.getvalue()
		http_buffer.close()
		pass