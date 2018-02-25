import redis
from . import setup

if setup.enviornment == "local":
	from ..config_local import REDIS_DB_CREDENTIALS
elif setup.enviornment == "production":
	from ..config_production import REDIS_DB_CREDENTIALS

db = 15
for dbname in REDIS_DB_CREDENTIALS:
	REDIS_DB_CREDENTIALS[dbname]["db"] = db
	db = db - 1


class setupDB():

	def doCleanUp(self):
		for dbname in REDIS_DB_CREDENTIALS:
			redis.StrictRedis(**REDIS_DB_CREDENTIALS[dbname]).flushdb()

REDIS_SETUP = setupDB()
REDIS_SETUP.doCleanUp()

setup.CLEANUPQUEUE.append(REDIS_SETUP)