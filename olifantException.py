class OlifantException(Exception):
	"""
	A class for Olifant exceptions thrown by main module
	Each OlifantException has a specific error message

	You can use it this way:

	try:
		raise OlifantException('This is an error message')
	except OlifantException as a: #specify a variable a
		print a.getMessage() #print error message
	"""

	__message = None

	def __init__(self,errorMessage):
		Exception.__init__(self)
		self.__message = errorMessage

	def getMessage(self):
		return self.__message


