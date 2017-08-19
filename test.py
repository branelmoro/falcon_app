import json
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    print(environ)
    encoded_str = json.dumps(environ)
    return [b"Hellordgedgf There!" + encoded_str]
