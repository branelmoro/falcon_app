# always extend your model from base_model
# always give model class name same as model name
from ..base_model import baseModel

class sampleModel(baseModel):
	"""entire code goes here"""

	def test(self):
		print("in samplemodel test")
		self.pgMaster()
		self.pgSlave()