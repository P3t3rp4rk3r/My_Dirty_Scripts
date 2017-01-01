import md5
import hashlib
import os
salt = 'shishaclub'
md5_salt = md5.new(salt).hexdigest()

with open('wordlist.txt','rb') as f:
         for password in f:
                  md5_pass = md5.new(password).hexdigest()
                  s = str(salt+password.strip())
                  s1 = str(password.strip()+salt)
                  print(s+"="+md5.new(s).hexdigest())
                  print(s1+"="+md5.new(s1).hexdigest())
                #  print(md5.new(md5_salt+md5_pass).hexdigest())
