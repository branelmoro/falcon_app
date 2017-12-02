from os.path import dirname, abspath
from pathlib import Path
import re
from html import escape

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
	_folder = dirname(dirname(abspath(__file__))) + "/static/css/"
	_static_content = {}


class JS(BASE_STATIC_LOADER):
	_folder = dirname(dirname(abspath(__file__))) + "/static/js/"
	_static_content = {}


# class HTML(BASE_STATIC_LOADER):
# 	_folder = dirname(dirname(abspath(__file__))) + "/static/html/"
# 	_static_content = {}


class BASE_HTML():

	__base_html = """<!DOCTYPE html><html>
  <head>
	{header}
  </head>
  <body>{body}</body>
</html>"""

	__all_views = {}

	def __init__(self, body={}, header={}, parent=None):
		self._body = body
		self.__header = header
		self.__parent = parent

		if parent is None:

			self.__css = []
			self.__css_dict = {}

			self.__js = []
			self.__js_dict = {}


	@classmethod
	def renderView(cls, view, body={}, header={}, parent=None, partial=False):
		viewClass = cls.__getViewClass(view)
		obj = viewClass(body=body, header=header, parent=parent)
		body = obj._render()

		if parent:
			return body
		else:
			if partial:
				css = obj.__getCss()
				js = obj.__getjs()
				return css + body + js
			else:
				header = obj.__getHeaderStr()
				return cls.__base_html.format(body=body, header=header)

	@classmethod
	def __getViewClass(cls, view):
		if view not in cls.__all_views:
			try:
				view_class_name = view.split(".")[-1]
				view_module = __import__(name=("views." + view), fromlist=[view_class_name])
				cls.__all_views[view] = getattr(view_module,view_class_name)

				view_template_file = dirname(view_module.__file__) + "/" + view_class_name + ".html"
				cls.__all_views[view]._template = cls.__getViewTemplate(view_template_file)

			except AttributeError:
				exit("View Logic Class - "+view_class_name+" not found")
			except:
				exit("AAwoo... view nahi mila..")
		return cls.__all_views[view]


	@classmethod
	def __getViewTemplate(cls, view_template_file):
		print(view_template_file)
		template = ""
		if(Path(view_template_file).is_file()):
			fp = open(view_template_file, 'r')
			html = fp.read()
			fp.close()
			# html = re.sub(r'\n', ' ', html)
			template = html
		return template

	def __getHeaderStr(self):
		# format header here
		title = ""
		if "title" in self.__header:
			title = "<title>"+escape(self.__header["title"])+"</title>"
		return "".join([title, self.__getMetaData(), self.__getCss(), self.__getJs()])


	def __getMetaData(self):
		# default http_equiv
		# <meta http-equiv="Content-type" content="text/html; charset=utf-8"/>
		# <meta http-equiv="X-UA-Compatible" content="IE=Edge" />
		meta_http_equiv = {
			# "Content-type":{
			# 	"content":"text/html; charset=utf-8"
			# },
			# "X-UA-Compatible":{
			# 	"content":"IE=Edge"
			# }
		}

		meta_name = {
			# "application-name":"abc",
			# "auther":"auther",
			# "description":"this is description",
			# "keywords":"key,words"
		}

		custom_meta = []

		if "meta" in self.__header:
			for i in self.__header["meta"]:
				if "name" in i:
					meta_name[i["name"]] = i
				elif "http-equiv" in i:
					meta_http_equiv[i["http-equiv"]] = i
				else:
					custom_meta.append(i)

		meta_data = []
		for http_equiv in meta_http_equiv:
			meta_data.append("<meta " + (" ".join([(attr+'='+'"'+escape(meta_http_equiv[http_equiv][attr])+'"') for attr in meta_http_equiv[http_equiv]])) + "/>")

		for name in meta_name:
			meta_data.append("<meta " + (" ".join([(attr+'='+'"'+escape(meta_name[name][attr])+'"') for attr in meta_name[name]])) + "/>")

		for meta in custom_meta:
			meta_data.append("<meta " + (" ".join([(attr+'='+'"'+escape(meta[attr])+'"') for attr in meta])) + "/>")

		return "".join(meta_data)

	def __getCss(self):
		if self.__css:
			return '<style type="text/css">' + ''.join(self.__css) + '</style>'
		else:
			return ''

	def __getJs(self):
		if self.__js:
			return '<script type="text/javascript">' + ''.join(self.__js) + '</script>'
		else:
			return ''

	def _addCss(self, css, inline=False):
		parent = self._getParentView()
		if css not in parent.__css_dict:
			if inline:
				parent.__css.append(css)
			else:
				parent.__css.append(CSS.get(css))
			parent.__css_dict[css] = True


	def _addJs(self, js, inline=False):
		parent = self._getParentView()
		if js not in parent.__js_dict:
			if inline:
				parent.__js.append(js)
			else:
				parent.__js.append(JS.get(js))
			parent.__js_dict[js] = True

	def _getParentView(self):
		parent = self
		while parent.__parent is not None:
			parent = parent.__parent
		return parent

	def _render(self):
		for k in list(self._body):
			if isinstance(self._body[k], str):
				# to prevent CSRF attack
				self._body[k] = escape(self._body[k])
		return self._getFormatedText()