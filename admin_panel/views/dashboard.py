# from ..library import HTML_RENDERER
from .layout import layout

class dashboard(layout):

	@classmethod
	def _getHTML(cls, html_collector, **kwargs):
		html_collector.addCssFile('right_content_section.css')
		html_collector.addCssFile('right_content_title_bar.css')
		html_collector.addCssFile('data_table.css')


		footer = cls._renderView("common.footer", html_collector=html_collector, **kwargs)

		print('get html')

		return cls._formatHtml(footer=footer)

	# @classmethod
	# def _getFormatedText(cls, html_collector, **kwargs):
	# 	html_collector.addCssFile('right_content_section.css')
	# 	html_collector.addCssFile('right_content_title_bar.css')
	# 	html_collector.addCssFile('data_table.css')


	# 	footer = cls._renderView("common.footer", html_collector=html_collector, **kwargs)

	# 	return cls._formatHtml(footer=footer)

	@classmethod
	def _getFstring(cls):
		return f'''


		'''