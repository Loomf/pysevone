import json

import util

class DeviceDataIndicator(util.CustomJSON):
	_jsonattrs = ['name', 'value', 'format', 'units', 'maxValue']
	name = None
	value = None
	format = None
	units = None
	maxValue = None

	def __init__(this, name, value, **kwargs):
		assert type(name) == str and name != ''
		assert type(value) == int or type(value) == float
		this.name = name
		this.value = value
		for (k, v) in kwargs.items():
			setattr(this, k, v)

class DeviceDataTimestamp(util.CustomJSON):
	_jsonattrs = ['timestamp', 'indicators:values']
	timestamp = 0
	indicators = {}

	def __init__(this, timestamp, **kwargs):
		assert type(timestamp) == int and timestamp > 0
		this.timestamp = timestamp
		for (k, v) in kwargs.items():
			setattr(this, k, v)

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

	def __init__(this, name, type_name, plugin_name, create_automatically, **kwargs):
		assert type(name) == str and name != ''
		assert type(type_name) == str and type_name != ''
		assert type(plugin_name) == str and plugin_name != ''
		assert type(create_automatically) == bool
		this.name = name
		this.type = type_name
		this.plugin_name = plugin_name
		this.create_automatically = create_automatically
		for (k, v) in kwargs.items():
			setattr(this, k, v)

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

	def __init__(this, name, initial_timestamp, source_id, **kwargs):
		assert type(name) == str and name != ''
		assert type(initial_timestamp) == int
		assert type(source_id) == int
		this.name = name
		this.initial_timestamp = initial_timestamp
		this.source_id = source_id
		for (k, v) in kwargs.items():
			setattr(this, k, v)

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

