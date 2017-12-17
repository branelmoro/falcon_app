import random
import hashlib
import datetime
from ..resources.redis import redis as redisCrud
from . import json

SESSION_DB = redisCrud("sessionDb")

class Session(object):

	__session_id = None
	__session_key = "x-session"
	__sessionData = {}

	__req = None
	__res = None

	def __init__(self, req, res):
		self.__req = req
		self.__res = res
		# load session
		if self.__session_key in self.__req.cookies:
			if SESSION_DB.exists(self.__req.cookies[self.__session_key]):
				self.__sessionData = SESSION_DB.hgetall(self.__req.cookies[self.__session_key])
				self.__session_id = self.__req.cookies[self.__session_key];
			else:
				# session is expired hence unset cookie
				self.__res.unset_cookie(self.__req.cookies[self.__session_key])

	def __generateUniqueIdFromKey(self):
		key = hashlib.md5(str(random.random()) + str(datetime.datetime.now()))
		while SESSION_DB.exists(key):
			key = hashlib.md5(key)
		return key

	def exists(self):
		return (self.__session_id is not None)

	def start(self, expiry = 900, data={}):
		self.__session_id = self.__generateUniqueIdFromKey()
		self.__res.set_cookie(name=self.__session_key, value=self.__session_id, max_age=expiry)
		# self.__res.set_cookie(name=self.__session_key, value=self.__session_id, expires=None, max_age=900, domain=None, path=None, secure=None, http_only=True)
		if data:
			self.setData(data)

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
		self.__res.unset_cookie(self.__session_id)
		self.__session_id = None;
		self.__sessionData = {};

	def refresh(self, data):
		sessionData = self.__sessionData
		sessionData.update(data)
		self.destroy()
		self.start(expiry = data["refreshTokenExpiry"], data=sessionData)