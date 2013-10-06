from ctypes import cdll
import threading
import time

lib = cdll.LoadLibrary('./libpowerlock.so') #this is the C library which does magic

class PowerLocker(object):
	"""
	A class which locks power button on linux
	so that it has no effect
	"""
	
	__buttonPressed = False #it will be true if someone presses power button (just for active mode)

	def __init__(self):
		self.obj = lib.PowerLocker_new()

	def power_lock(self):
		"""
		Locks power button: from this moment on it will not work! 
		Be aware that this operation requires admin rights.
		Returns 1 if successful 0 otherwise
		"""
		return lib.lock_power(self.obj)

	def active_power_lock(self):
		"""
		Same of power_lock but blocks until power button is pressed,
		useful to detect pressing: when button is pressed wasButtonPressed
		function will return true (power button will still be disabled
		untile unlock)
		"""
		pt = self._PowerThread(self)
		pt.start()
		

	def wasButtonPressed(self):
		"""
		Used in active mode: check this function to see if no one pressed
		power button
		"""
		return self.__buttonPressed

	def power_unlock(self):
		"""
		Unlocks the lock on power button
		"""
		lib.unlock_power(self.obj)

	def __del__(self):
		lib.free_object(self.obj)

########################################thread section################################
# A thread will be used when active mode is chosen so that main program would not stop
# just ignore following method and class as they should not be used directly in your
# program
	
	def _thread_run(self):
		result = 0
		if lib.active_lock_power(self.obj):
			self.__buttonPressed = True
			result = 1

		return result
	
	class _PowerThread(threading.Thread):

		def __init__(self,powerLock):
			threading.Thread.__init__(self)
			self.power = powerLock

		def run(self):
			self.power._thread_run()



if __name__== "__main__":
	pw = PowerLocker()
	pw.active_power_lock()
	time.sleep(5)
	print pw.wasButtonPressed()
	pw.power_unlock()
	
	




