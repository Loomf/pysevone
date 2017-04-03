class CustomJSON:
	_jsonattrs = []

	def get_dict(this):
		return {attr : this.get_attr(attr) for attr in this._jsonattrs}

	def get_attr(this, attr):
		obj = getattr(this, attr)
		if(hasattr(obj, 'get_dict')):
			return obj.get_dict()
		elif(type(obj) == list):
			return [o.get_dict() if hasattr(o, 'get_dict') else o for o in obj]
		elif(type(obj) == dict):
			return {k : v.get_dict() if hasattr(v, 'get_dict') else v for k, v in obj.items()}
		return getattr(this, attr)

