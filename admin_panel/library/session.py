import random
import datetime
from ..resources.redis import redis as redisCrud
from . import json

try:
	from hashlib import blake2s
except ImportError:
	from pyblake2 import blake2s


SESSION_DB = redisCrud("client_sessionDb")

class SESSION(object):

	__session_id = None
	__session_key = "admin-session"
	__sessionData = {}

	__req = None
	__resp = None

	def __init__(self, container):
		self.__req = container.req
		self.__resp = container.resp
		# load session
		if self.__session_key in self.__req.cookies:
			if SESSION_DB.exists(self.__req.cookies[self.__session_key]):
				self.__sessionData = SESSION_DB.hgetall(self.__req.cookies[self.__session_key])
				self.__session_id = self.__req.cookies[self.__session_key]
			else:
				# session is expired hence unset cookie
				self.__resp.unset_cookie(self.__req.cookies[self.__session_key])

	def __isSessionIdLocked(self, session_id, data):
		conn = SESSION_DB.getConnection("client_sessionDb")
		pipe = conn.pipeline(transaction=True)
		pipe.watch(session_id)
		pipe.multi()
		pipe.hmset(session_id, data)
		pipe.execute()

	def __getHashKey(self, key):
		return blake2s(key.encode('utf-8')).hexdigest()

	def __generateUniqueIdFromKey(self, data):
		key = self.__getHashKey(str(random.random()) + str(datetime.datetime.now()))
		while SESSION_DB.exists(key):
			key = self.__getHashKey(key)
		while True:
			try:
				self.__isSessionIdLocked(session_id=key,data=data)
				self.__sessionData.update(data)
				break
			except:
				key = self.__getHashKey(key)
		return key

	def exists(self):
		return (self.__session_id is not None)

	def isUserLoggedIn(self):
		return self.exists() and "accessToken" in self.__sessionData

	def start(self, expiry = 900, data={}):
		self.__session_id = self.__generateUniqueIdFromKey(data=data)
		self.__resp.set_cookie(name=self.__session_key, value=self.__session_id, max_age=expiry, secure=(self.__req.protocol=="https"))
		# self.__resp.set_cookie(name=self.__session_key, value=self.__session_id, expires=None, max_age=900, domain=None, path=None, secure=None, http_only=True)

	def setData(self, data):
		self.__sessionData.update(data)
		SESSION_DB.hmset(self.__session_id, data)

	def getData(self):
		return self.__sessionData

	def set(self, key, value):
		self.__sessionData[key] = value
		SESSION_DB = hset(self.__session_id, key, value)

	def get(self, key):
		return self.__sessionData[key]

	def destroy(self):
		SESSION_DB.delete(self.__session_id)
		self.__resp.unset_cookie(self.__session_key)
		self.__session_id = None
		self.__sessionData = {}

	def refresh(self, data):
		sessionData = self.__sessionData
		sessionData.update(data)
		self.destroy()
		self.start(expiry = data["refreshTokenExpiry"], data=sessionData)