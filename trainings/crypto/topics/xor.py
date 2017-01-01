from Crypto.Cipher import XOR
import base64

def encrypt(key, plaintext):
  cipher = XOR.new(key)
  return base64.b64encode(cipher.encrypt(plaintext))

def decrypt(key, ciphertext):
  cipher = XOR.new(key)
  return cipher.decrypt(base64.b64decode(ciphertext))
plaintext = raw_input('Message:')
key = raw_input('key:')
ciphertext = encrypt(key,plaintext)
print "Ciphertext:", ciphertext
print "Plaintext:" , decrypt(key,ciphertext)

