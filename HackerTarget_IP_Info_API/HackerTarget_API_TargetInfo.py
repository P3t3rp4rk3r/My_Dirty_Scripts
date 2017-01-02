#!/usr/bin/env python
__author__ = "Santhosh Baswa"
__copyright__ = "Copyright 2016, Independent Security Researcher"

import os
import sys
import json
import urllib
import urllib2
import hashlib
import argparse
import re
import socket
from urllib2 import urlopen


def color(text, color_code):
    if sys.platform == "win32" and os.getenv("TERM") != "xterm":
        return text

    return '\x1b[%dm%s\x1b[0m' % (color_code, text)


def red(text):
    return color(text, 31)

def blue(text):
    return color(text, 34)



if __name__ == "__main__":

    my_ip = raw_input("Enter the IP Address:")

    print(blue('Get Reverse DNS, GeoIP, NMAP, Traceroute and pulls HTTP Headers for an IP address'))
    print(blue('A quick and dirty script by @jgamblin'))
    print('\n')
    print(red('Your Target IP address is {0}'.format(my_ip)))
    print('\n')

    #Get IP To SCAN

    resp = raw_input(blue('Would you like target info about {0}? (Y/N):'.format(my_ip)))

    if resp.lower() in ["yes", "y"]:
        badip = my_ip
    else:
        badip = raw_input(blue("What IP would you like to check?: "))

    print('\n')

    #IP INFO
    reversed_dns = urllib.urlopen('http://api.hackertarget.com/reverseiplookup/?q=' + badip).read()
    geoip = urllib.urlopen('http://api.hackertarget.com/geoip/?q=' + badip).read()
    nmap = urllib.urlopen('http://api.hackertarget.com/nmap/?q=' + badip).read()
    httpheaders = urllib.urlopen('http://api.hackertarget.com/httpheaders/?q=' + badip).read()
    tracert = urllib.urlopen('http://api.hackertarget.com/mtr/?q=' + badip).read()
 
    print(red('Reverse DNS Information:'))
    print(blue(reversed_dns))
    print('\n')
    print(red('GEOIP Information:'))
    print(blue(geoip))
    print('\n')
    print(red('NMAP of Traget (Only Ports: 21,25,80 and 443):'))
    print(blue(nmap))
    print('\n')
    print(red('HTTP Headers:'))
    print(blue(httpheaders))
    print('\n')
    print(red('Trace Route:'))
    print(blue(tracert))
    print('\n')
