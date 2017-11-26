from library import BASE_HTML




class sample_view(BASE_HTML):

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
		# self._body["name"] = BASE_HTML.renderView("anotherview", body=self._body["name"], parent=self)

		self._body = self.__text.format(**self._body)