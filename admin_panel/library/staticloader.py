from os import path
from pathlib import Path

from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))



class BASE_STATIC_LOADER(object):

	@classmethod
	def get(cls, file_name):

		if file_name not in cls._static_content:


			pass
		return cls._static_content[file_name]
		view_template_file = path.dirname(abspath(__file__)) + "/" + view_class_name + ".html"




class CSS(BASE_STATIC_LOADER):
	_folder = dirname(dirname(abspath(__file__))) + "/css/"
	_static_content = {}


class JS(BASE_STATIC_LOADER):
	_folder = dirname(dirname(abspath(__file__))) + "/js/"
	_static_content = {}