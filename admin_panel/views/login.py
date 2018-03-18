from ..library import BASE_HTML

class login(BASE_HTML):

	def _getFormatedText(self):

		# self._addJs("test.js")

		template_vars = ["username","username_error","password_error"]

		for v in template_vars:
			if v not in self._body:
				self._body[v] = ""

		return self._template.format(**self._body)