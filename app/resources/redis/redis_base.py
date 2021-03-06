import redis
from ...config import REDIS_DB_CREDENTIALS
import atexit

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

	__connection_pool = {}
	__dbconfig = REDIS_DB_CREDENTIALS

	@classmethod
	def createConnectionPool(cls):
		print("CREATING REDIS CONNECTION POOL")
		for dbName in cls.__dbconfig:
			cls.__connection_pool[dbName] = redis.BlockingConnectionPool(**cls.__dbconfig[dbName])
		print("DONE")

	@classmethod
	def deleteConnectionPool(cls):
		print("CLOSING REDIS CONNECTION POOL")
		for dbName in cls.__dbconfig:
			cls.__connection_pool[dbName].disconnect()
		print("DONE")

	@classmethod
	def is_validDB(cls,dbName):
		if not dbName in cls.__connection_pool:
			raise rdException({"redis":"Invalid redis database server provided"})

	@classmethod
	def getDBConnection(cls, dbName):
		return redis.StrictRedis(connection_pool=cls.__connection_pool[dbName])

redisBase.createConnectionPool()

atexit.register(redisBase.deleteConnectionPool)


class redisCrud(object):

	__dbname = None

	def __init__(self, dbName=None):
		redisBase.is_validDB(dbName)
		self.__dbname = dbName

	def getConnection(self,is_master=True):
		return redisBase.getDBConnection(self.__dbname)

	#override all StrictRedis methods
	# key/value commands	
	def get(self, key):
		data = self.getConnection().get(key)
		if data:
			return data.decode('utf-8')
		else:
			return data

	def set(self, key, value, expiry = None):
		# print(value);
		if expiry is None:
			return self.getConnection().set(key, value)
		else:
			return self.getConnection().set(key, value, expiry)

	def delete(self, key):
		return self.getConnection().delete(key)

	def exists(self, key):
		return self.getConnection().exists(key)

	def expire(self, key, expiry):
		return self.getConnection().expire(key, expiry)

	def ttl(self, key):
		return self.getConnection().ttl(key)


	# list commands
	def lpush(self, key, value):
		return self.getConnection().lpush(key, value)

	def rpush(self, key, value):
		return self.getConnection().rpush(key, value)

	def lrange(self, key, start=0, end=-1):
		return [i.decode('utf-8') for i in self.getConnection().lrange(key, start, end)]


	# set commands
	def sadd(self, key, value):
		return self.getConnection().sadd(key, value)

	def srem(self, key, value):
		return self.getConnection().srem(key, value)

	def sismember(self, key, value):
		return self.getConnection().sismember(key, value)

	def smembers(self, key):
		return {i.decode('utf-8') for i in self.getConnection().smembers(key)}


	# hash/object commands
	def hset(self, hashkey, key, value):
		return self.getConnection().hset(hashkey, key, value)
	
	def hget(self, hashkey, key):
		data = self.getConnection().hget(hashkey, key)
		if data:
			return data.decode('utf-8')
		else:
			return data
	
	def hmset(self, hashkey, key_value):
		return self.getConnection().hmset(hashkey, key_value)
	
	def hgetall(self, key):
		data = self.getConnection().hgetall(key)
		if data:
			return {k.decode('utf-8'):data[k].decode('utf-8') for k in data}
		else:
			return data
	
	def hdel(self, hashkey, key):
		return self.getConnection().hdel(hashkey, key)

	def hexists(self, hashkey, key):
		return self.getConnection().hexists(hashkey, key)