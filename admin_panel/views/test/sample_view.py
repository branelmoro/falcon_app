from library import BASE_HTML




class sample_view(BASE_HTML):

	__text = """<p>Hello, {name} {here}</p>"""

	def _getFormatedText(self):

		# render inner view
		self._body["here"] = BASE_HTML.renderView("sample_view", body={"at":" here"}, parent=self)

		self._body["name"] = "Branel"
		return self.__text.format(**self._body)