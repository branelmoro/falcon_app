from os import path
from pathlib import Path
import re
from html import escape

class BASE_HTML():

	__base_html = """<html>
  <head>
	{header}
  </head>
  <body>{body}</body>
</html>"""

	__all_views = {}

	def __init__(self, body={}, header={}, parent=None):
		self._body = body
		self._header = header
		self._parent = parent

		if "script" not in self._header:
			self._header["script"] = []

		if "css" not in self._header:
			self._header["css"] = []

		if not parent:
			self._script_dict = {}
			for i in self._header["script"]:
				self._script_dict[i["id"]] = True

			self._css_dict = {}
			for i in self._header["css"]:
				self._css_dict[i["id"]] = True


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

				view_template_file = path.dirname(view_module.__file__) + "/" + view_class_name + ".html"
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
		if "title" in self._header:
			title = "<title>"+escape(self._header["title"])+"</title>"
		# meta_data = self.__getMetaData()
		# css = self.__getCss()
		# js = self.__getJs()
		return "".join([title, self.__getMetaData(), self.__getCss(), self.__getJs()])


	def __getMetaData(self):
		# default http_equiv
		"""<meta http-equiv="Content-type" content="text/html; charset=utf-8"/>
		<meta http-equiv="X-UA-Compatible" content="IE=Edge" />"""
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

		if "meta" in self._header:
			for i in self._header["meta"]:
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
		css = ""
		if self._header["css"]:
			for i in self._header["css"]:
				if isinstance(i, str):
					css = css + i
		if css:
			css = '<style type="text/css">' + css + '</style>'
		return css

	def __getJs(self):
		js = ""
		if self._header["script"]:
			for i in self._header["script"]:
				if isinstance(i, str):
					js = js + i
		if js:
			js = '<script type="text/javascript">' + js + '</script>'
		return js

	def _getParentView(self):
		parent = self
		while parent._parent is not None:
			parent = parent._parent
		return parent

	def _mergeHeaderInParent(self):
		parent = self._getParentView()
		if parent == self:
			return
		parent.__mergeHeader(self._header)

	def __mergeHeader(self, header):
		# merge header in self._header

		for script in header["script"]:
			if script["id"] not in self._script_dict:
			# if script not in self._header:
				self._header["script"].append(script)
				self._script_dict[script["id"]] = True

		for css in header["css"]:
			if css["id"] not in self._css_dict:
			# if css not in self._header:
				self._header["css"].append(css)
				self._css_dict[css["id"]] = True

	def _render(self):
		for k in list(self._body):
			if isinstance(self._body[k], str):
				# to prevent CSRF attack
				self._body[k] = escape(self._body[k])
		self._mergeHeaderInParent()
		return self._getFormatedText()