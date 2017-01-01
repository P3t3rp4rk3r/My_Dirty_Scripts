__author__ = "Santhosh Baswa"
__copyright__ = "Copyright 2016, Independent Security Researcher"
import os
import json
import simplejson
import requests

a = raw_input("Enter the email:")
b = {'q':a}
r = requests.get('https://hacked-emails.com/api', params=b)
res = simplejson.loads(r.text)
a = range(int(res['results']))
if  r.status_code == 200:
	print "Email:" , res['query']
	print "Status:" , res['status']
	print "No.of.leaks:", res['results']
	for i in a:
		print "Leaked Data : Part-",i+1 
		print "Title of leak :" , res['data'][i]['title']
		print "Author :" , res['data'][i]['author']
		print "Verified leak :" , res['data'][i]['verified']
		print "Date leaked :" , res['data'][i]['date_leaked']
		print "Date published :" , res['data'][i]['date_created']
		print "Network :" , res['data'][i]['source_network']
		print "Site:" , res['data'][i]['source_provider']
		print "File size :" , res['data'][i]['source_size'] % 1024
		print "Emails found :" , res['data'][i]['emails_count']
		print "Details:" , res['data'][i]['details']
		print "Source URL:" , res['data'][i]['source_url']
		print "No. of lines :" , res['data'][i]['source_lines']
		print "------------xxxxxxxxxxxxx----------------"
#	print "Leak:" , res['data'][0]['title']
#	print "Source Network:", res['data'][0]['']
else:
	print "Email:" , res['query']
	print "Status:" , res['status']

