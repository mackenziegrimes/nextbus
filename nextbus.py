#!/usr/bin/env python

"""
Target GRE - API Consumption
nextbus.py
~~~~~~~~~~~~~~~~

Given a bus route, direction, and stop name,
this script prints out the next time of departure
using Metro Transit's NexTrip API

:copyright: (c) 2017 by Mackenzie Grimes

Usage:
> python3 nextbus.py {BUS_ROUTE} {BUS STOP NAME} {DIRECTION}

"""
import sys
import os.path
import transitAPI as api

class NextBus:
	def __init__(self, route, direction, stopName):
		self.route = route
		self.direction = direction
		self.stop = stopName

	"""
	class NextBus stores all information for nextBus inquiry
	and makes API calls to get the next departure 
	of the route of interest

	:param route: str of (partial) description of route
	:param direction: str of cardinal direction 
					{north, south, east, west}
	:param stop:
	"""
	def getNextDeparture(self):
		return api.getNextDeparture(self.route, self.direction, self.stop)

def main(args):
	# Test that enough arguments were passed
	if len(args) < 1:
		sys.exit(
			"Sorry, we're missing some arguments.\n" +
			"Usage:\tnextbus <BUS ROUTE> [BUS STOP NAME] [DIRECTION]\n")


	elif len(args) < 2:
		sys.exit(
			"Sorry, we're missing some arguments.\n" +
			"Usage:\tnextbus <BUS ROUTE> <BUS STOP NAME> <DIRECTION>\n")

	# Assign all command line arguments to this inquiry's details
	busRoute, stopName, direction = args[1:4]
	aBus = NextBus(str(busRoute), str(direction), str(stopName))

	# Retrieve next departure for inquiry and print
	nextDeparture = aBus.getNextDeparture()
	print("Next departure is", nextDeparture)

if __name__ == "__main__": 
	main(sys.argv)