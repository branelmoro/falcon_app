from library import BASE_HTML




class sample_view(BASE_HTML):

	__text = """<p>Hello, {name}</p>"""

	def _getFormatedText(self):

		# render inner view
		# self._body["name"] = BASE_HTML.renderView("anotherview", body=self._body["name"], parent=self)

		self._body["name"] = "Branel"
		return self.__text.format(**self._body)