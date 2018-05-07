from ..library import HTML_RENDERER

class layout(HTML_RENDERER):

	@classmethod
	def _getFormatedText(cls, html_collector, **kwargs):

		data = {}

		# header = cls._renderView("common.header", container=container, html_collector=html_collector)
		header = cls._renderView("common.header", html_collector=html_collector, **kwargs)
		left_section = cls._renderView("common.left_nav", html_collector=html_collector, **kwargs)
		right_section = cls._getHTML(html_collector=html_collector, **kwargs)

		return header + left_section + right_section
		# return cls._formatHtml(header=header, left_section=left_section, right_section=right_section)

	# @classmethod
	# def _getFstring(cls):
	# 	return f'''


	# 	'''