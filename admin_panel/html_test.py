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


import threading
import pycurl, time, datetime, sys
from io import BytesIO


start_time = datetime.datetime.now().timestamp()

def excecute(path, async=False):
	global start_time
	c = pycurl.Curl()
	c.setopt(c.URL, path)

	if not async:
		http_buffer = BytesIO()
		c.setopt(c.WRITEDATA, http_buffer)
		try:
			c.perform()
		except:
			# throw backend connection error
			pass
		httpcode = c.getinfo(c.HTTP_CODE);

		c.close()
		response = http_buffer.getvalue()
		http_buffer.close()

		if httpcode in [500,501,502,503,504,505]:
			# throw backend api server error
			pass

		end_time = datetime.datetime.now().timestamp()
		total_execution_time = end_time - start_time
		print("Total time - ", total_execution_time)

		return {
			"response" : response,
			# "error_no" => os_errno,
			"httpcode" : httpcode
		}
	else:
		return c




urls = [
	# "http://localhost/phpinfo.php",
	# "http://localhost/phpinfo.php",
	# "http://localhost/phpinfo.php",
	# "http://localhost/phpinfo.php",
	# "http://localhost/phpinfo.php",
	# "http://localhost/phpinfo.php",
	# "http://localhost/phpinfo.php",
	# "http://localhost/phpinfo.php",
	# "http://localhost/phpinfo.php"

	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	"https://fragmentsofcode.wordpress.com/2011/01/22/pycurl-curlmulti-example/",
	# "http://pycurl.io/docs/latest/curlmultiobject.html",
	# "https://curl.haxx.se/libcurl/c/curl_multi_perform.html",
	# "https://stackoverflow.com/questions/25228637/is-the-multi-interface-in-curl-faster-or-more-efficient-than-using-multiple-easy",
	# "http://masnun.com/2015/11/13/python-generators-coroutines-native-coroutines-and-async-await.html"
]

ass = (sys.argv[1] == "1")
if sys.argv[1]=="1":
	reqs = [] 
	# Build multi-request object.
	m = pycurl.CurlMulti()
	for u in urls:
		c = excecute(u, True)
		http_buffer = BytesIO()
		c.setopt(c.WRITEDATA, http_buffer)
		m.add_handle(c)
		reqs.append((u, http_buffer, c))

	# Perform multi-request.
	# This code copied from pycurl docs, modified to explicitly
	# set num_handles before the outer while loop.
	SELECT_TIMEOUT = 1.0
	num_handles = len(reqs)
	while num_handles:
		ret = m.select(SELECT_TIMEOUT)
		print(ret)
		if ret == -1:
			print("here", ret)
			continue
		while 1:
			ret, num_handles = m.perform()
			print(ret,num_handles)
			# exit()
			if ret != pycurl.E_CALL_MULTI_PERFORM: 
				break


	for req in reqs:
		# print(req[1].getvalue())
		req[2].close()


	print(m.info_read())

	m.close()
	# pass
elif sys.argv[1]=="2":
	for u in urls:
		t = threading.Thread(target=excecute, args=[u])
		t.start()
else:
	for u in urls:
		excecute(u)

end_time = datetime.datetime.now().timestamp()
total_execution_time = end_time - start_time
print("Total time - ", total_execution_time)
exit()



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