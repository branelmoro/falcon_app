import time
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from . import setup


if setup.enviornment == "local":
	from ..config_local import PGDB1
elif setup.enviornment == "production":
	from ..config_production import PGDB1

PG_CONNECTION_DETAIL = PGDB1["master"].copy()
del PG_CONNECTION_DETAIL["minconn"]
del PG_CONNECTION_DETAIL["maxconn"]


class setupDB():

	def __init__(self):
		self.__dbname = "laborstack_" + str(time.time()).replace(".", "_")

	def getDBName(self):
		return self.__dbname

	def __getConnection(self):
		con = connect(**PG_CONNECTION_DETAIL)
		con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		return con

	def __closeConnection(self, con):
		con.close()

	def createDATABASE(self):
		con = self.__getConnection()
		cur = con.cursor()
		sql = """
		CREATE DATABASE """+self.__dbname+""" WITH TEMPLATE laborstack OWNER """+PG_CONNECTION_DETAIL["user"]+""" CONNECTION LIMIT = -1;
		"""
		cur.execute(sql)
		cur.close()
		self.__closeConnection(con)

	def doCleanUp(self):
		con = self.__getConnection()
		cur = con.cursor()
		sql = """
		DROP DATABASE """+self.__dbname+""";
		"""
		cur.execute(sql)
		cur.close()
		self.__closeConnection(con)

PGDB1_SETUP = setupDB()
PGDB1_SETUP.createDATABASE()
dbname = PGDB1_SETUP.getDBName()

setup.CLEANUPQUEUE.append(PGDB1_SETUP)

DB_DETAILS = PG_CONNECTION_DETAIL.copy()
DB_DETAILS["database"] = dbname
DB_DETAILS["minconn"] = 0
DB_DETAILS["maxconn"] = 2

PGDB1 = {
	"master":DB_DETAILS,
	"slave":[
		DB_DETAILS,
		DB_DETAILS,
		DB_DETAILS
	]
}