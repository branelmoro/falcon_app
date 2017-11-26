# never change this file unless required

from ..resources.postgres import pgBase as postgres

class baseModel(object):
	"""This is base model and all other models will be child"""

	# def __init__(self):
	# 	self.__master = None
	# 	self.__slave = None

	def pgMaster(self):
		return postgres().master()

	def pgSlave(self):
		return postgres().slave()

	def pgTransaction(self):
		return postgres().transaction()