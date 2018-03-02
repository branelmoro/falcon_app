import redis
import atexit

try:
	from ..env import env as enviornment
except ImportError:
	enviornment = "production"

if enviornment == "local":
	from ..config_local import REDIS_DB_CREDENTIALS
elif enviornment == "production":
	from ..config_production import REDIS_DB_CREDENTIALS

db = 15
for dbname in REDIS_DB_CREDENTIALS:
	REDIS_DB_CREDENTIALS[dbname]["db"] = db
	db = db - 1


class setupDB():

	def setDB(self):
		for dbname in REDIS_DB_CREDENTIALS:
			redis.StrictRedis(**REDIS_DB_CREDENTIALS[dbname]).flushdb()

	def doCleanUp(self):
		print("DOING TDD REDIS CLEANUP")
		self.setDB()
		print("DONE")

REDIS_SETUP = setupDB()
REDIS_SETUP.setDB()

atexit.register(REDIS_SETUP.doCleanUp)