import json
import restclient

class SevOne:
	headers = {
		'User-Agent' : 'sevrest/python/0.1',
		'Accept' : 'application/json',
		'Content-Type' : 'application/json;charset=UTF-8'
	}
	client = None
	base_url = None

	def __init__(this, base_url, token = None, username = None, password = None):
		this.base_url = base_url
		this.client = restclient.RestClient()
		if(token == None):
			this.auth(username, password)
		else:
			this.set_token(token)
	
	def auth(this, username, password):
		response = this.request('POST', 'authentication/signin', {"user" : username, "password" : password})
		this.set_token(response['token'])
	
	def set_token(this, token):
		this.headers['X-Auth-Token'] = token
		
	def request(this, method, url, body = None):
		url = this.base_url + '/' + url
		if(body == None):
			return json.loads(this.client.make_request(method, url, headers = this.headers))
		return json.loads(this.client.make_request(method, url, headers = this.headers, body = json.dumps(body)))

