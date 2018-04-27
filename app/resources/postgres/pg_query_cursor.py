from psycopg2 import InterfaceError as interfaceError
from psycopg2 import OperationalError as operationalError
from .pg_exception import pgException
from .pg_result_cursor import pgResultCursor
from .pg_load_balancer import pgLoadBalancer


class pgQueryCursor(object):

	def __init__(self, connection_pool, is_master, autocommit=True):
		self.__connection_pool = connection_pool
		self.__is_master = is_master
		self.__autocommit = autocommit
		self.__pullConnection()

	def __pullConnection(self):
		self.__connection = self.__connection_pool.getconn()
		self.__connection.autocommit = self.__autocommit

	def __deleteConnection(self):
		self.__connection_pool.putconn(conn=self.__connection, close=True)

	def __leaveConnection(self):
		self.__connection_pool.putconn(conn=self.__connection, close=False)

	def query(self,query,params=[]):
		# run query

		if self.__autocommit:

			while True:
				try:
					cursor = self.__connection.cursor()
					cursor.execute(query, params)
					break
				except operationalError as e:
					# exc_type, exc_value, exc_traceback = sys.exc_info()
					self.__resetConnectionPull()
				except interfaceError as e:
					self.__resetConnectionPull()

			return pgResultCursor(cursor=cursor, connection_pool=self.__connection_pool)
		else:
			cursor = self.__connection.cursor()
			cursor.execute(query, params)
			return pgResultCursor(cursor=cursor, connection_pool=self.__connection_pool)

	def __resetConnectionPull(self):
		self.__deleteConnection()
		self.__connection_pool = pgLoadBalancer.getConnectionPull(self.__is_master)
		self.__pullConnection()

	# def multiquery(self,query,params):
	# 	# run multiple queries
	# 	result = self.__cursor.executemany(query, params)
	# 	return pgResultCursor(self.__cursor)

	def insert(self,table,data):
		pass

	def getBoundQuery(self,query,params):
		cursor = self.__connection.cursor()
		qry = cursor.mogrify(query, params)
		cursor.close()
		self.__leaveConnection()
		return qry

	# def closeCursor(self):
	# 	self.__cursor.close()

	def commit(self):
		if not self.__autocommit:
			self.__connection.commit()
			self.__leaveConnection()

	def __del__(self):
		print("closing query cursor")