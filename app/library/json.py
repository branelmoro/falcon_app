import json

class jsonLib:

	@classmethod
	def encode(cls, data):
		return json.dumps(data)

	@classmethod
	def decode(cls, data):
		return json.loads(data)