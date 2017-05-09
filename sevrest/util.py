# This is here to be a base class, such that subclasses can specify which
#    fields should be included when serialized to JSON
class CustomJSON:
	_jsonattrs = []

	def get_dict(this):
		return {attr : this.get_attr(attr) for attr in this._jsonattrs}

	def get_attr(this, attr):
		obj = None
		if(':' in attr):
			attr = attr.split(':', 2)
			obj = getattr(this, attr[0])
			if(hasattr(obj, attr[1])):
				attr = getattr(obj, attr[1])
				if(callable(attr)):
					obj = attr()
				else:
					obj = attr
		else:
			obj = getattr(this, attr)
		if(hasattr(obj, 'get_dict')):
			return obj.get_dict()
		elif(type(obj) == list):
			return [o.get_dict() if hasattr(o, 'get_dict') else o for o in obj]
		elif(type(obj) == dict):
			return {k : v.get_dict() if hasattr(v, 'get_dict') else v for k, v in obj.items()}
		return getattr(this, attr)

