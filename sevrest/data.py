import json

from . import util

class DeviceDataIndicator(util.CustomJSON):
	_jsonattrs = ['name', 'value', 'format', 'units', 'maxValue']
	name = None
	value = None
	format = None
	units = None
	maxValue = None

	@classmethod
	def new(cls, name, value, **kwargs):
		assert type(name) == str and name != ''
		assert type(value) == int or type(value) == float
		return cls(name = name, value = value, **kwargs)

class DeviceDataTimestamp(util.CustomJSON):
	_jsonattrs = ['timestamp', 'indicators:values']
	timestamp = 0
	indicators = {}

	@classmethod
	def new(cls, timestamp, **kwargs):
		assert type(timestamp) == int and timestamp > 0
		return cls(timestamp = timestamp, **kwargs)

	def __init__(this, **kwargs):
		if('indicators' in kwargs):
			this.indicators = {i['name'] if(type(i) == dict) else i.name : DeviceDataIndicator(**i) if(type(i) == dict) else i for i in kwargs['indicators']}
			del kwargs['indicators']
		super(this.__class__, this).__init__(**kwargs)

	def add_indicator(this, name, value):
		if(name in this.indicators):
			indicator = this.indicators[name]
			indicator.value = value
		else:
			indicator = DeviceDataIndicator(name, value)
			this.indicators[name] = indicator

class DeviceDataObject(util.CustomJSON):
	_jsonattrs = ['name', 'type', 'pluginId', 'pluginName', 'description', 'automaticCreation', 'timestamps:values']
	name = None
	type = None
	pluginId = None
	pluginName = None
	description = None
	automaticCreation = False
	timestamps = {}

	@classmethod
	def new(cls, name, type_name, plugin_name, create_automatically, **kwargs):
		assert type(name) == str and name != ''
		assert type(type_name) == str and type_name != ''
		assert type(plugin_name) == str and plugin_name != ''
		assert type(create_automatically) == bool
		return cls(name = name, type = type_name, pluginName = plugin_name, automaticCreation = create_automatically, **kwargs)

	def __init__(this, **kwargs):
		if('timestamps' in kwargs):
			this.timestamps = {t['timestamp'] if(type(t) == dict) else t.timestamp : DeviceDataTimestamp(**t) if(type(t) == dict) else t for t in kwargs['timestamps']}
			del kwargs['timestamps']
		super(this.__class__, this).__init__(**kwargs)

	def add_indicator(this, time, name, value):
		if(time in this.timestamps):
			timestamp = this.timestamps[time]
		else:
			timestamp = DeviceDataTimestamp(time)
			this.timestamps[time] = timestamp
		timestamp.add_indicator(name, value)

class DeviceData(util.CustomJSON):
	_jsonattrs = ['name', 'type', 'oldTs', 'newTs', 'ip', 'automaticCreation', 'sourceId', 'objects:values']
	name = None
	type = None
	oldTs = 0
	newTs = 0
	ip = None
	automaticCreation = False
	sourceId = None
	objects = {}

	@classmethod
	def new(cls, name, initial_timestamp, source_id, **kwargs):
		assert type(name) == str and name != ''
		assert type(initial_timestamp) == int
		assert type(source_id) == int
		return cls(name = name, oldTs = initial_timestamp, sourceId = source_id, **kwargs)

	def __init__(this, **kwargs):
		if('objects' in kwargs):
			this.objects = {o['name'] if(type(o) == dict) else o.name : DeviceDataObject(**o) if(type(o) == dict) else o for o in kwargs['objects']}
			del kwargs['objects']
		super(this.__class__, this).__init__(**kwargs)

	def add_indicator(this, object_name, object_type, plugin_name, time, indicator_name, value):
		if(object_name in this.objects):
			obj = this.objects[object_name]
		else:
			obj = DeviceDataObject(object_name, object_type, plugin_name, this.automaticCreation)
			this.objects[object_name] = obj
		obj.add_indicator(time, indicator_name, value)

	def resolve_timestamps(this):
		for o in this.objects.values():
			for t in o.timestamps.values():
				if(t.timestamp < this.oldTs or this.oldTs == 0):
					this.oldTs = t.timestamp
				if(t.timestamp > this.newTs):
					this.newTs = t.timestamp

