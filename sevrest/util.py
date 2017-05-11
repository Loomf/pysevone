import json

# This is here to be a base class, such that subclasses can specify which
#    fields should be included when serialized to JSON
class CustomJSON(object):
	_jsonattrs = []

	@classmethod
	def loads(cls, in_str):
		obj = json.loads(in_str)
		return cls.load(obj)

	@classmethod
	def load(cls, in_obj):
		if(type(in_obj) == list):
			return [cls(**o) for o in in_obj]
		elif(type(in_obj) == dict):
			return cls(**in_obj)
		raise TypeError(cls.__name__ + '::load() cannot handle JSON objects of type "' + type(in_obj).__name__ + '"')

	def __init__(this, **kwargs):
		for (k, v) in kwargs.items():
			if(not hasattr(this, k)):
				raise AttributeError(this.__class__.__name__ + ' does not have attribute "' + k + '"')
			setattr(this, k, v)

	def dumps(this):
		return json.dumps(this.get_dict())

	def get_dict(this):
		this_dict = {}
		for attr in this._jsonattrs:
			try:
				(attr, value) = this.get_attr(attr)
				this_dict[attr] = value
			except NoValue:
				pass

		return this_dict

	def get_attr(this, attr):
		if(',' in attr):
			(attr, options) = attr.split(',', 1)
			options = options.split(',')
		else:
			options = []
		(attr, value) = this.get_raw_attr(attr)
		return (attr, this.process_options(value, options))

	def get_raw_attr(this, attr):
		obj = None
		if(':' in attr):
			(attr, func) = attr.split(':', 1)
			obj = getattr(this, attr)
			if(hasattr(obj, func)):
				member = getattr(obj, func)
				if(callable(member)):
					obj = member()
				else:
					obj = member
		else:
			obj = getattr(this, attr)

		if(hasattr(obj, 'get_dict')):
			return (attr, obj.get_dict())
		elif(type(obj) == list):
			return (attr, [o.get_dict() if hasattr(o, 'get_dict') else o for o in obj])
		elif(type(obj) == dict):
			return (attr, {k : v.get_dict() if hasattr(v, 'get_dict') else v for k, v in obj.items()})
		return (attr, getattr(this, attr))

	def process_options(this, value, options):
		if('omitempty' in options):
			if(value == None):
				raise NoValue()
			elif(type(value) == int):
				if(value == 0):
					raise NoValue()
			elif(type(value) == float):
				if(value == 0.0):
					raise NoValue()
			elif(type(value) == str):
				if(value == ''):
					raise NoValue()
			elif(type(value) == tuple):
				if(value == ()):
					raise NoValue()
			elif(type(value) == list):
				if(len(value) == 0):
					raise NoValue()
			elif(type(value) == dict):
				if(len(value) == 0):
					raise NoValue()
		return value

class NoValue(Exception):
	pass

