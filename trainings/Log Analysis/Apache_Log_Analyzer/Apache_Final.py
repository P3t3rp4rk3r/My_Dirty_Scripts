#Author: P3t3rp4rk3r
#Team: r3b00t
import re		
import os
from geoip import geolite2
os.system("figlet -t Apache Log Analyzer")
print '\033[1m' + '\n\t\t\t\t\t\t\t\t\t\t\t\t -P3t3rp4rk3r' + '\033[0m'
def parse_logs():
	try:
		access_file=raw_input("Enter filename:")	# Enter File Location
		f = open(access_file,'r')			# Read the file
		print("[+] Accessing file ...!!!"+access_file)
	except IOError:
		print 'Log file does not exist'
		return
	log_regx = re.compile(r'(.*?) - - \[(.*?)\] "GET (.*?)HTTP\/1.\d" (\d+)') #Regular expression to parse logfile
  	logs = f.readlines()
  	logs_parsed = []
  	logs_parsed.append(['URL', 'Request', 'Country', 'Location (lat/long)'])  #Append to list
  	for l in logs:
		m = re.match(log_regx, str(l))
		if m:
			print("[+] Extracting Information (200 OK) Requests...!!!") # Extracting 200 OK requests
			if m.group(4) == '200':
				row = []
				try:
				  ipmatch = geolite2.lookup(m.group(1))
				except:
				  ipmatch = None
				if ipmatch is not None:
					row.append(m.group(1))
					row.append(m.group(3))
					row.append(ipmatch.country)
					row.append(ipmatch.location)
				else:
					row.append(m.group(1))
					row.append(m.group(3))
					row.append('N/A')
					row.append('N/A')
				logs_parsed.append(row)
			#Non 200 requests are avoided
			#else: print l
	print_report(logs_parsed)
def print_report(loglist):
	print("[+] Generate log_report.html ")	# Genrate HTML Report
	f = open('log_report.html', 'w')
	f.write("""
		<html>
		<head>
		<title> Apache Log Report </title>
		<body>
		<table border="1" style="width:100%">
		""")
	f.close()
	f = open('log_report.html', 'a')	
	for l in loglist:
		if l[0] == 'URL':
			str1 = '''<tr>
			<td><h3>%s<h3></td>
			<td><h3>%s<h3></td>
			<td><h3>%s<h3></td>
			<td><h3>%s<h3></td>
			</tr>''' % (l[0], l[1], l[2], l[3])
			f.write(str1)
		else:
			str1 = '''<tr>
			<td>%s</td>
			<td>%s</td>
			<td>%s</td>
			<td>%s</td>
			</tr>''' % (l[0], l[1], l[2], l[3])
			f.write(str1)
	os.system("firefox log_report.html")	# Open HTML Report in Google Chrome
	f.close()
if __name__ == '__main__':
#	print "Processing Apache Log File\n\n"
	parse_logs()
