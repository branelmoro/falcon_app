import psycopg2
import time
# import sys

class pgException(Exception):
	"""Raise for my specific kind of exception"""

class pgLoadBalancer(object):
	__hosts = False
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
		cls.__hosts = {
			"master":{
				"host":"127.0.0.1",
				"username":"branelm",
				"password":"root",
				"database":"branelm",
				"port":5432
			},
			"slave":[
				{
					"host":"127.0.0.1",
					"username":"branelm",
					"password":"root",
					"database":"branelm",
					"port":5432
				},
				{
					"host":"127.0.0.1",
					"username":"branelm",
					"password":"root",
					"database":"branelm",
					"port":5432
				},
				{
					"host":"127.0.0.1",
					"username":"branelm",
					"password":"root",
					"database":"branelm",
					"port":5432
				},
				{
					"host":"127.0.0.1",
					"username":"branelm",
					"password":"root",
					"database":"branelm",
					"port":5432
				}
			]
		}

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

	@classmethod
	def disconnect_pg(cls, conn):
		conn.close()

class pgResultCursor(object):

	def __init__(self, cursor):
		self.__cursor = cursor
		self.__columns = None
		if cursor.description is not None:
			self.__columns = {value.name:cursor.description.index(value) for value in cursor.description}

	def getColumns(self):
		return self.__columns

	def getOneRecord(self):
		try:
			return self.__cursor.fetchone()
		except psycopg2.InterfaceError:
			print("cursor closed, hence failed to fetchone")

	def getManyRecord(self, size):
		try:
			return self.__cursor.fetchmany(size)
		except psycopg2.InterfaceError:
			print("cursor closed, hence failed to fetchmany")

	def getAllRecords(self):
		try:
			return self.__cursor.fetchall()
		except psycopg2.InterfaceError:
			print("cursor closed, hence failed to fetchall")

	def getArraySize(self):
		return self.__cursor.arraysize

	def getIterSize(self):
		return self.__cursor.itersize

	def setArraySize(self, size):
		self.__cursor.arraysize = size

	def setIterSize(self, size):
		self.__cursor.itersize = size

	def getRowNumber(self):
		return self.__cursor.rownumber

	def getLastInsertId(self):
		return self.__cursor.lastrowid

	def getStatusMessage(self):
		return self.__cursor.statusmessage

	def isClosed(self):
		return self.__cursor.closed

	def getLastQuery(self):
		return self.__cursor.query

	def closeCursor(self):
		self.__cursor.close()

	def __del__(self):
		print("closing result cursor")
		self.closeCursor()
		self.__cursor = None
		self.__columns = None

class pgQueryCursor(object):

	def __init__(self, conn, num, conntype):
		self.__connection = conn
		self.__num = num
		self.__type = conntype
		self.__cursor = self.__connection.cursor()

	def query(self,query,params=[]):
		# run query
		blnRun = True
		while blnRun:
			try:
				blnRun = False
				self.__cursor.execute(query, params)
			except psycopg2.OperationalError as e:
				# exc_type, exc_value, exc_traceback = sys.exc_info()
				self.__reConnectToDB()
				blnRun = True

			except psycopg2.InterfaceError as e:
				self.__reConnectToDB()
				blnRun = True

		return pgResultCursor(self.__cursor)

	def __reConnectToDB(self):
		if self.__type == "master":
			self.__connection, self.__num, self.__type = pgLoadBalancer.getDBConnection(True)
		else:
			self.__connection, self.__num, self.__type = pgLoadBalancer.getDBConnection(False)

		if self.__connection is False:
			raise pgException("unable to connect "+self.__type+" db")

		self.__cursor = self.__connection.cursor()

	# def multiquery(self,query,params):
	# 	# run multiple queries
	# 	result = self.__cursor.executemany(query, params)
	# 	return pgResultCursor(self.__cursor)

	def insert(self,table,data):
		pass

	def getBoundQuery(self,query,params):
		# cursor = self.__connection.cursor()
		return self.__cursor.mogrify(query, params)

	def closeCursor(self):
		self.__cursor.close()

	def commit():
		self.__connection.commit()

	def __del__(self):
		print("closing query cursor")
		self.__connection = None
		self.__num = None
		self.__type = None
		self.__cursor = None

class httpBase(object):

	def pgmaster(self):
		return self.__getConnector(True)

	def pgslave(self):
		return self.__getConnector(False)

	def __getConnector(self, is_master):
		conn, num, conntype = pgLoadBalancer.getDBConnection(is_master)
		return pgQueryCursor(conn, num, conntype)

	def pgtransaction(self):
		conn = pgLoadBalancer.init_transaction()
		return pgQueryCursor(conn, 0, "master")

	def __del__(self):
		print("closing http connection")
