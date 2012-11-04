# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort, Response, request, url_for, make_response
from functools import update_wrapper
import json, sys
from pprint import pprint
import datetime
import jsonrpclib

lights = Blueprint('lights', __name__)
zwave = jsonrpclib.Server("http://localhost:8080")

#r.headers.add('Last-Modified', datetime.datetime.now())
#r.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, 
#post-check=0, pre-check=0')
#r.headers.add('Pragma', 'no-cache')

def nocache(f):
	def new_func(*args, **kwargs):
		resp = make_response(f(*args, **kwargs))
		resp.cache_control.no_cache = True
		return resp
	return update_wrapper(new_func, f)

@lights.after_request
def add_no_cache(response):
	response.cache_control.no_cache = True
	response.headers.add('Last-Modified', datetime.datetime.now())
	response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
	response.headers.add('Pragma', 'no-cache')
	return response

@lights.route('/')
def index():
	locations=[]
	for loc in sorted(zwave.get_switches_locations()):
		location={}
		location['location']=loc
		location['url']=url_for('.with_location', location=loc)

		num_on = 0 ; num_off = 0 ; lights = 0

		switches = sorted(zwave.get_switches_from_location(loc))
		for switch in switches:
			lights += 1
			if switch['state']: num_on += 1
			else: num_off += 1

		dimmers = sorted(zwave.get_dimmers_from_location(loc))
		for dimmer in dimmers:
			lights += 1
			if dimmer['level']>0: num_on += 1
			else: num_off += 1

		location['num_lights']=lights
		location['num_lights_on']=num_on
		location['num_lights_off']=num_off
		location['has_lights_on']=(num_on>0)
		locations.append(location)
	if lights == 0:
		return render_template("locations.html", empty = True, page_title = "Lights")
	return render_template('locations.html', items = locations, page_title = "Lights")

@lights.route('/<location>')
def with_location(location):
	lights=[]
	for light in sorted (zwave.get_lights_from_location(location) ):
		if light.has_key("state"):
			light['switched_on'] = light['state']
			light['url'] = url_for('.with_switch',location=location, name=light['name'], node=light['node'])
		else:
			light['switched_on'] = light['level']>0
			light['url'] = url_for('.with_dimmer',location=location, name=light['name'], node=light['node'], level=light['level'])

		lights.append(light)
	return render_template('lights.html', items = lights, page_title=location)
		

@lights.route('/<location>/<name>/<node>')
def with_switch(location,name,node):
	device={}
	device['location']=location
	device['name']=name
	device['node']=node
	device['on']=zwave.get_switch_state( device['node'] )
	return render_template('switch.html', device=device)

@lights.route('/<location>/<name>/<node>/<level>')
def with_dimmer(location,name,node,level):
	device={}
	device['location']=location
	device['name']=name
	device['node']=node
	device['on']=zwave.get_switch_state( device['node'] )
	return render_template('dimmer.html', device=device)
