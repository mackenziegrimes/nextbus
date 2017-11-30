#!/usr/bin/env python

"""
Target GRE - API Consumption
transitAPI.py
~~~~~~~~~~~~~~~~

This module is a wrapper for the Metro Transit NexTrip API.

:copyright: (c) 2017 by Mackenzie Grimes


Functions:

getRoutes 		-- 	returns dict of all Metro Transit routes
getStops 		-- 	returns dict of all stops for a route in one direction
					Note that it can take a route number or substring description of route
getDirections	--	returns dict of two valid directions for a bus
getDepartures 	-- 	returns dict of all scheduled departures for a stop
					of a route in one direction

Attribution:

Python API request library examples from
HVS (https://stackoverflow.com/users/318700/hvs)
"""

import sys
import os.path

import requests
import json


JSON_FORMAT = "?format=json"
NEXTRIP_URI = "http://svc.metrotransit.org/NexTrip/"


def prettyprint(data):
	"""
	Converts dict to nicely formatted JSON string

	:param data: dict of JSON data
	:rtype: str
	"""

	return json.dumps(data, indent = 4, sort_keys = True)


def directionToCode(cardinalDirection):
	"""
	Converts cardinal direction to Metro Transit direction code, 
	or None if invalid direction passed

	:param cardinalDirection: str that is north, south, east, west
	:rtype: int 
	"""	

	return {
		'south'	: '1',
		'east'	: '2',
		'west'	: '3',
		'north'	: '4'
	}.get(cardinalDirection, None)



def lookupStopId(stopName, stopDict):
	"""
	Finds 4-char string of Metro Transit stop ID 
	based on provided stop description
	
	:param stopName: str that is substring of stop description
	:param stopDict: dict of JSON data detailing possible stops
	:rtype: str
	"""

	for aStop in stopDict:
		if stopName in aStop["Text"]:
			return aStop["Value"]

	return None

	
def lookupRouteId(routeName, routesDict):
	"""
	Return integer of Metro Transit route ID 
	based on provided (partial) route description

	:param routeName: str that is substring of route description
	:param routesDict: dict of JSON data detailing possible routes
	:rtype: str
	"""

	for aRoute in routesDict:
		if routeName in aRoute["Description"]:
			return aRoute["Route"]

	return None

	
def convertDirection(cardinalDirection):
	"""
	Returns Metro Transit directionCode 
	or exits if invalid code passed

	:param cardinalDirection: str that is north, south, east, west
	:rtype: str
	"""

	directionCode = directionToCode(cardinalDirection)
	if not directionCode:
		sys.exit(
			"Could not recognize direction \"{0}\".\n".format(cardinalDirection) +
			"Please use north, south, east, or west.")

	return directionCode

def convertStopToId(stopName, stopDict):
	"""
	Returns Metro Transit stopID
	or exits if invalid stop name passed

	:param stopName: str that is substring of stop description
	:param stopDict: dict of JSON data detailing possible stops
	:rtype: str
	"""

	stopID = lookupStopId(stopName, stopDict)

	# If stopID was not found for this stop name, print error
	if not stopID:
		sys.exit(
			"Could not find stop name \"{0}\".".format(stopName))

	return stopID


def convertRouteToId(routeName, routesDict):
	"""
	Return integer of Metro Transit route ID 
	or exits if invalid route name

	:param routeName: str that is substring of route description
	:param routesDict: dict of JSON data detailing possible routes
	:rtype: str
	"""

	routeID = lookupRouteId(routeName, routesDict)
	if not routeID:
		sys.exit(
			"Could not find route name \"{0}\".".format(route))

	return routeID

def transitRequest(url):
	"""
	Takes argument of Metro Transit API Uri, calls and processes request
	and returns JSON dump, or None if failure

	:param url: str that is full URL to API endpoint
	:rtype: dict
	"""

	jData = {}
	transitResponse = requests.get(url)

	# For successful API call, response code will be 200 (OK)
	if transitResponse.ok:

	    # Load the response data into a dict variable
	    jData = json.loads(transitResponse.content)

	else:
	  	# If response code is not ok (200), 
	  	# print the resulting http error code with description
	    transitResponse.raise_for_status()

	return jData

	
def getRoutes():
	"""
	Returns JSON dump of all Metro Transit routes

	:rtype: dict
	"""

	url = (NEXTRIP_URI + "Routes" + JSON_FORMAT)
	return transitRequest(url)

	
def getDirections(route):
	"""
	Gets dict of two valid cardinal directions for given route

	:param route: str of Metro Transit route ID
	:rtype: dict
	"""

	url = (NEXTRIP_URI + "Directions/" + 
		route + JSON_FORMAT)

	return transitRequest(url)

	
def getStops(route, direction):
	"""
	Gets JSON dump of all stops for a route 
	travelling a certain direction
	
	:param route:
	:param direction: str of cardinal direction
	:rypte: dict
	"""

	directionCode = convertDirection(direction)

	# Search for routeID by route description
	routesDict = getRoutes()
	routeID = convertRouteToId(route, routesDict)
	#routeID = ""

	# If route cannot be converted to an int, 
	# must be route description, so lookup route ID
	# try:
	# 	routeID = route
	# 	int(route)
	# except:
	# 	routesDict = getRoutes()
	# 	routeID = lookupRouteId(route, routesDict)
	#
	# 	if str.isEmpty(routeID):
	# 		sys.exit(
	# 			"Could not find route name \"{0}\".".format(route))

	url = (NEXTRIP_URI + "Stops/" +
		routeID + "/" + directionCode + JSON_FORMAT)

	return transitRequest(url)

	
def getDepartures(route, direction, stop):
	"""
	Gets JSON dump of all scheduled departures from this stop for this route
	
	:param route: str of route description
	:param direction: str of cardinal direction
	:param stop: str of stop description (often intersection of streets)
	:rtype dict:
	"""

	# First, make API call to lookup the routeID
	# and lookup the stopID by route and stop descriptions
	stopsDict = getStops(route, direction)
	stopID = convertStopToId(stop, stopsDict)

	routesDict = getRoutes()
	routeID = convertRouteToId(route, routesDict)

	directionCode = convertDirection(direction)

	url = (NEXTRIP_URI +
		routeID + "/" + directionCode + "/" + stopID + JSON_FORMAT)

	return transitRequest(url)

	
def getNextDeparture(route, direction, stop):
	"""
	Gets time (in human readable text) of next departure for route
	or none if route has no more departures today.
	Mostly just a wrapper for getDepartures().

	:param route: str of route description
	:param direction: str of cardinal direction
	:param stop: str of stop description (often intersection of streets)
	:rtype dict:
	"""

	# Retrieve all departures for this route, and return first one 
	allDepartures = getDepartures(route, direction, stop)
	nextDeparture = None

	# If departures dict found, return the first departure's time
	if allDepartures:
		nextDeparture = allDepartures[0]["DepartureText"]

	return nextDeparture
