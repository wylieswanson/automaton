#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, request, make_response
from handler.lights import lights
from functools import update_wrapper
import jsonrpclib

# from handler.videos import videos
# from handler.recordings import recordings
# from handler.remote import remote
# from handler.settings import settings

app = Flask(__name__)
app.register_blueprint(lights, url_prefix='/Lights')
zwave = jsonrpclib.Server("http://localhost:8080")


def nocache(f):
	def new_func(*args, **kwargs):
		resp = make_response(f(*args, **kwargs))
		resp.cache_control.no_cache = True
		return resp
	return update_wrapper(new_func, f)


@app.after_request
def add_no_cache(response):
   if request.method == 'POST':
      response.cache_control.no_cache = True
   return response


@app.route('/_switch', methods=['POST', 'GET'])
@nocache
def switch():
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
