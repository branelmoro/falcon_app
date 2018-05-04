from ..library import HTML_RENDERER

class home(HTML_RENDERER):

	@classmethod
	def _getFormatedText(cls, container, html_collector):

		data = {}

		# data["header"] = cls._renderView("common.header", container=container, html_collector=html_collector)
		data["header"] = cls._renderView("common.header")
		data["footer"] = cls._renderView("common.footer")

		return cls._formatHtml(**data)

	@classmethod
	def _getFstring(cls):
		return f'''


		'''