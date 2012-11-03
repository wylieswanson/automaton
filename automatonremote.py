#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, request, make_response
from handler.lights import lights
from handler.tv import tv
from functools import update_wrapper
import jsonrpclib, datetime

# from handler.videos import videos
# from handler.recordings import recordings
# from handler.remote import remote
# from handler.settings import settings

app = Flask(__name__)
app.register_blueprint(lights, url_prefix='/Lights')
app.register_blueprint(tv, url_prefix='/TV')

def nocache(f):
	def new_func(*args, **kwargs):
		resp = make_response(f(*args, **kwargs))
		resp.cache_control.no_cache = True
		return resp
	return update_wrapper(new_func, f)

@app.after_request
def add_no_cache(response):
	response.cache_control.no_cache = True
	response.headers.add('Last-Modified', datetime.datetime.now())
	response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
	response.headers.add('Pragma', 'no-cache')
	return response

@app.route('/_switch', methods=['POST', 'GET'])
@nocache
def switch():
	zwave = jsonrpclib.Server("http://localhost:8080")
	error = None
	if request.method == 'POST':
		id = request.form['id'].rsplit('_')
		node = int(id[2])
		val = request.form['val']

		if (val=='on'): zwave.light_on(node)
		else: zwave.light_off(node)
	return jsonify(result=1)

@app.route('/')
@nocache
def root():
	"""
	This renders the very first page
	"""
	return render_template('index.html')

if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0', port=80)
	# app.run(host='0.0.0.0', port=5678)
