from ...library import HTML_RENDERER

class header(HTML_RENDERER):

	@classmethod
	def _getFormatedText(cls, html_collector, **kwarg):

		html_collector.addCssFile('reset.css')

		html_collector.addCssFile('layout.css')

		return cls._formatHtml()