from library import BASE_HTML

class sample_view(BASE_HTML):

	def _getFormatedText(self):

		# render inner view
		self._body["here"] = BASE_HTML.renderView("sample_view", body={"at":" here"}, parent=self)

		self._body["name"] = "Branel"
		return self._template.format(**self._body)