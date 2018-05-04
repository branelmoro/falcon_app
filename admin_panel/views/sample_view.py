from ..library import HTML_RENDERER

class sample_view(HTML_RENDERER):

	def _getFormatedText(cls):

		cls._addJs("test.js")

		return cls._formatHtml()