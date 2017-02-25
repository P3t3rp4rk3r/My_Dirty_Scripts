#!/bin/python
#Team: r3b00t
#Author: P3t3rp4rk3r
import os
from io import BytesIO
from urllib2 import urlopen
from zipfile import ZipFile

pass_file='/tmp/password.csv'
sites='/tmp/list.csv'
vulnsites='https://github.com/pirate/sites-using-cloudflare/archive/master.zip'
pw_list = []
sites = []

if not os.path.isfile(sites):
    urlobj = urlopen(vulnsites)
    with ZipFile(BytesIO(urlobj.read())) as zf:
        zf.extract('sites-using-cloudflare-master/sorted_unique_cf.txt', '/tmp/')
        os.rename('/tmp/sites-using-cloudflare-master/sorted_unique_cf.txt', '/tmp/list.csv')

with open(sites, 'r') as f:
    for line in f.readlines():
        sites.append(line.rstrip())
f.close()

with open(pass_file, 'r') as f:
    for line in f.readlines():
        newline=line.split(',')[0].replace('http://','').replace('www.', '').lower().rstrip()
        pw_list.append(newline)
f.close()

result=sorted(list(set(pw_list) & set(sites)))
print(result)

