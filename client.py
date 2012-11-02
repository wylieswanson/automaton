#!/usr/bin/env python

import jsonrpclib, time
from pprint import pprint

zwave = jsonrpclib.Server("http://localhost:8080")

def switchinfo():
	locations = sorted (zwave.all_switch_locations() )
	pprint(locations)
	for location in locations:
		switches = sorted (zwave.all_switches_in_location(location) )
		num_switches_on = 0
		num_switches_off = 0
		for switch in switches:
			if switch['state']: num_switches_on += 1
			else: num_switches_off += 1
			# pprint(switch)
		print "%s: on=%s, off=%s" % (location, num_switches_on,num_switches_off)

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

#zwave.print_nodes()
#zwave.print_all_lights()

switchinfo()

#zwave.all_lights_off()
#time.sleep(1.0)
#zwave.all_lights_on()

#print zwave.test()

#zwave.light_on(2)
#time.sleep(3.0)
zwave.light_off(8)

#print zwave.get_switch_state(3)
#print zwave.get_switch_state(7)
