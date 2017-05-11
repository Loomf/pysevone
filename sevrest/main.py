import json
import requests 
import urllib

from . import util

from . import plugin

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
		return this.search('plugins' + this.dict2qstr(sieve), cls = plugin.Plugin)

	def get_objecttypes(this, sieve = None):
		return this.search('plugins/objecttypes', sieve, cls = plugin.ObjectType)

	def get_indicatortypes(this, sieve = None):
		return this.search('plugins/indicatortypes', sieve, cls = plugin.IndicatorType)

	def get_devices(this, sieve = None):
		return this.search('devices', sieve)

	def get_objects(this, sieve):
		assert sieve != None
		return this.search('devices/objects', sieve)

	def search(this, url, sieve = None, page = None, size = 50, cls = None):
		if(page == None):
			page = 0
			response = this.search(url, sieve, page, size, cls)
			results = response['content']
			total_pages = response['totalPages']
			for page in range(1, total_pages):
				response = this.search(url, sieve, page, size, cls)
				results.extend(response['content'])
		else:
			append = 'page=' + str(page) + '&size=' + str(size)
			if(sieve == None):
				results = this.request('GET', url + ('&' if '?' in url else '?') + append)
			else:
				results = this.request('POST', url + '/filter' + ('&' if '?' in url else '?') + append, body = sieve)

			if('status' in results and not(results['status'] >= 200 and results['status'] < 300)):
				raise util.RESTException('%d %s:  %s' % (results['status'], results['title'], results['detail']))

			results['content'] = cls.load(results['content'])

		return results

	def request(this, method, url, body = None):
		url = this.base_url + '/' + url
		if(body == None):
			return json.loads(requests.request(method, url, headers = this.headers).content)
		return json.loads(requests.request(method, url, headers = this.headers, json = body).content)

	def dict2qstr(this, dict_in):
		if(dict_in == None or len(dict_in) == 0):
			return ''
		qstr = '?' + ''.join(['%s=%s&' % (urllib.quote(key, ''), urllib.quote(value, '')) for key, value in dict_in.items()])
		return qstr[:-1]

