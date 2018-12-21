#!/usr/bin/env python
from __future__ import print_function
import json
import pprint
import argparse

def flatten_json(y,namespace="json",delim="."):
        name=namespace+delim
	out={}
	def flatten(x, name='',delim=delim):
		if type(x) is dict:
			for a in x:
				flatten(x[a], name + a + delim)
			out[name[:-len(delim)]]=list(x.keys())

		elif type(x) is list:
			i=0
			for a in x:
				flatten(a, name + str(i) + delim)
				i+=1
			out[name[:-len(delim)]]=list(range(0,i))
		else:
			out[name[:-len(delim)]] = x

	flatten(y,name=namespace+delim)
	return out

parser = argparse.ArgumentParser(description="Flatten a json file into single name value pairs for use with CMake.")
parser.add_argument("jsonfile", help="Name of json file to flatten",type=str)
parser.add_argument("--output", help="Name of output file to write to",type=str)
parser.add_argument("--name", help="Namespace to use for json variables",type=str,default="json")
parser.add_argument("--delim", help="Delimiter to use for namespace separation",type=str,default=".")
args=parser.parse_args()

with open(args.jsonfile,'r') as json_file:
	json_obj = json.load(json_file)
        flat=flatten_json(json_obj,namespace=args.name,delim=args.delim)
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
