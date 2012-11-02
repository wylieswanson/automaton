# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort, Response, request, url_for, make_response
from functools import update_wrapper
import json, sys
from pprint import pprint

import jsonrpclib

lights = Blueprint('lights', __name__)
zwave = jsonrpclib.Server("http://localhost:8080")

def nocache(f):
	def new_func(*args, **kwargs):
		resp = make_response(f(*args, **kwargs))
		resp.cache_control.no_cache = True
		return resp
	return update_wrapper(new_func, f)

@lights.route('/')
@nocache
def index():
	locations=[]
	for loc in sorted(zwave.all_switch_locations()):
		location={}
		location['location']=loc
		location['url']=url_for('.with_location', location=loc)

		switches = sorted(zwave.all_switches_in_location(loc))
		num_on = 0 ; num_off = 0
		for switch in switches:
			if switch['state']: num_on += 1
			else: num_off += 1

		location['num_switches']=len( switches )
		location['has_switches_on']=(num_on>0)
		location['num_switches_on']=num_on
		location['num_switches_off']=num_off
		locations.append(location)
	if not len(locations):
		return render_template("lights.html", empty = True, page_title = "Lights")
	pprint(locations)
	return render_template('lights.html', items = locations, page_title = "Lights")

@lights.route('/<location>')
@nocache
def with_location(location):
	devices=[]
	for device in sorted (zwave.all_switches_in_location(location) ):
		device['url'] = url_for('.with_device',location=location, name=device['name'], node=device['node'])
		device['switched_on'] = device['state']
		devices.append(device)
		return render_template('devices.html', items = devices, page_title=location)
		

@lights.route('/<location>/<name>/<node>')
@nocache
def with_device(location,name,node):
	device={}
	device['location']=location
	device['name']=name
	device['node']=node
	device['on']=zwave.get_switch_state( device['node'] )


	return render_template('switch.html', device=device)

