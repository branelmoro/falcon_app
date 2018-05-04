from ..library import HTML_RENDERER

class login(HTML_RENDERER):

	@classmethod
	def _getFormatedText(cls, html_collector, container=None):

		# cls._addJs('test.js')
		if container:
			data = container.data
		else:
			data = {}

		data.update({i:'' for i in ['username','username_error','password_error'] if i not in data})

		return cls._template.format(**data)