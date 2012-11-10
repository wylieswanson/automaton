#!/usr/bin/env python

import operator
import jsonrpclib, time
from pprint import pprint

ozw = jsonrpclib.Server("http://localhost:8080")

def f7(seq):
	seen = set()
	seen_add = seen.add
	return [ x for x in seq if x not in seen and not seen_add(x)]

def unique_locations():
	locations=[]
	for location in ozw.get_switches_locations(): locations.append(location)
	for location in ozw.get_dimmers_locations(): locations.append(location)
	pprint( sorted( f7(locations) ) )

def switches_info():
	locations = sorted (ozw.get_switches_locations() )
	pprint(locations)
	for location in locations:
		switches = sorted (ozw.get_switches_from_location(location) )
		num_switches_on = 0
		num_switches_off = 0
		for switch in switches:
			if switch['state']: num_switches_on += 1
			else: num_switches_off += 1
			# pprint(switch)
		print "%s: on=%s, off=%s" % (location, num_switches_on,num_switches_off)

def dimmers_info():
	locations = sorted (ozw.get_dimmers_locations() )
	pprint(locations)
	for location in locations:
		dimmers = sorted (ozw.get_dimmers_from_location(location) )
		num_dimmers_on = 0
		num_dimmers_off = 0
		for dimmer in dimmers:
			if dimmer['level'] > 0: num_dimmers_on += 1
			else: num_dimmers_off += 1
			# pprint(switch)
		print "%s: on=%s, off=%s" % (location, num_dimmers_on,num_dimmers_off)

#print ozw.ozw_library_version(),
#print ozw.python_ozw_library_version(),
#print ozw.zw_library_version(),
#print ozw.home_id()
#print ozw.controller_node_id(),
#print ozw.controller_node_version(),
#print ozw.nodes()
#print ozw.controller_capabilities() # error	
#print ozw.controller_node_capabilities() # error
#print ozw.controller_stats()

# print ozw.print_nodes()

#print ozw.print_all_lights()
#print ozw.print_all_dimmers()

#print "------------------------------------------------------------"
#switches_info()
#print "------------------------------------------------------------"
#dimmers_info()
#print "------------------------------------------------------------"

#ozw.all_lights_off()
#time.sleep(1.0)
#ozw.all_lights_on()

#print ozw.test()

#ozw.light_on(6)
#time.sleep(3.0)
#ozw.light_on(8)

#ozw.set_dimmer(13,25)
#time.sleep(5)
#ozw.set_dimmer(13,0)
#time.sleep(5)
#print ozw.set_dimmer(13,0)
#time.sleep(3)
# ozw.set_dimmer(13,0)
#print ozw.get_dimmer_level(13)

# unique_locations()

#print ozw.get_switch_state(3)
#print ozw.get_switch_state(7)

#unique_locations()

#pprint ( ozw.get_switches_dimmers_locations() )

lights = ozw.get_switches_dimmers()
#pprint( ozw.get_switches_dimmers() )

pprint(lights)
print "---"

sorted_locations= sorted( lights, key=operator.itemgetter('location'))
seen = set()
seen_add = seen.add

print "---"
unique_locations=[]
for location in sorted_locations:
	if location['location'] not in seen and not seen_add(location['location']):
		unique_locations.append(location['location'])
pprint(unique_locations)
print "---"

for location in unique_locations:
	num_lights_location=0 ; num_on_location=0
	for specific_light in sorted_locations:
		if specific_light['location'] in location:
			num_lights_location += 1
			if specific_light['state']==True or specific_light['level']>0:  num_on_location += 1
	print "%s (lights, #on) = %s/%s" % (location, str(num_lights_location), str(num_on_location))
	
	
