from ...library import HTML_RENDERER

class left_nav(HTML_RENDERER):

	@classmethod
	def _getFormatedText(cls, html_collector, **kwargs):
		html_collector.addCssFile('left_nav.css')
		return cls._formatHtml()

	@classmethod
	def _getFstring(cls):
		return f'''


		'''