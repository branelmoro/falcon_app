from os.path import dirname, abspath
from pathlib import Path
from html import escape

from .. import exception as appException





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






class HTML_COLLECTOR(object):

	def __init__(self, container):
		self.container = container
		self.__head = {}
		self.__css = []
		self.__css_set = set()
		self.__js = []
		self.__js_set = set()
		self.__body = ''


	def __getHtmlHead(self):
		head = ''
		if 'title' in self.__head:
			head = head + '<title>'+escape(self.__head['title'])+'</title>'

		if 'meta' in self.__head:
			for meta_data in self.__head['meta']:
				head = head + '<meta ' + (' '.join([attr + '="' + escape(meta[attr]) + '"' for attr in meta_data])) + '/>'

		head = head + self.__getCss()
		head = head + self.__getJs()

		return head

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

	def setTitle(self, title):
		self.__head['title'] = title

	def setMetaData(self, data):
		if 'meta' not in self.__head:
			self.__head['meta'] = []
		self.__head['meta'].append(data)

	def addJsFile(self, js):
		if css not in self.__css_set:
			self.__css.append(CSS.get(css))
			self.__css_set.add(css)

	def addCssFile(self, js):
		if js not in self.__js_set:
			self.__js.append(JS.get(js))
			self.__js_set.add(js)

	def addCss(self, css):
		if css not in self.__css_set:
			self.__css.append(css)
			self.__css_set.add(css)

	def addJs(self, js, inline=False):
		if js not in self.__js_set:
			self.__js.append(js)
			self.__js_set.add(js)

	def setBody(self, body):
		self.__body = body

	def getHTML(self, partial=False):
		if partial:
			css = self.__getCss()
			js = self.__getjs()
			return css + body + js
		else:
			head = self.__getHtmlHead()
			return self.__base_html.format(body=self.__body, head=head)





class HTML_RENDERER():

	__base_html = '''<!DOCTYPE html><html>
  <head>
	{head}
  </head>
  <body>{body}</body>
</html>'''

	@classmethod
	def render(cls, view, container, partial=False):
		html_collector = HTML_COLLECTOR()
		html_collector.setBody(cls._renderView(view, container, html_collector))
		return html_collector.getHTML(partial)

	@classmethod
	def _renderView(cls, view, container, html_collector):
		viewClass = cls.__getViewClass(view)
		return viewClass._getFormatedText(container, html_collector)

	@classmethod
	def __getViewClass(cls, view):
		if view not in cls.__all_views:
			try:
				view_class_name = view.split(".")[-1]
				view_module = __import__(name=("admin_panel.views." + view), fromlist=[view_class_name])
				
				cls.__all_views[view] = getattr(view_module,view_class_name)

				view_template_file = dirname(view_module.__file__) + "/" + view_class_name + ".html"
				cls.__all_views[view]._template = cls.__getViewTemplate(view_template_file)

			except AttributeError:
				exit("View Logic Class - "+view_class_name+" not found")
			except:
				exit("AAwoo... view nahi mila..")
				# raise appException.serverException_500()
		return cls.__all_views[view]


	@classmethod
	def __getViewTemplate(cls, view_template_file):
		# print(view_template_file)
		template = ""
		if(Path(view_template_file).is_file()):
			fp = open(view_template_file, 'r')
			html = fp.read()
			fp.close()
			# html = re.sub(r'\n', ' ', html)
			template = html
		return template
