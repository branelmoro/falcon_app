# from os import path
from pathlib import Path

from os.path import dirname, abspath

class BASE_STATIC_LOADER(object):

	@classmethod
	def get(cls, file_name):

		if file_name not in cls._static_content:
			file_path = cls._folder + file_name
			if(Path(file_path).is_file()):
				fp = open(file_path, 'r')
				d = fp.read()
				fp.close()
				cls._static_content[file_name] = d
			else:
				exit("file not found - " + file_path)
		return cls._static_content[file_name]

class CSS(BASE_STATIC_LOADER):
	_folder = dirname(dirname(abspath(__file__))) + "/css/"
	_static_content = {}


class JS(BASE_STATIC_LOADER):
	_folder = dirname(dirname(abspath(__file__))) + "/js/"
	_static_content = {}