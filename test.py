# import json
# def application(environ, start_response):
# 	start_response('200 OK', [('Content-Type', 'text/html')])
# 	print(environ)
# 	encoded_str = json.dumps(environ)
# 	return [b"Hellordgedgf There!" + encoded_str]


import os, tempfile, time


# if b'0':
# 	print("true")
# else:
# 	print("false")
# exit()
os.remove("/tmp/tmp6c0a4fgv")

fd, path = tempfile.mkstemp()
print(path)
time.sleep(10)
try:
	with os.fdopen(fd, 'w+b') as tmp:
		# do stuff with temp file
		tmp.write(b'\x03\xff\x00')
		tmp.write(b'stuff')
		tmp.write(b'stuff')
		tmp.write(b'stuff')
		tmp.write(b'stuff')
	time.sleep(5)
finally:
	os.remove(path)