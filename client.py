#!/usr/bin/env python

import jsonrpclib, time
from pprint import pprint

server = jsonrpclib.Server("http://localhost:8080")

#print server.ozw_library_version(),
#print server.python_ozw_library_version(),
#print server.zw_library_version(),
#print server.home_id()
#print server.controller_node_id(),
#print server.controller_node_version(),
#print server.nodes()
#print server.controller_capabilities() # error	
#print server.controller_node_capabilities() # error
#print server.controller_stats()

#server.print_nodes()
#server.print_all_lights()
locations = sorted (server.all_switch_locations() )
pprint(locations)
for location in locations:
	switches = sorted (server.all_switches_in_location(location) )
	num_switches_on = 0
	num_switches_off = 0
	for switch in switches:
		if switch['state']: num_switches_on += 1
		else: num_switches_off += 1

		# pprint(switch)
	print "%s: on=%s, off=%s" % (location, num_switches_on,num_switches_off)

#server.all_lights_off()
#time.sleep(1.0)
#server.all_lights_on()

#print server.test()

#server.light_on(2)
#time.sleep(3.0)
server.light_off(8)

#print server.get_switch_state(3)
#print server.get_switch_state(7)
