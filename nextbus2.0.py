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
	def __init__(self, route = None, direction = None, stop = None, departures = 1):
		self.route = route
		self.direction = direction
		self.stop = stop
		self.departures = departures

	def answerInquiry(self):
		answer = None
		# If no route passed, find all routes
		if not self.route:
			answer = self.getAllRoutes()

		# If no stop passed, then find all stops for this route and direction
		elif not self.stop:
			answer = self.getAllStops()
		
		else:	
			answer = self.getNextDeparture()

		return answer

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
		return api.getNextDeparture(self.route, self.direction, self.stop, self.departures)

	def getAllStops(self):
		return api.getAllStops(self.route, self.direction)

	def getAllRoutes(self):
		return api.getAllRoutes()

def main(args):

	# Print usage if help requested
	if ("-h" in args) or ("--help" in args):
		sys.exit(
			"Welcome to NextBus.\n" +
			"Usage:\tnextbus <BUS ROUTE> [DIRECTION] [BUS STOP NAME] [NUMBER OF UPCOMING DEPARTURES]\n")

	aBus = None
	inquiryLabel = ""

	# Inquiry is all bus routes
	if len(args) == 1:
		aBus = NextBus()
		inquiryLabel = "Available routes"

	# Can't pass only two arguments 
	elif len(args) == 2:
		busRoute = args[1]
		sys.exit(
			"Sorry, we need a cardinal direction (north/south, east/west)\n" +
			"to show you stops for route " + busRoute + ".\n")

	# Inquiry is only bus route and direction, so return all stops		
	elif len(args) == 3:
		busRoute, direction = args[1:]
		aBus = NextBus(route = str(busRoute), direction = str(direction))
		inquiryLabel = "Available stops for route " + busRoute + " going " + direction

	# Inquiry is next departure time
	elif len(args) == 4:
		busRoute, direction, stopName = args[1:4]
		aBus = NextBus(route = str(busRoute), direction = str(direction), 
			stop = str(stopName))
		inquiryLabel = "Next departure(s) for " + busRoute + " at stop " + stopName

	# Inquiry is multiple departure times
	else:
		busRoute, direction, stopName, quantity = args[1:5]
		aBus = NextBus(route = str(busRoute), direction = str(direction), 
			stop = str(stopName), departures = int(quantity))
		inquiryLabel = "Next departure(s) for " + busRoute + " at stop " + stopName

	# Retrieve and print the answer
	inquiryResult = aBus.answerInquiry()
	print(inquiryLabel, ":\n\n", inquiryResult, sep = "")

if __name__ == "__main__": 
	main(sys.argv)