__author__ = "Santhosh Baswa"
__copyright__ = "Copyright 2016, Independent Security Research"

from urlparse import urlparse
import re
import socket
import sqlite3
a = raw_input("Enter the db:")
conn = sqlite3.connect(a)
c = conn.cursor()

def host_to_ip(host):
        try:
            ips = socket.gethostbyname_ex(host)
        except socket.gaierror:
            ips=[]
        return ips

lines = [line.rstrip('\n') for line in open('feed_1.txt')]
for i in lines:
         parse_domain = urlparse(i)
                 # print type(parse_domain.netloc)
         url = parse_domain.netloc
         ips = host_to_ip(url)
         str_ips = ','.join(map(str,list(ips)))
                #print str_ips
         found = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})',str_ips)
         if found is not None:
             l = list(set(found))
             for j in l:
                  print i         
#print db_out()
                  #print "[+] Adding to Database"
                         #  (phishpage domain ipaddr)
                  c.execute("INSERT INTO openphishdb (phishpage,domain,ipaddr) VALUES (?,?,?)",(str(i),str(url),str(l)))
                  print "[+] Inserted ..!!"
conn.commit()
c.execute("SELECT * FROM openphishdb")
for row in c:
         print(row)
conn.close()   
