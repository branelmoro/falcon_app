# from library.htmlloader import BASE_HTML
# a = BASE_HTML.renderView("test.sample_view")
# print(a)

# def coro():
# 	hello = yield "Hello"
# 	yield hello


# c = coro()
# print(next(c))
# print(c.send("World"))
# exit()

import asyncio
# [(function1, data1),(function1, data1),(function1, data1)]


def runAsync(*args):
	for detail in args:
		func = detail[0]
		data = detail[0]
	pass





@asyncio.coroutine
def shleepy_time(seconds):
	print("Shleeping for {s} seconds...".format(s=seconds))
	# yield from asyncio.sleep(seconds)
	# if seconds == 5:
	# 	raise Exception("custom exception")
	print("Done Shleeping for {s} seconds...".format(s=seconds))


if __name__ == '__main__':
	shleepy_time(seconds=4)
	loop = asyncio.get_event_loop()

	# Side note: Apparently, async() will be deprecated in 3.4.4.
	# See: https://docs.python.org/3.4/library/asyncio-task.html#asyncio.async
	tasks = asyncio.gather(
		asyncio.async(shleepy_time(seconds=5)),
		asyncio.async(shleepy_time(seconds=3)),
		asyncio.async(shleepy_time(seconds=7))
	)
	runAsync()
	try:
		print("starting loop")
		loop.run_until_complete(tasks)
		print("done event loop")
	except KeyboardInterrupt as e:
		print("Caught keyboard interrupt. Canceling tasks...")
		tasks.cancel()
		loop.run_forever()
		tasks.exception()
	finally:
		loop.close()