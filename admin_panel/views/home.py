from ..library import BASE_HTML

class home(BASE_HTML):

	def _getFormatedText(self):

		self._body["header"] = BASE_HTML.renderView("common.header", body={}, parent=self)
		self._body["footer"] = BASE_HTML.renderView("common.footer", body={}, parent=self)

		return self._template.format(**self._body)