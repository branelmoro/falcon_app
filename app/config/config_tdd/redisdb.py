import redis
from . import cleanup

REDIS_DB_CREDENTIALS = {
	"access_tokenDb" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":15
	},
	"refresh_tokenDb" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":14
	},
	"access_scopeDb" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":13
	},
	"sessionDb" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":12
	},
	"skillDb" : {
		"host":"127.0.0.1",
		"port":6379,
		"db":11
	}
}

class setupDB():

	def doCleanUp(self):
		for dbname in REDIS_DB_CREDENTIALS:
			redis.StrictRedis(**REDIS_DB_CREDENTIALS[dbname]).flushdb()

REDIS_SETUP = setupDB()
REDIS_SETUP.doCleanUp()

cleanup.CLEANUPQUEUE.append(REDIS_SETUP)