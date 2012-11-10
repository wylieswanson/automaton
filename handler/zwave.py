# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort, Response, request, url_for, make_response, jsonify, redirect, flash
from flask.ext.login import (LoginManager, current_user, login_required, login_user, logout_user, UserMixin, AnonymousUser, confirm_login, fresh_login_required) 
from functools import update_wrapper
import operator
import json, sys, time, datetime, jsonrpclib

zwave = Blueprint('zwave', __name__)
ozw = jsonrpclib.Server("http://localhost:8080")

def nocache(f):
	def new_func(*args, **kwargs):
		resp = make_response(f(*args, **kwargs))
		resp.cache_control.no_cache = True
		return resp
	return update_wrapper(new_func, f)

@zwave.after_request
def add_no_cache(response):
   response.cache_control.no_cache = True
   response.headers.add('Last-Modified', datetime.datetime.now())
   response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
   response.headers.add('Pragma', 'no-cache')
   return response

def f7(seq):
   seen = set()
   seen_add = seen.add
   return [ x for x in seq if x not in seen and not seen_add(x)]

@zwave.route('/')
@nocache
@login_required
def index():

	lights = ozw.get_switches_dimmers() ; sorted_locations= sorted( lights, key=operator.itemgetter('location'))
	seen = set() ; seen_add = seen.add ; unique_locations=[]
	# get unique locations
	for location in sorted_locations:
		if location['location'] not in seen and not seen_add(location['location']):
			unique_locations.append(location['location'])

	# find out which lights are on and how many per location
	items=[]
	for location in unique_locations:
		num_lights_location=0 ; num_on_location=0
		for specific_light in sorted_locations:
			if specific_light['location'] in location:
				num_lights_location += 1
				if specific_light['state']==True or specific_light['level']>0:  num_on_location += 1
		item={}
		item['url']=url_for('.with_location', location=location)
		item['location']=location
		item['num_lights']=num_lights_location
		item['num_on']=num_on_location
		items.append(item)
		
	if len(unique_locations) == 0:
		return render_template("locations.html", empty = True, page_title = "Locations")
	return render_template('locations.html', items = items, page_title = "Locations")

@zwave.route('/scenes')
@nocache
@login_required
def scenes():
	return render_template('scenes.html', empty=True, page_title = "Scenes")

@zwave.route('/status')
@nocache
@login_required
def status():
	status=[]
	status['ozw_library_version']=ozw.ozw_library_version()

	return render_template('status.html', status=status, page_title = "Status")

@zwave.route('/update', methods=['POST', 'GET'])
@nocache
@login_required
def adjust():
	error = None
	if request.method == 'POST':
		id = request.form['id']
		node = request.form['node']
		device = request.form['device']
		action = request.form['action']
		location = request.form['locale']
		name = request.form['name']

		if (device=='switch'):
			state = request.form['state']
			if (state=='on'): 
				ozw.light_on(node)
				flash('%s %s %s node %s to %s by %s' % (location, name, device, node, state, action))
			else: 
				ozw.light_off(node)
				flash('%s %s %s node %s to %s by %s' % (location, name, device, node, state, action))

		elif (device=='dimmer'):
			if (action=='flip'):
				state = request.form['state']
				if (state=='on'): 
					ozw.set_dimmer(node,255)
					flash('%s %s %s node %s to %s by %s' % (location, name, device, node, state, action))
				else: 
					ozw.set_dimmer(node,0)
					flash('%s %s %s node %s to %s by %s' % (location, name, device, node, state, action))
			elif (action=='dim'):
				level = request.form['level']
				ozw.set_dimmer(node,level)
				flash('%s %s %s node %s to %s by %s' % (location, name, device, node, level, action))

	return jsonify(result=1)

@zwave.route('/alloff')
@nocache
@login_required
def alloff():
	for loc in sorted(ozw.get_switches_locations()):
		location={}
		location['location']=loc
		location['url']=url_for('.with_location', location=loc)

		num_on = 0 

		switches = sorted(ozw.get_switches_from_location(loc))
		for switch in switches:
			if switch['state']: 
				num_on += 1
				ozw.light_off(switch['node'])
				flash('Lights turned off in %s' % (location['location']))
				time.sleep(1)

		dimmers = sorted(ozw.get_dimmers_from_location(loc))
		for dimmer in dimmers:
			if dimmer['level']>0: 
				num_on += 1
				flash('Lights turned off in %s' % (location['location']))
				time.sleep(1)

	return redirect( url_for('.scenes'))
	
@zwave.route('/<location>')
@nocache
@login_required
def with_location(location):
	lights=[]
	for light in sorted(ozw.get_lights_from_location(location) ):
		lights.append(light)
	return render_template('lights.html', items = lights, page_title=location)


@zwave.route('/<location>/<name>/<node>')
@nocache
@login_required
def with_switch(location,name,node):
	device={}
	device['location']=location
	device['name']=name
	device['node']=node
	device['on']=ozw.get_switch_state( device['node'] )
	return render_template('switch.html', device=device)

@zwave.route('/<location>/<name>/<node>/<level>')
@nocache
@login_required
def with_dimmer(location,name,node,level):
	device={}
	device['location']=location
	device['name']=name
	device['node']=node
	device['on']=ozw.get_switch_state( device['node'] )
	return render_template('dimmer.html', device=device)
