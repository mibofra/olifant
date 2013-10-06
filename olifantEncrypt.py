"""
This class handles encryption stuff and is used
to make an authentication token to put on usb.
It is used to check token too
*NOT COMPLETE YET!!!*
"""

import uuid
import hashlib
import random

class TokenFactory:
	mac_addr = None
	salt = None
	pwd = None

	def __init__(self):
		random.seed(None)
		self.mac_addr = str(uuid.getnode())
		self.salt = str(random.randint(1,1000))

	def makeToken(self,pwd):
		self.pwd = pwd
		sha1_fun = hashlib.sha1() 	#we get a sha1 function
		
		self.m
		
		str1 = self.md5_fun.digest()
		
		self.sha1_fun.update(str1)
		self.sha1_fun.update(pwd)

		return self.sha1_fun.digest()
		
		
tf = TokenFactory()
print tf.makeToken('paafasfsgs')

