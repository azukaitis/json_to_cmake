#!/usr/bin/env python
from __future__ import print_function
import json
import pprint
import argparse

def flatten_json(y,namespace="json"):
        name=namespace+"."
	out={}
	def flatten(x, name=''):
		if type(x) is dict:
			for a in x:
				flatten(x[a], name + a + '.')
			out[name[:-1]]=list(x.keys())

		elif type(x) is list:
			i=0
			for a in x:
				flatten(a, name + str(i) + '.')
				i+=1
			out[name[:-1]]=list(range(0,i))
		else:
			out[name[:-1]] = x

	flatten(y,name=namespace+".")
	return out

parser = argparse.ArgumentParser(description="Flatten a json file into single name value pairs for use with CMake.")
parser.add_argument("jsonfile", help="Name of json file to flatten",type=str)
parser.add_argument("--output", help="Name of output file to write to",type=str)
parser.add_argument("--name", help="Namespace to use for json variables",type=str,default="json")
args=parser.parse_args()

with open(args.jsonfile,'r') as json_file:
	json_obj = json.load(json_file)
        flat=flatten_json(json_obj,namespace=args.name)
	if( args.output ) : 
		f1=open(args.output,"w")
	for key in flat:
		if type(flat[key]) is list:
			output=" ".join(str(x) for x in flat[key])
		else:
			output=str(flat[key])
                mystring="set( " + str(key) + " " + output +" )\n"
		if( args.output ) : 
      			f1.write(mystring)
		print(mystring,end='')
	if( args.output ) : 
		f1.close()
