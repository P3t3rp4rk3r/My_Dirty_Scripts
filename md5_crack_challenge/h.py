import crypt
salt = 'shishaclub'
with open('wordlist.txt','rb') as f:
         for password in f:
                  print(crypt.crypt(password.strip(),salt))
