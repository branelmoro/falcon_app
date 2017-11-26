from library import BASE_HTML




class sample_view(BASE_HTML):

	__text = """ {at}"""

	def _getFormatedText(self):

		# render inner view
		# self._body["name"] = BASE_HTML.renderView("anotherview", body=self._body["name"], parent=self)

		return self.__text.format(**self._body)