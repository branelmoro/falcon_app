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

class abc():
	def __init__(self):
		self.a = 10


def abcd():
	pass
a = {}
print(type(a))
exit()
a = abc()
b = abc()


lst = [b,b,a]

print(a in lst)
print(lst)
print(id(a), a)
print(id(b), b)
exit()

import threading, redis
import pycurl, time, datetime, sys
from io import BytesIO


def getRedis():
	# return redis.StrictRedis(host, port, db, password, socket_timeout, connection_pool, charset, errors, decode_responses, unix_socket_path)
	return redis.StrictRedis(host="127.0.0.1", port=6379, db=0)


def raceThread(delay):
	client_session_id = "mykey"
	conn = getRedis()
	# conn.watch(client_session_id)
	pipe = conn.pipeline(transaction=True)
	pipe.watch(client_session_id)
	pipe.multi()
	time.sleep(delay)
	pipe.hset(client_session_id, "token_api_call", "thread"+str(delay)+str(datetime.datetime.now()))
	# pipe.set(client_session_id, "thread"+str(delay)+ "-----" + str(datetime.datetime.now()))
	response = pipe.execute()
	print(delay, response)
	# conn.close()


# def raceThread1(pipe):
# 	client_session_id = "mykey"
# 	pipe.watch(client_session_id)
# 	pipe.hset(client_session_id, "token_api_call", thread_name + str(datetime.datetime.now()))
# 	time.sleep(delay)
# 	response = pipe.execute()
# 	print(thread_name, delay, response)


# def threadfunc(thread_name, delay):
# 	client_session_id = "mykey"
# 	conn = getRedis()
# 	response = conn.transaction(client_side_incr, client_session_id)
# 	print(thread_name, delay, response)



t = threading.Thread(target=raceThread, args=[5])
t.start()

t = threading.Thread(target=raceThread, args=[2])
t.start()

t = threading.Thread(target=raceThread, args=[3])
t.start()

t = threading.Thread(target=raceThread, args=[4])
t.start()

# time.sleep(1)
# conn = getRedis()
# conn.set("mykey", "dsdsfsdfsdf")

time.sleep(5)
exit()



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

	m.setopt(pycurl.M_PIPELINING, 1)

	# Perform multi-request.
	# This code copied from pycurl docs, modified to explicitly
	# set num_handles before the outer while loop.
	SELECT_TIMEOUT = 1.0
	num_handles = len(reqs)
	old_handles = num_handles
	while num_handles:
		ret = m.select(SELECT_TIMEOUT)
		if ret == -1:
			continue
		while 1:
			ret, num_handles = m.perform()
			print(ret,num_handles)
			if old_handles != num_handles:
				# check completed request
				print(m.info_read())
				old_handles=num_handles
				pass
			if ret != pycurl.E_CALL_MULTI_PERFORM: 
				break



	print(m.info_read())

	for req in reqs:
		# print(req[1].getvalue())
		req[2].close()

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












# def getDataFromAPI(self, resources):
# 	if "async" in resources:
# 		# this is async call
# 	else:
# 		# this is sync call
		


# 	if "next" in resources:
# 		self.getDataFromAPI(resources["next"])


# [

# {
# 	resource1:{

# 	},
# 	callback1: {

# 	}
# },
# [
# {
# 	resource1:{

# 	},
# 	callback1: {

# 	}
# },

# ]


# ]


# {
# 	run_now:[
# 		C1
# 		{
# 			resource1:{

# 			},
# 			callback1: {

# 			},
# 			next:{
# 				run_now:[
# 					c5
# 					{
# 						next:[

# 						],
# 						resource1:{

# 						},
# 						callback1: {

# 						}
# 					}
# 				]
# 			}
# 		}

# 		c2

# 		c3

# 	]
# 	next:{
# 		run_now:[
# 			c6
# 			{
# 				next:{
# 					run_now:[
# 						c8
# 						{
# 							resource1:{

# 							},
# 							callback1: {

# 							},
# 							next:[

# 							]
# 						},


# 						C9
# 					]
# 				}
# 			}

# 			c7
# 		]
# 	}
# }
















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