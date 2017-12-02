from library import BASE_HTML

class sample_view(BASE_HTML):

	def _getFormatedText(self):

		self._addJs("test.js")

		return self._template.format(**self._body)