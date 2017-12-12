import pycurl

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
		pass