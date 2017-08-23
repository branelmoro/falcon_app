class serverException(Exception):
	"""Raise for server errors"""
	def __init__(self, params, http_status):
		self.__params = params
		self.__http_status = http_status

	def getErrorMessages(self):
		return self.__params

	def getHttpStatus(self):
		return self.__http_status

class serverException_500(clientException):
	"""This will handle all http 500 exception, server error"""
	def __init__(self, params):
		clientException.__init__(self,params,500)


class clientException(Exception):
	"""Raise for client errors"""
	def __init__(self, params, http_status):
		self.__params = params
		self.__http_status = http_status
		# super.__init__(self,"Invalid Data Supplied by Client")

	def getErrorMessages(self):
		return self.__params

	def getHttpStatus(self):
		return self.__http_status



class clientException_400(clientException):
	"""This will handle all http 400 exception, invalid request"""
	def __init__(self, params):
		clientException.__init__(self,params,400)



class clientException_401(clientException):
	"""This will handle all http 401 exception, unauthorised user"""
	def __init__(self, params):
		clientException.__init__(self,params,401)


class clientException_403(clientException):
	"""This will handle all http 405 exception, request method not allowed"""
	def __init__(self, params):
		clientException.__init__(self,params,403)


class clientException_404(clientException):
	"""This will handle all http 404 exception, url not found allowed"""
	def __init__(self, params):
		clientException.__init__(self,params,404)


class clientException_405(clientException):
	"""This will handle all http 405 exception, request method not allowed"""
	def __init__(self, params):
		clientException.__init__(self,params,405)


class clientException_406(clientException):
	"""This will handle all http 405 exception, request method not allowed"""
	def __init__(self, params):
		clientException.__init__(self,params,406)