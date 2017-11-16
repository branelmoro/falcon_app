


class BASE_RENDERER(object):

	__all_views = {}

	@classmethod
	def getviewObj(cls, someview):

		if someview not in cls.__all_views:
			try:
				pass
				# from some_view import some_view
			except:
				pass
			cls.__all_views[someview] = some_view

		return cls.__all_views[someview]
		# if False:
		#	 exit("view not found")
		# return some_view()


	@classmethod
	def render(cls, someview, kwargs):
		view = cls.getviewObj()
		for k in list(kwargs):
			if isinstance(kwargs[k], RAW):
				kwargs[k] = kwargs[k].get()
			elif isinstance(kwargs[k], str):
				# to prevent CSRF attack
				kwargs[k] = html_special_chars(kwargs[k])
		return view._getFormatedText(kwargs)





class some_view(BASE_RENDERER):

	__text = """
<html>
  <head>
	<title>Spitfire example</title>
  </head>
  <body><p>Hello, {name}</p></body>
</html>
		"""

	def _getFormatedText(cls, kwargs):

		# render inner view
		kwargs["name"] = cls.render("anotherview", kwargs["name"])

		return cls.__text.format(**kwargs)