import json

from . import util

class IndicatorType(util.CustomJSON):
	_jsonattrs = ['id', 'pluginId', 'pluginObjectTypeId', 'name', 'isEnabled', 'isDefault', 'format', 'dataUnits', 'displayUnits,omitempty', 'description', 'allowMaximumValue', 'syntheticExpression', 'syntheticMaximumExpression', 'extendedInfo,omitempty']
	id = None
	pluginId = None
	pluginObjectTypeId = None
	name = None
	isEnabled = None
	isDefault = None
	format = None
	dataUnits = None
	displayUnits = None
	description = None
	allowMaximumValue = None
	syntheticExpression = None
	syntheticMaximumExpression = None
	extendedInfo = None

class ObjectType(util.CustomJSON):
	_jsonattrs = ['id,omitempty', 'pluginId', 'parentObjectTypeId', 'name', 'isEnabled', 'isEditable', 'extendedInfo,omitempty', 'indicatorTypes:values']
	id = None
	pluginId = None
	parentObjectTypeId = None
	name = None
	isEnabled = None
	isEditable = None
	extendedInfo = None
	indicatorTypes = {}

	def __init__(this, **kwargs):
		if('indicatorTypes' in kwargs):
			this.indicators = {i['name'] if(type(i) == dict) else i.name : IndicatorType(**i) if(type(i) == dict) else i for i in kwargs['indicatorTypes']}
			del kwargs['indicatorTypes']
		super(this.__class__, this).__init__(**kwargs)

class Plugin(util.CustomJSON):
	_jsonattrs = ['id,omitempty', 'name', 'objectName', 'dir', 'plottable']
	id = None
	name = None
	objectName = None
	dir = None
	plottable = None

