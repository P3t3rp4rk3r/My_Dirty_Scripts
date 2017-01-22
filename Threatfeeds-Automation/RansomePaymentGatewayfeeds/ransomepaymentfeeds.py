#!/usr/bin/python
import requests

if __name__ == '__main__':
    ioc = []
    feed_file = requests.get('https://files.deependresearch.org/feeds/ransomware/ransomware-payment-sites.txt', verify=False).content
    outfile = 'domain,notes\n'
    for line in feed_file.splitlines():
        if line.startswith('#') or '.' not in line:
            continue
        outfile += '%s,Suspected Ransomware Payment Site\n' % line
    with open('ransomware_payment_site.csv', 'w') as fh:
        fh.write(outfile)

#Use in Splunk environment set a query using'inputlookup' option
	
