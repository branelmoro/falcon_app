import psycopg2.pool
import time
from .pg_exception import pgException
from ...config import PGDB1

class pgLoadBalancer(object):
	__hosts = PGDB1
	__connectionPull = {}

	@classmethod
	def initConnectionPull(cls):
		dbPull = {}
		dbPull["master"] = psycopg2.pool.ThreadedConnectionPool(**cls.__hosts["master"])

		slave_pull_list = []
		for slave_detail in cls.__hosts["slave"]:
			slave_pull_list.append(psycopg2.pool.ThreadedConnectionPool(**slave_detail))

		dbPull["slave_count"] = len(slave_pull_list)
		dbPull["slave"] = cls.__slave_selector(slave_pull_list)

		cls.__connectionPull["PGDB1"] = dbPull

	@classmethod
	def deleteConnectionPull(cls):
		for db_name in cls.__connectionPull:
			cls.__connectionPull[db_name]["master"].closeall()
			while cls.__connectionPull[db_name]["slave_count"] > 0:
				slave_pull = next(cls.__connectionPull[db_name]["slave"])
				slave_pull.closeall()
				cls.__connectionPull[db_name]["slave_count"] = cls.__connectionPull[db_name]["slave_count"]-1
		cls.__connectionPull = {}

	@classmethod
	def getConnectionPull(cls, is_master=False, db_name="PGDB1"):
		if is_master:
			pool = cls.__connectionPull[db_name]["master"]
		else:
			pool = next(cls.__connectionPull[db_name]["slave"])
		return pool

	@classmethod
	def __slave_selector(cls, slave_pull_list):
		while True:
			for pool in slave_pull_list:
				yield pool


pgLoadBalancer.initConnectionPull()