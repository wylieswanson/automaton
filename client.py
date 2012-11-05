#!/usr/bin/env python

import jsonrpclib, time
from pprint import pprint

zwave = jsonrpclib.Server("http://localhost:8080")

def f7(seq):
	seen = set()
	seen_add = seen.add
	return [ x for x in seq if x not in seen and not seen_add(x)]

def unique_locations():
	locations=[]
	for location in zwave.get_switches_locations(): locations.append(location)
	for location in zwave.get_dimmers_locations(): locations.append(location)
	pprint( sorted( f7(locations) ) )

def switches_info():
	locations = sorted (zwave.get_switches_locations() )
	pprint(locations)
	for location in locations:
		switches = sorted (zwave.get_switches_from_location(location) )
		num_switches_on = 0
		num_switches_off = 0
		for switch in switches:
			if switch['state']: num_switches_on += 1
			else: num_switches_off += 1
			# pprint(switch)
		print "%s: on=%s, off=%s" % (location, num_switches_on,num_switches_off)

def dimmers_info():
	locations = sorted (zwave.get_dimmers_locations() )
	pprint(locations)
	for location in locations:
		dimmers = sorted (zwave.get_dimmers_from_location(location) )
		num_dimmers_on = 0
		num_dimmers_off = 0
		for dimmer in dimmers:
			if dimmer['level'] > 0: num_dimmers_on += 1
			else: num_dimmers_off += 1
			# pprint(switch)
		print "%s: on=%s, off=%s" % (location, num_dimmers_on,num_dimmers_off)

#print zwave.ozw_library_version(),
#print zwave.python_ozw_library_version(),
#print zwave.zw_library_version(),
#print zwave.home_id()
#print zwave.controller_node_id(),
#print zwave.controller_node_version(),
#print zwave.nodes()
#print zwave.controller_capabilities() # error	
#print zwave.controller_node_capabilities() # error
#print zwave.controller_stats()

# print zwave.print_nodes()

#print zwave.print_all_lights()
print zwave.print_all_dimmers()

print "------------------------------------------------------------"
switches_info()
print "------------------------------------------------------------"
dimmers_info()
#print "------------------------------------------------------------"

#zwave.all_lights_off()
#time.sleep(1.0)
#zwave.all_lights_on()

#print zwave.test()

#zwave.light_on(2)
#time.sleep(3.0)
#zwave.light_on(8)

#zwave.set_dimmer(13,25)
#time.sleep(5)
#zwave.set_dimmer(13,0)
#time.sleep(5)
#print zwave.set_dimmer(13,0)
#time.sleep(3)
# zwave.set_dimmer(13,0)
#print zwave.get_dimmer_level(13)

# unique_locations()

#print zwave.get_switch_state(3)
#print zwave.get_switch_state(7)
