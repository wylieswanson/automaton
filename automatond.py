#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import os, sys, logging, time

from SocketServer import ThreadingMixIn
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

logging.getLogger('openzwave').addHandler(logging.NullHandler())
#logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('openzwave')

import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from pprint import pprint

class SimpleThreadedJSONRPCServer(ThreadingMixIn, SimpleJSONRPCServer):
	pass

class ZWaveManager():

	def	__init__( self ):
		device="/dev/ttyUSB0"
	
		options = ZWaveOption( "/dev/ttyUSB0", \
			config_path=os.path.expanduser("~/.zwave/config/"), \
			#user_path='.', \
			user_path=os.path.expanduser("~/.zwave/"), \
			cmd_line="")

		options.set_append_log_file(False)
		options.set_console_output(False)
		options.set_save_log_level('Info')

		options.set_logging(False)
		options.lock()

		self.network = ZWaveNetwork(options, log=None)

		# Waiting for driver
		for i in range(0,20):
			if self.network.state>=self.network.STATE_INITIALISED: break
			else: time.sleep(1.0)

		if self.network.state<self.network.STATE_INITIALISED:
			print "Can't initialise driver! Look at the logs in OZW_Log.log"
			quit(1)
	
		# Waiting for network ready
		for i in range(0,90):
			if self.network.state>=self.network.STATE_READY: break
			else: time.sleep(1.0)
		if not self.network.is_ready:
			print "Can't start network! Look at the logs in OZW_Log.log"
			quit(2)
		
	def print_nodes(self):
		for node in self.network.nodes:
			pprint(self.network.nodes[node])
			print
			print "------------------------------------------------------------"
			print "%s - Name : %s" % (self.network.nodes[node].node_id,self.network.nodes[node].name)
			print "%s - Manufacturer name / id : %s / %s" % (self.network.nodes[node].node_id,self.network.nodes[node].manufacturer_name, self.network.nodes[node].manufacturer_id)
			print "%s - Product name / id / type : %s / %s / %s" % (self.network.nodes[node].node_id,self.network.nodes[node].product_name, self.network.nodes[node].product_id, self.network.nodes[node].product_type)
			print "%s - Version : %s" % (self.network.nodes[node].node_id, self.network.nodes[node].version)
			print "%s - Command classes : %s" % (self.network.nodes[node].node_id,self.network.nodes[node].command_classes_as_string)
			print "%s - Capabilities : %s" % (self.network.nodes[node].node_id,self.network.nodes[node].capabilities)
			print "%s - Neigbors : %s" % (self.network.nodes[node].node_id,self.network.nodes[node].neighbors)
			groups = {}
			for grp in self.network.nodes[node].groups :
				groups[self.network.nodes[node].groups[grp].index] = {'label':self.network.nodes[node].groups[grp].label, 'associations':self.network.nodes[node].groups[grp].associations}
			print "%s - Groups : %s" % (self.network.nodes[node].node_id, groups)
			values = {}
			for val in self.network.nodes[node].values :
				values[self.network.nodes[node].values[val].object_id] = {
					'label':self.network.nodes[node].values[val].label,
					'help':self.network.nodes[node].values[val].help,
					'command_class':self.network.nodes[node].values[val].command_class,
					'max':self.network.nodes[node].values[val].max,
					'min':self.network.nodes[node].values[val].min,
					'units':self.network.nodes[node].values[val].units,
					'data':self.network.nodes[node].values[val].data_as_string,
					'ispolled':self.network.nodes[node].values[val].is_polled
					}
			#print "%s - Values : %s" % (self.network.nodes[node].node_id, values)
			#print "------------------------------------------------------------"
			for cmd in self.network.nodes[node].command_classes:
				print "   ---------   "
				#print "cmd = ",cmd
				values = {}
				for val in self.network.nodes[node].get_values_for_command_class(cmd) :
					values[self.network.nodes[node].values[val].object_id] = {
						'label':self.network.nodes[node].values[val].label,
						'help':self.network.nodes[node].values[val].help,
						'max':self.network.nodes[node].values[val].max,
						'min':self.network.nodes[node].values[val].min,
						'units':self.network.nodes[node].values[val].units,
						'data':self.network.nodes[node].values[val].data,
						'data_str':self.network.nodes[node].values[val].data_as_string,
						'genre':self.network.nodes[node].values[val].genre,
						'type':self.network.nodes[node].values[val].type,
						'ispolled':self.network.nodes[node].values[val].is_polled,
						'readonly':self.network.nodes[node].values[val].is_read_only,
						'writeonly':self.network.nodes[node].values[val].is_write_only,
						}
				print "%s - Values for command class : %s : %s" % (self.network.nodes[node].node_id,
											self.network.nodes[node].get_command_class_as_string(cmd),
											values)
			print "------------------------------------------------------------"
		print
	
	def print_all_lights(self):
		values = {}
		for node in self.network.nodes:
			for val in self.network.nodes[node].get_switches() :
				print("node/name/location/version/index/instance : %s/%s/%s/%s/%s/%s" % (node, \
					self.network.nodes[node].name,
					self.network.nodes[node].location,
					self.network.nodes[node].version,
					self.network.nodes[node].values[val].index,
					self.network.nodes[node].values[val].instance))
				print("  label/help : %s/%s" % (self.network.nodes[node].values[val].label,self.network.nodes[node].values[val].help))
				print("  id on the network : %s" % (self.network.nodes[node].values[val].id_on_network))
				print("  state: %s" % (self.network.nodes[node].get_switch_state(val)))


	def all_switch_locations(self):
		values = {}
		locations = []
		for node in self.network.nodes:
			for val in self.network.nodes[node].get_switches() :
				#location = {}
				#location['location']=self.network.nodes[node].location
				#locations.append(location)
				locations.append(self.network.nodes[node].location)
		return locations
			
	def all_switches_in_location(self, location):
		values = {}
		switches = []
		switch = {}
		for node in self.network.nodes:
			for val in self.network.nodes[node].get_switches() :
				if self.network.nodes[node].location == location:
					switch['name']=self.network.nodes[node].name
					switch['node']=node
					switch['state']=self.network.nodes[node].get_switch_state(val)
					switches.append( switch  )
		return switches

	def get_switch_state( self, node ):
		node=int(node)
		for val in self.network.nodes[node].get_switches():
			return self.network.nodes[node].get_switch_state(val)

	def light_on(self,node):
		node=int(node)
		for val in self.network.nodes[node].get_switches() : self.network.nodes[node].set_switch(val,True)
		print "Node %s, Switch on" % (str(node))

	def light_off(self,node):
		node=int(node)
		for val in self.network.nodes[node].get_switches() : self.network.nodes[node].set_switch(val,False)
		print "Node %s, Switch off" % (str(node))

	def all_lights_on(self):
		for node in self.network.nodes:
			for val in self.network.nodes[node].get_switches() : self.network.nodes[node].set_switch(val,True)

	def all_lights_off(self):
		for node in self.network.nodes:
			for val in self.network.nodes[node].get_switches() : self.network.nodes[node].set_switch(val,False)

	def shutdown(self):
		self.network.stop()

	def test(self):
		return "life"


	def ozw_library_version(self):
		return self.network.controller.ozw_library_version

	def python_ozw_library_version(self):
		return self.network.controller.python_library_version

	def zw_library_version(self):
		return self.network.controller.library_description

	def home_id(self):
		return self.network.home_id_str

	def controller_node_id(self):
		return self.network.controller.node.node_id

	def controller_node_version(self):
		return self.network.controller.node.version

	def nodes(self):
		return self.network.nodes_count

	def controller_capabilities(self):
		return self.network.controller.capabilities

	def controller_node_capabilities(self):
		return self.network.controller.node.capabilities

	def controller_stats(self):
		return self.network.controller.stats

	
def main():
	print "Starting network."
	
	zwave = ZWaveManager()

	server = SimpleThreadedJSONRPCServer(('localhost', 8080))

	server.register_function(zwave.ozw_library_version)
	server.register_function(zwave.python_ozw_library_version)
	server.register_function(zwave.zw_library_version)
	server.register_function(zwave.home_id)
	server.register_function(zwave.controller_node_id)
	server.register_function(zwave.controller_node_version)
	server.register_function(zwave.nodes)
	server.register_function(zwave.controller_capabilities)
	server.register_function(zwave.controller_node_capabilities)
	server.register_function(zwave.controller_stats)

	server.register_function(zwave.print_nodes)

	server.register_function(zwave.print_all_lights)
	server.register_function(zwave.all_switch_locations)
	server.register_function(zwave.all_switches_in_location)


	server.register_function(zwave.all_lights_on)
	server.register_function(zwave.all_lights_off)
	server.register_function(zwave.light_on)
	server.register_function(zwave.light_off)
	server.register_function(zwave.test)
	
	server.register_function(zwave.get_switch_state)

	print "Network started."
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		print "Stopping network."
		zwave.shutdown()
		print "Network stopped."

if __name__ == '__main__':
	main()

