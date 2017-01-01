__author__ = "Santhosh Baswa"
__copyright__ = "Copyright 2016, Independent Security Research"

from DNSDumpsterAPI import DNSDumpsterAPI

a = raw_input("Enter the target:")
res = DNSDumpsterAPI(False).search(a)
#print res
print "[+] Domain "
print res['domain']

print "[+] DNS Servers"
for entry in res['dns_records']['dns']:
         print("{domain} {ip} {as} {provider} {country} {header}".format(**entry))

print "{+} MX Records"
for entry in res['dns_records']['mx']:
    print("{domain} ({ip}) {as} {provider} {country} {header}".format(**entry))

print "[+] Host Records"

for entry in res['dns_records']['host']:
    if entry['reverse_dns']:
        print("{domain} ({reverse_dns}) ({ip}) {as} {provider} {country} {header}".format(**entry))
    else:
        print("{domain} ({ip}) {as} {provider} {country} {header}".format(**entry))

print "[+] TXT Records"

for entry in res['dns_records']['txt']:
	print entry

print "[+] Image Save"
image_retrieved = res['image_data'] is not None
print "\n\n\nRetrieved Network mapping image? {} (accessible in 'image_data')".format(image_retrieved)
#print repr(res['image_data'].decode('base64')[:20]) + '...'
print "Created"+a+".png"
open(a+'.png','wb').write(res['image_data'].decode('base64'))
print "[+] Image Saved Successfully ..!!!"


print "[+] XLSX File"

xls_retrieved = res['xls_data'] is not None
print "\n\n\nRetrieved XLS hosts? {} (accessible in 'xls_data')".format(xls_retrieved)
#print repr(res['xls_data'].decode('base64')[:20]) + '...' # to save it somewhere else.
print "Created"+a+".xlsx"
open(a+'.xlsx','wb').write(res['xls_data'].decode('base64'))
print "[+] XLSX Saved Successfully ..!!!"
