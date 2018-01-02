import pycurl
from io import BytesIO

from ...library import json
from ...config import BACKEND_API_URL

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
		http_buffer = BytesIO()
		c = pycurl.Curl()
		c.setopt(c.CUSTOMREQUEST, method);

		default_headers = {
			"Content-Type":"application/json"
		}

		if data and method != "GET":
			data = json.encode($data);
			default_headers["Content-Length"] = len(data)
			c.setopt(c.POSTFIELDS, data);

		header.update(default_headers)

		c.setopt(c.HTTPHEADER, [i+": "+str(header[i]) for i in header])

		# c.setopt(c.HTTPHEADER, ["Content-Type: application/json"])
		c.setopt(c.URL, BACKEND_API_URL)

		c.setopt(c.WRITEDATA, http_buffer)

		if async:
			return (c, http_buffer)

		try:
			c.perform()
		except:
			# throw backend connection error
			pass

		httpcode = c.getinfo(c.HTTP_CODE);

		# response_code = c.getinfo(c.RESPONSE_CODE);

		# os_errno = c.getinfo(c.OS_ERRNO);

		c.close()

		response = http_buffer.getvalue()
		http_buffer.close()

		if httpcode in [500,501,502,503,504,505]:
			# throw backend api server error
			pass

		return {
			"response":response,
			# "error_no" => os_errno,
			"httpcode":httpcode
		};