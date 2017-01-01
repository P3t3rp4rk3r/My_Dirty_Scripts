__author__ = "Santhosh Baswa"
__copyright__ = "Copyright 2016, Independent Security Researcher"

import json, sys, re, os
import requests
import getpass
import argparse
from datetime import datetime


companyId = ""
outputFilename = ""
accountUsername = ""
accountPassword = ""


def startRequest():
	pageNum = 1

	now = str(datetime.now()).replace(' ','_').replace(':','-')
	if outputFilename:
		outputFile = open(sys.path[0] + '/output/' + outputFilename, 'w')
	else:
		outputFile = open(sys.path[0] + '/output/' + now + '.csv', 'w')

	#Preparing file
	outputFile.write('first name, last name, role, id, linkedin url\n')

	try:
		# Logging in
		linkedinSession = requests.Session()
		r = linkedinSession.get('https://www.linkedin.com/')
		pattern = re.compile('name="loginCsrfParam" value="([^"]+)"')
		match = pattern.search(r.text)
		url = 'https://www.linkedin.com/uas/login-submit'
		params = {'session_key': accountUsername, 'session_password': accountPassword , 'loginCsrfParam': match.group(1)}
		r = linkedinSession.post(url, data=params)
	except Exception, e:
		print "Something went wrong during login."
	

	#Getting first page of employees from the company id
	response = linkedinSession.get('https://www.linkedin.com/vsearch/pj?f_CC=' + companyId + '&page_num=' + str(pageNum))
	response = json.loads(response.text)['content']

	#Trying to get information out of the first page of employees, checking for errors
	try:
		#How many results there are (thought most might be "Linkedin user")
		resultCount = int(response['page']['voltron_unified_search_json']['search']['formattedResultCount'].replace(',','').replace('.',''))
		dictOfResults = response['page']['voltron_unified_search_json']['search']['results']
	except Exception, e:
		print "Couldn't make sense of the server response page 1, something probably went wrong or maybe there are no results?"
		sys.exit()
	

	print "Got " + str(resultCount) + " results."
	

	print "Fetching results from page 1."
	moreReachableUsersAvailable = extractUsersAndWriteToFile(dictOfResults, outputFile)



	if resultCount > 10:

		#Fetching results from other pages (if they exist)
		while moreReachableUsersAvailable:

			pageNum += 1

			#Check if pageNum is bigger than 10, because a regular LinkedIn account can only look up to 10 pages.
			if pageNum > 10:
				print "Already got 10 pages, that is all you can get without a premium account."
				sys.exit()
			else:
				print "Fetching results from page " + str(pageNum) + "."
				response = linkedinSession.get('https://www.linkedin.com/vsearch/pj?f_CC=' + companyId + '&page_num=' + str(pageNum))

				try:
					response = json.loads(response.text)['content']
					dictOfResults = response['page']['voltron_unified_search_json']['search']['results']
				except Exception, e:
					print "Couldn't make sense of the server response page " + str(pageNum) + ". Maybe last page?"

				moreReachableUsersAvailable = extractUsersAndWriteToFile(dictOfResults, outputFile)

	print "Done."


		

def extractUsersAndWriteToFile(dictOfResults, outputFile):
	#This function writes results to file and returns false if there are no more reachable users in the results

	#Person object properties
	#firstName
	#lastName
	#fmt_headline - job description usually
	#fmt_location
	#image_url

	unreachableUserCount = 0

	for person in dictOfResults:
		
		p = person['person']
		
		firstName = p['firstName'].encode('ascii', 'ignore')

		#If the current user logged on can see the name, and not 'Linkedin Member'
		if firstName:
			lastName = p['lastName'].encode('ascii', 'ignore')
			#Remove HTML tags from headline
			headline = re.sub('<[a-zA-Z ="/]+>', '', p['fmt_headline'].encode('ascii', 'ignore'))
			personId = str(p['id'])
			profileLink = p['link_nprofile_view_3']
			line =  firstName + ',' + lastName + ',' + headline + ',' + personId + ',' + profileLink

			outputFile.write(line.rstrip(',') + '\n')
		else:
			unreachableUserCount += 1


	if len(dictOfResults) == unreachableUserCount:
		return False	
	return True

if __name__ == "__main__":

	#Create output folder if doesn't exist
	if not os.path.exists(sys.path[0] + '/output'):
		os.makedirs(sys.path[0] + '/output')
	
	parser = argparse.ArgumentParser(description='Linkedin employee enum.')
	parser.add_argument('-l', metavar='username', help='Username for login')
	parser.add_argument('-p', metavar='password', required=False, help='password for login')
	parser.add_argument('company_id', help='Company id (as seen in the company\'s url)')
	parser.add_argument('-o', '--o', metavar='output', required=False, nargs='?', help='output filename')
	args = parser.parse_args()

	companyId = args.company_id
	outputFilename = args.o

	if not args.l:
		accountUsername = raw_input("Username: ")
	else:
		accountUsername = args.l

	if not args.p:
		accountPassword = getpass.getpass("Password for " + accountUsername + ":" )
	else:
		accountPassword = args.p

	startRequest()
	
else:
	print __name__
	
