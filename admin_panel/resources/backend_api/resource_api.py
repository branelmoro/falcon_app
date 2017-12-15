import pycurl
from io import BytesIO

class BACKEND_API(object):

	@classmethod
	def get(cls, path, header={}):
		return cls.__excecute(method="GET", path=path, header=header)

	@classmethod
	def post(cls, path, data = null, header={}):
		return cls.__excecute(method="POST", path=path, data=data, header=header)

	@classmethod
	def put(cls, path, data = null, header={}):
		return cls.__excecute(method="PUT", path=path, data=data, header=header)

	@classmethod
	def delete(cls, path, data, header={}):
		return cls.__excecute(method="DELETE", path=path, data=data, header=header)

	@classmethod
	def __excecute(cls, method, path, data = None, header={}):
		http_buffer = BytesIO()
		c = pycurl.Curl()
		c.setopt(c.CUSTOMREQUEST, method);
		c.setopt(c.HTTPHEADER, ["Content-Type: application/json"])
		c.setopt(c.URL, 'http://pycurl.io/')
		c.setopt(c.WRITEDATA, http_buffer)
		c.perform()
		c.close()

		body = http_buffer.getvalue()
		http_buffer.close()
		pass