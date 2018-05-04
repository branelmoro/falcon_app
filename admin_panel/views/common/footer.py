from ...library import HTML_RENDERER

class footer(HTML_RENDERER):

	@classmethod
	def _getFormatedText(cls, html_collector, **kwarg):
		html_collector.addCssFile('footer.css')
		return cls._formatHtml()