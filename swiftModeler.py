#!/usr/bin/env python3
import json
import sys
import re


swiftModelTemplate = '''import Foundation

struct ModelName : Codable, Identifiable {
}

'''

# Functions
def getListOfWhat(lst):
	retVal = ""
	if bool(lst) and isinstance(lst, list) and all(isinstance(elem, float) for elem in lst):
		retVal = "float"
	elif bool(lst) and isinstance(lst, list) and all(isinstance(elem, int) for elem in lst):
		retVal = "int"
	else:
		retVal = "str"
	
	return retVal

	
def getSwiftType(pythonType):
	if pythonType == "int":
		return "Int"
	if pythonType == "float":
		return "Double"
	if pythonType == "str":
		return "String"
	if pythonType == "[float]":
		return "[Double]"
	if pythonType == "[str]":
		return "[String]"
	if pythonType == "[int]":
		return "[Int]"
	

def updateSwiftFile(propTypes, modelName):
	"""
		Generates a swift file string,
		this function adds the properties and their types in the string, then returns the string of the swift file.
		
		the returned string consists of the imported libraries and the struct
		
		e.g. of returned string

			import Foundation
			
			struct Product : Codable, Identifiable {
				let id: Int?
				let name : String?
				let image : String?
				let price : Int?
			}

	"""
	
	retVal = swiftModelTemplate.replace("ModelName", modelName)
	
	for key, value in propTypes.items():
		retVal = retVal.replace("}", "\tlet {} : {}?\n}}".format(key, getSwiftType(value)))
	return retVal
	

def getPropertyAndTypes(data):
	"""
		data is a list of objects
		e,g,:
		[
			{
				"id" : 1,
				"name" : "Blue helmet",
				"image" : "helmet-no6",
				"price" : 199,
				"description" : "aaaaaa",
				"color" : [
					0.61,
					0.8,
					0.89
				]
			},
			{
				"id" : 2,
				"name" : "Yellow helmet",
				"image" : "helmet-no2",
				"price" : 159,
				"description" : "aaaaaabcd",
				"color" : [
					0.97,
					0.87,
					0.49
				], 
				"age" : 35.4
			}
		]

		e.g. of returned value:
			{'id': 'int', 
			'name': 'str', 
			'image': 'str', 
			'price': 'int', 
			'description': 'str', 
			'color': 'list', 
			'age': 'float'}

	"""
	
	propertiesDict = dict()
	for obj in data:
		for (index, key) in enumerate(obj.keys()):
			typeOfValue = list(obj.values())[index]
			if type(typeOfValue).__name__ == "list":
				valueTypeString = "[{}]".format(getListOfWhat(typeOfValue))
			else:
				valueTypeString = type(list(obj.values())[index]).__name__
			propertiesDict[key] = valueTypeString
	return propertiesDict

def saveSwiftFile(fileName, content):
	try:
		f = open(fileName, "w")
		f.write(content)
		
	except Exception as error:
		print(error)
		sys.exit(2)
	finally:
		if not f.closed:
			f.close()

# Main function
def main(argv):
	"""
		args at:
			0: script name (not used)
			1: json file name. e.g. playsers.json
			
	"""

	if not argv or len(argv) < 3:
		print("the json file path is required")
		print("e.g. python3 pyJson.py data.json ModelName\n\n")
		exit(0)
	if not argv[1]:
		print("the json file path is required")
		exit(0)
	if not argv[2]:
		print("the model name is required. e.g. User, Player, Product...etc")
		exit(0)
		
	jsonFile = argv[1]
	modelName = argv[2]
	fileName = "{}.swift".format(modelName)
	f = None
	swiftFileString = ""
	try:
		f = open(jsonFile,)
		data = json.load(f)
		propertiesDict = getPropertyAndTypes(data)		# this is a dict of key (property) and value (property type)
		swiftFileString = updateSwiftFile(propertiesDict, modelName)
		
	except Exception as error:
		print(error)
		sys.exit(2)
	finally:
		if not f.closed:
			f.close()
	saveSwiftFile(fileName, swiftFileString)
	print("The file {} is created.\nModel name: {}".format(fileName, modelName))
if __name__ == "__main__":
	main(sys.argv)
	