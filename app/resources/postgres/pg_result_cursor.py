from psycopg2 import InterfaceError as interfaceError

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
		except interfaceError:
			print("cursor closed, hence failed to fetchone")
		except:
			return []

	def getManyRecord(self, size):
		try:
			return self.__cursor.fetchmany(size)
		except interfaceError:
			print("cursor closed, hence failed to fetchmany")
		except:
			return []

	def getAllRecords(self):
		try:
			return self.__cursor.fetchall()
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
		self.__cursor.close()

	def __del__(self):
		print("closing result cursor")
		self.closeCursor()
		self.__cursor = None
		self.__columns = None