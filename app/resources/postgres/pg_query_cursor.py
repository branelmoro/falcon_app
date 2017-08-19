from psycopg2 import InterfaceError as interfaceError
from psycopg2 import OperationalError as operationalError
from .pg_exception import pgException
from .pg_result_cursor import pgResultCursor
from .pg_load_balancer import pgLoadBalancer

class pgQueryCursor(object):

	def __init__(self, conn, num, conntype):
		self.__connection = conn
		self.__num = num
		self.__type = conntype
		if self.__connection.autocommit:
			self.__cursor = self.__connection.cursor()

	def query(self,query,params=[]):
		# run query

		# condition to handle transaction
		if not self.__connection.autocommit:
			cursor = self.__connection.cursor()
			cursor.execute(query, params)
			return pgResultCursor(cursor)

		blnRun = True
		while blnRun:
			try:
				blnRun = False
				self.__cursor.execute(query, params)
			except operationalError as e:
				# exc_type, exc_value, exc_traceback = sys.exc_info()
				self.__reConnectToDB()
				blnRun = True

			except interfaceError as e:
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

	# def closeCursor(self):
	# 	self.__cursor.close()

	def commit(self):
		if not self.__connection.autocommit:
			self.__connection.commit()
			self.__connection.close()

	def __del__(self):
		print("closing query cursor")
		self.__connection = None
		self.__num = None
		self.__type = None
		self.__cursor = None