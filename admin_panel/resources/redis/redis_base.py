import redis
from ...config import REDIS_DB_CREDENTIALS

# from app import exception as appException

class rdException(Exception):
	"""Raise for my specific kind of redis exception"""

"""
structure of shards and replica(may be required in future)
{
	# dbName
	"tokenDb":[
		# shard 1
		{
			"host":"127.0.0.1",
			"port":6379,
			"db":0,
			"replica":[
				# replica 1
				{
					"host":"127.0.0.1",
					"port":6379
				},
				# replica 1
				{
					"host":"127.0.0.1",
					"port":6379
				}
			]
		},
		# shard 2
		{
			"host":"127.0.0.1",
			"port":6379,
			"db":0,
			"replica":[
				{
					"host":"127.0.0.1",
					"port":6379
				},
				{
					"host":"127.0.0.1",
					"port":6379
				}
			]
		}
	]
}
Accordingly changes need to be done in code to handle connection to all shards and replicas
"""

class redisBase(object):

	__connections = {}
	__dbconfig = REDIS_DB_CREDENTIALS

	@classmethod
	def setConfig(cls):
		cls.__dbconfig = {
			"access_tokenDb" : {
				"host":"127.0.0.1",
				"port":6379,
				"db":0
			},
			"refresh_tokenDb" : {
				"host":"127.0.0.1",
				"port":6379,
				"db":1
			},
			"access_scopeDb" : {
				"host":"127.0.0.1",
				"port":6379,
				"db":2
			},
			"sessionDb" : {
				"host":"127.0.0.1",
				"port":6379,
				"db":3
			},
			"skillDb" : {
				"host":"127.0.0.1",
				"port":6379,
				"db":5
			}
		}
		pass

	@classmethod
	def is_validDB(cls,dbName):
		# cls.setConfig()
		if not dbName in cls.__dbconfig:
			raise rdException({"redis":"Invalid redis database server provided"})

	@classmethod
	def getDBConnection(cls, dbName):
		if dbName in cls.__connections:
			return cls.__connections[dbName];
		else:
			if dbName not in cls.__dbconfig:
				raise rdException({"redis":"Invalid redis database server provided"})
			cls.__connections[dbName] = cls.connectRedis(cls.__dbconfig[dbName]["host"],cls.__dbconfig[dbName]["port"],cls.__dbconfig[dbName]["db"])
			return cls.__connections[dbName]

	@classmethod
	def getFreshConnection(cls, dbName):
		return cls.connectRedis(cls.__dbconfig[dbName]["host"],cls.__dbconfig[dbName]["port"],cls.__dbconfig[dbName]["db"])

	@classmethod
	def connectRedis(cls, host, port=6379, db=0, password=None, socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', decode_responses=False, unix_socket_path=None):
		# return redis.StrictRedis(host, port, db, password, socket_timeout, connection_pool, charset, errors, decode_responses, unix_socket_path)
		return redis.StrictRedis(host, port, db, password, socket_timeout, connection_pool, charset)

	@classmethod
	def reconnectDB(cls, dbName):
		if dbName not in cls.__dbconfig:
			raise rdException({"redis":"Invalid redis database server provided"})
		cls.__connections[dbName] = cls.connectRedis(cls.__dbconfig[dbName]["host"],cls.__dbconfig[dbName]["port"],cls.__dbconfig[dbName]["db"])
		return cls.__connections[dbName]



class redisCrud(object):

	__dbname = None

	def __init__(self, dbName=None):
		redisBase.is_validDB(dbName)
		self.__dbname = dbName

	def __getDBConnection(self,is_master=True):
		return redisBase.getDBConnection(self.__dbname)

	def __getReConnection(self,is_master=True):
		return redisBase.reconnectDB(self.__dbname)

	@classmethod
	def getConnection(self, dbName=None):
		redisBase.is_validDB(dbName)
		return redisBase.getFreshConnection(dbName)

	#override all StrictRedis methods
	# key/value commands	
	def get(self, key):
		try:
			data = self.__getDBConnection().get(key)
		except:
			data = self.__getReConnection().get(key)
		if data:
			return data.decode()
		else:
			return data

	def set(self, key, value, expiry = None):
		# print(value);
		if expiry is None:
			try:
				return self.__getDBConnection().set(key, value)
			except:
				return self.__getReConnection().set(key, value)
		else:
			try:
				return self.__getDBConnection().set(key, value, expiry)
			except:
				return self.__getReConnection().set(key, value, expiry)

	def delete(self, key):
		try:
			return self.__getDBConnection().delete(key)
		except:
			return self.__getReConnection().delete(key)

	def exists(self, key):
		try:
			return self.__getDBConnection().exists(key)
		except:
			return self.__getReConnection().exists(key)

	def expire(self, key, expiry):
		try:
			return self.__getDBConnection().expire(key, expiry)
		except:
			return self.__getReConnection().expire(key, expiry)

	def ttl(self, key):
		try:
			return self.__getDBConnection().ttl(key)
		except:
			return self.__getReConnection().ttl(key)


	# set commands
	def sadd(self, key, value):
		try:
			return self.__getDBConnection().sadd(key, value)
		except:
			return self.__getReConnection().sadd(key, value)

	def srem(self, key, value):
		try:
			return self.__getDBConnection().srem(key, value)
		except:
			return self.__getReConnection().srem(key, value)

	def sismember(self, key, value):
		try:
			return self.__getDBConnection().sismember(key, value)
		except:
			return self.__getReConnection().sismember(key, value)

	def smembers(self, key):
		try:
			return self.__getDBConnection().smembers(key)
		except:
			return self.__getReConnection().smembers(key)


	# hash/object commands
	def hset(self, hashkey, key, value):
		try:
			return self.__getDBConnection().hset(hashkey, key, value)
		except:
			return self.__getReConnection().hset(hashkey, key, value)
	
	def hget(self, hashkey, key):
		try:
			data = self.__getDBConnection().hget(hashkey, key)
		except:
			data = self.__getReConnection().hget(hashkey, key)
		if data:
			return data.decode()
		else:
			return data
	
	def hmset(self, hashkey, key_value):
		try:
			return self.__getDBConnection().hmset(hashkey, key_value)
		except:
			return self.__getReConnection().hmset(hashkey, key_value)
	
	def hgetall(self, key):
		try:
			data = self.__getDBConnection().hgetall(key)
		except:
			data = self.__getReConnection().hgetall(key)
		if data:
			return {k.decode():data[k].decode() for k in data}
		else:
			return data
	
	def hdel(self, hashkey, key):
		try:
			return self.__getDBConnection().hdel(hashkey, key)
		except:
			return self.__getReConnection().hdel(hashkey, key)

	def hexists(self, hashkey, key):
		try:
			return self.__getDBConnection().hexists(hashkey, key)
		except:
			return self.__getReConnection().hexists(hashkey, key)