from .pg_load_balancer import pgLoadBalancer
from .pg_query_cursor import pgQueryCursor

class pgBase(object):

	def master(self):
		return self.__getConnector(True)

	def slave(self):
		return self.__getConnector(False)

	def __getConnector(self, is_master):
		conn, num, conntype = pgLoadBalancer.getDBConnection(is_master)
		return pgQueryCursor(conn, num, conntype)

	def transaction(self):
		conn = pgLoadBalancer.init_transaction()
		return pgQueryCursor(conn, 0, "master")