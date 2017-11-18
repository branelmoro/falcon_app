from html import escape

class BASE_HTML():

	__base_html = """
<html>
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

	@classmethod
	def renderView(cls, view, body={}, header={}, parent=None, partial=False):
		viewClass = cls.__getViewClass(view)
		obj = viewClass(body=body, header=header, parent=parent)
		body = obj._render()

		if parent:
			return body
		else:
			header = obj.__getHeaderStr()
			if partial:
				return header + body
			else:
				return cls.__base_html.format(body=body, header=header)

	@classmethod
	def __getViewClass(cls, someview):
		if someview not in cls.__all_views:
			try:
				pass
				# from some_view import some_view
			except:
				pass
			cls.__all_views[someview] = some_view
		return cls.__all_views[someview]

	def __getHeaderStr(self):
		# format header here
		header = self._header
		return str(header)

	def _getParentView(self):
		parent = self
		while parent.parent is not None:
			parent = parent.parent
		return parent

	def _mergeHeaderInParent(self, header):
		parent = self._getParentView()
		if parent == self:
			return
		parent._mergeHeader(header)

	def _mergeHeader(self, header):
		# merge header in self._header
		self._header = self._header + header

	def _render(self):
		for k in list(self._body):
			if isinstance(self._body[k], str):
				# to prevent CSRF attack
				self._body[k] = escape(self._body[k])
		parent._mergeHeaderInParent(self._header)
		return self._getFormatedText(self._body)




class some_view(BASE_HTML):

	__text = """
<html>
  <head>
	<title>Spitfire example</title>
  </head>
  <body><p>Hello, {name}</p></body>
</html>
		"""

	def _getFormatedText(self):

		# render inner view
		self._body["name"] = BASE_HTML.renderView("anotherview", body=self._body["name"], header=self._header, parent=self)

		self._body = self.__text.format(**self._body)