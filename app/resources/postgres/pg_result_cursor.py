from psycopg2 import InterfaceError as interfaceError

class pgResultCursor(object):

	def __init__(self, cursor, connection_pool):
		self.__connection_pool = connection_pool
		self.__cursor = cursor
		self.__columns = None
		if cursor.description is not None:
			self.__columns = {value.name:cursor.description.index(value) for value in cursor.description}
		else:
			if self.__cursor.connection.autocommit:
				self.__leaveConnection()

	def __leaveConnection(self):
		if self.__cursor.connection.autocommit and self.__connection_pool is not None:
			self.__connection_pool.putconn(conn=self.__cursor.connection, close=False)
			self.__connection_pool = None
		self.closeCursor()

	def getColumns(self):
		return self.__columns

	def getOneRecord(self):
		try:
			record = self.__cursor.fetchone()
			if record is None:
				self.__leaveConnection()
			return record
		except interfaceError:
			print("cursor closed, hence failed to fetchone")
		except:
			return []

	def getManyRecord(self, size):
		try:
			records = self.__cursor.fetchmany(size)
			if not records:
				self.__leaveConnection()
			return records
		except interfaceError:
			print("cursor closed, hence failed to fetchmany")
		except:
			return []

	def getAllRecords(self):
		try:
			records =  self.__cursor.fetchall()
			self.__leaveConnection()
			return records
		except interfaceError:
			print("cursor closed, hence failed to fetchall")
		except:
			return []

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
		# return self.__cursor.lastrowid
		# use RETURNING id in insert query
		row = self.getOneRecord()
		if len(row) == 1:
			return row[0]
		else:
			return 0

	def getStatusMessage(self):
		return self.__cursor.statusmessage

	def isClosed(self):
		return self.__cursor.closed

	def getLastQuery(self):
		return self.__cursor.query

	def closeCursor(self):
		if not self.__cursor.closed:
			self.__cursor.close()

	def __del__(self):
		print("closing result cursor")
		self.__leaveConnection()
		self.__cursor = None
		self.__columns = None