import pycurl
from io import BytesIO

from ...library import json

class BACKEND_API(object):

	@classmethod
	def get(cls, path, header={}):
		return cls.__excecute(method="GET", path=path, header=header)

	@classmethod
	def post(cls, path, data = None, header={}):
		return cls.__excecute(method="POST", path=path, data=data, header=header)

	@classmethod
	def put(cls, path, data = None, header={}):
		return cls.__excecute(method="PUT", path=path, data=data, header=header)

	@classmethod
	def delete(cls, path, data, header={}):
		return cls.__excecute(method="DELETE", path=path, data=data, header=header)

	@classmethod
	def __excecute(cls, method, path, data = None, header):
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
		c.setopt(c.URL, 'http://127.0.0.1:3032')

		c.setopt(c.WRITEDATA, http_buffer)
		try:
			c.perform()
		except:
			# throw backend connection error
			pass

		httpcode = c.getinfo(HTTP_CODE);

		# response_code = c.getinfo(RESPONSE_CODE);

		# os_errno = c.getinfo(OS_ERRNO);

		c.close()

		response = http_buffer.getvalue()
		http_buffer.close()

		if httpcode in [500,501,502,503,504,505]:
			# throw backend api server error
			pass

		return {
			"response" => response,
			# "error_no" => os_errno,
			"httpcode" => httpcode
		};