from .pg_load_balancer import pgLoadBalancer
from .pg_query_cursor import pgQueryCursor

class pgBase(object):

	def master(self):
		return self.__getConnector(True)

	def slave(self):
		return self.__getConnector(False)

	def __getConnector(self, is_master):
		connection_pool = pgLoadBalancer.getConnectionPull(is_master)
		return pgQueryCursor(connection_pool=connection_pool, is_master=is_master, autocommit=True)

	def transaction(self):
		connection_pool = pgLoadBalancer.getConnectionPull()
		return pgQueryCursor(connection_pool=connection_pool, is_master=True, autocommit=False)