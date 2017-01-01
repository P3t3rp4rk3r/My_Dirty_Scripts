__author__ = "Santhosh Baswa"
__copyright__ = "Copyright 2016, Penetration Testing"

import requests
import json
import re
import simplejson
a = raw_input("Enter the email:")
r = requests.get("https://haveibeenpwned.com/api/v2/breachedaccount/"+a)
res = json.loads(r.text)
url_pattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
a = len(res)
if  r.status_code == 200:
         print "Email:" , a
         for i in res:
                  print "Domain:" , i['Domain']
                  print "Leakedaccounts:" , i['PwnCount']
                  print "Domain:", i['Domain']
                  print "BreachDate:", i['BreachDate']
                  print "AddedDate:", i['AddedDate']
                  links = i['Description']
                  find_links = re.findall(url_pattern, links)
                  print "Links:", "\n".join([str(x) for x in find_links])
