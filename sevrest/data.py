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

