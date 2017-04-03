import json

import util

class DeviceDataIndicator(util.CustomJSON):
	_jsonattrs = ['name', 'value', 'format', 'units', 'maxValue']
	name = None
	value = None
	format = None
	units = None
	maxValue = None

class DeviceDataTimestamp(util.CustomJSON):
	_jsonattrs = ['timestamp', 'indicators']
	timestamp = 0
	indicators = []

class DeviceDataObject(util.CustomJSON):
	_jsonattrs = ['name', 'type', 'pluginId', 'pluginName', 'description', 'automaticCreation', 'timestamps']
	name = None
	type = None
	pluginId = None
	pluginName = None
	description = None
	automaticCreation = False
	timestamps = []

class DeviceData(util.CustomJSON):
	_jsonattrs = ['name', 'type', 'oldTs', 'newTs', 'ip', 'automaticCreation', 'sourceId', 'objects']
	name = None
	type = None
	oldTs = 0
	newTs = 0
	ip = None
	automaticCreation = False
	sourceId = None
	objects = []

