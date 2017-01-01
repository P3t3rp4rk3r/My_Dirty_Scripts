#Author: P3t3rp4rk3r
#Access Code:
# Training Session 

import hashlib
print "[+] Hashing [+]"
msg = raw_input("Enter the Message:")
print "[+] List of Hashs "
print hashlib.algorithms
a = raw_input("Enter the Hash:")
h = hashlib.new(a)
h.update(msg)
print "[+]"+a+"sum:"+h.hexdigest()
print "[+] Execution done."

