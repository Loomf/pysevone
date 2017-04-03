import json
import requests 

class SevOne:
	headers = {
		'User-Agent' : 'sevrest/python/0.1',
		'Accept' : 'application/json',
		'Content-Type' : 'application/json;charset=UTF-8'
	}
	base_url = None

	def __init__(this, base_url, token = None, username = None, password = None):
		this.base_url = base_url
		if(token == None):
			response = this.auth(username, password)
			this.set_token(response['token'])
		else:
			this.set_token(token)

	def auth(this, username, password):
		response = this.request('POST', 'authentication/signin', {"name" : username, "password" : password})
		return response

	def set_token(this, token):
		this.headers['X-Auth-Token'] = token

	def get_plugins(this, sieve = None):
		return this.search('GET', 'plugins', sieve)

	def get_objecttypes(this, sieve = None):
		if(sieve == None):
			return this.search('GET', 'plugins/objecttypes')
		return this.search('POST', 'plugins/objecttypes/filter', sieve)

	def search(this, method, url, sieve = None, page = None, size = 50):
		if(page == None):
			page = 0
			response = this.search(method, url, sieve, page, size)
			results = response['content']
			total_pages = response['totalPages']
			for page in range(1, total_pages):
				response = this.search(method, url, sieve, page, size)
				results.extend(response['content'])
		else:
			append = 'page=' + str(page) + '&size=' + str(size)
			results = this.request('GET', url + ('&' if '?' in url else '?') + append)
		return results

	def request(this, method, url, body = None):
		url = this.base_url + '/' + url
		if(body == None):
			return json.loads(requests.request(method, url, headers = this.headers).content)
		return json.loads(requests.request(method, url, headers = this.headers, json = body).content)

