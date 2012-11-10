# -*- coding: utf-8 -*-

from flask import send_file, Blueprint, render_template, abort, Response, request, url_for, make_response, jsonify, stream_with_context
from flask.ext.login import (LoginManager, current_user, login_required, login_user, logout_user, UserMixin, AnonymousUser, confirm_login, fresh_login_required) 

import urllib2, base64

from functools import update_wrapper
import json, sys
import datetime
import jsonrpclib

cameras = Blueprint('cameras', __name__)

def nocache(f):
	def new_func(*args, **kwargs):
		resp = make_response(f(*args, **kwargs))
		resp.cache_control.no_cache = True
		return resp
	return update_wrapper(new_func, f)

@cameras.after_request
def add_no_cache(response):
	response.cache_control.no_cache = True
	response.headers.add('Last-Modified', datetime.datetime.now())
	response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
	response.headers.add('Pragma', 'no-cache')
	return response

@cameras.route('/')
@login_required
def index():
	locations=[]

	location={}
	location['name']='Courtyard'
	location['snapshot']='http://courtyard.pv.pingzero.net:8041/snapshot.cgi?user=automaton&pwd=automaton'
	location['video']='http://pv.pingzero.net:5678/Cameras/stream.mp4'
	locations.append(location)

	location={}
	location['name']='Backyard'
	location['snapshot']='http://backyard.pv.pingzero.net:8042/snapshot.cgi?user=automaton&pwd=automaton'
	location['video']='http://backyard.pv.pingzero.net:8042/videostream.cgi?user=automaton'
	locations.append(location)
	
	location={}
	location['name']='Kids'
	location['snapshot']='http://automaton.pv.pingzero.net:5678/cameras/get_image'
	location['video']='http://backyard.pv.pingzero.net:8042/videostream.cgi?user=automaton'
	locations.append(location)

	if len(locations) == 0:
		return render_template("cameras.html", empty = True, page_title = "Cameras")
	return render_template('cameras.html', items = locations, page_title = "Cameras")

@cameras.route('/Snapshot')
# @login_required
def snapshot():
	# req = urllib2.urlopen("http://backyard.pv.pingzero.net:8042/videostream.cgi?user=admin&pwd=plan3tma3rsk")
	#req = urllib2.urlopen("http://craft.pv.pingzero.net:8042")
	req = urllib2.urlopen("http://courtyard.pv.pingzero.net:8041/snapshot.cgi?user=automaton&pwd=")
	def generate():
		while True:
			chunk = req.read( 16*1024 )
			if not chunk: break
			yield chunk
	return Response(stream_with_context(generate()))

@cameras.route('/stream.mp4')
# @login_required
def stream():
	# req = urllib2.urlopen("http://backyard.pv.pingzero.net:8042/videostream.cgi?user=admin&pwd=plan3tma3rsk")
	#req = urllib2.urlopen("http://craft.pv.pingzero.net:8042")
	req = urllib2.urlopen("http://10.0.10.11:8095/mystream.mp4")
	def generate():
		while True:
			chunk = req.read( 16*1024 )
			if not chunk: break
			yield chunk
	return Response(stream_with_context(generate()))

@cameras.route('/get_image')
@nocache
def get_image():
	# http://10.0.10.173/tmpfs/snap.jpg?user=guest&pwd=automaton
	request = urllib2.Request("http://10.0.10.173/tmpfs/snap.jpg")
	username = 'admin'
	password = 'plan3tma3rsk'
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)   
	result = urllib2.urlopen(request)

	return send_file(result, mimetype='image/jpg', cache_timeout=1)
