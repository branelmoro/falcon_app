import psycopg2
import time
from .pg_exception import pgException
from ...config import PGDB1

class pgLoadBalancer(object):
	__hosts = PGDB1
	__blnConnectedToAll = False
	__masterConn = False
	__slaveConns = []
	__currentSlave = False

	@classmethod
	def setConfig(cls):
		if cls.__hosts is None:
			while cls.__hosts is None:
				# infinite loop to avoid multiple static connections, wait for 1 second
				time.sleep(1)
			return
		if cls.__hosts is not False:
			return
		cls.__hosts = None
		# code to fetch database credentials
		cls.__hosts = PGDB1

	@classmethod
	def getDBConnection(cls,bln):
		if cls.__blnConnectedToAll is False:
			cls.connect_all_servers()
		if bln is True:
			if cls.__masterConn is False or cls.__masterConn is None or cls.__masterConn.closed != 0:
				print("reconnecting master")
				cls.connect_to_master()
			if cls.__masterConn is False:
				raise pgException("unable to connect master db")
			return (cls.__masterConn,0,"master")
		else:
			cls.select_slave()
			return (cls.__slaveConns[cls.__currentSlave],cls.__currentSlave,"slave")

	@classmethod
	def select_slave(cls):
		connectFlag = True
		loopcount = 0
		while connectFlag:
			if loopcount > len(cls.__hosts["slave"]):
				raise pgException("unable to connect all slave db")
			connectFlag = False
			cls.__currentSlave = cls.__currentSlave + 1
			if cls.__currentSlave == len(cls.__slaveConns):
				cls.__currentSlave = 0
			if cls.__slaveConns[cls.__currentSlave] is False or cls.__slaveConns[cls.__currentSlave] is None or cls.__slaveConns[cls.__currentSlave].closed != 0:
				connectFlag = True
				print("reconnecting to slave "+ str(cls.__currentSlave))
				cls.reconnect_slave(cls.__currentSlave)
			loopcount = loopcount + 1

	@classmethod
	def connect_all_servers(cls):
		# set database config
		cls.setConfig();
		#connect to all slave and store in array
		cls.connect_to_master()
		cls.connect_to_slaves()
		cls.__blnConnectedToAll = True

	@classmethod
	def connect_to_master(cls):
		print("connecting to master")
		if cls.__masterConn is None:
			while cls.__masterConn is None:
				# infinite loop to avoid multiple static connections, wait for 1 second
				time.sleep(1)
			return
		if cls.__masterConn is not False:
			cls.__masterConn.close()
		cls.__masterConn = None
		cls.__masterConn = cls.connect_to_pg(cls.__hosts["master"])

	@classmethod
	def connect_to_slaves(cls):
		print("connecting to slaves")
		if cls.__currentSlave is None:
			while cls.__currentSlave is None:
				# infinite loop to avoid multiple static connections, wait for 1 second
				time.sleep(1)
			return
		for conn in cls.__slaveConns:
			conn.close()
		cls.__slaveConns = []
		cls.__currentSlave = None

		for host in cls.__hosts["slave"]:
			cls.__slaveConns.append(cls.connect_to_pg(host))
		cls.__currentSlave = len(cls.__slaveConns) - 1

	@classmethod
	def connect_to_pg(cls, host, autocommit=True):
		try:
			conn = psycopg2.connect(database=host["database"], user=host["username"], password=host["password"], host=host["host"], port=host["port"])
			conn.autocommit = autocommit
		except psycopg2.Error as e:
			print("unable to connect database")
			print(host)
			print(e)
			print(psycopg2.Error)
			return False
		return conn;

	@classmethod
	def reconnect_slave(cls,num):
		if cls.__slaveConns[num] is None:
			while cls.__slaveConns[num] is None:
				# infinite loop to avoid multiple static connections, wait for 1 second
				time.sleep(1)
			return
		if cls.__slaveConns[num] is not None and cls.__slaveConns[num] is not False:
			cls.__slaveConns[num].close()
		cls.__slaveConns[num] = None
		cls.__slaveConns[num] = cls.connect_to_pg(cls.__hosts["slave"][num])

	@classmethod
	def init_transaction(cls):
		conn = cls.connect_to_pg(cls.__hosts["master"], False)
		if cls.__currentSlave is False:
			raise pgException("unable to connect master db for transaction")
		return conn

	def getHosts(self):
		return self.__hosts

	@classmethod
	def disconnect_pg(cls, conn):
		conn.close()