import os
import threading
import time
from olifantAudio import AudioPlayer 
from olifantException import OlifantException
from olifantDeviceLock import DeviceLocker
from olifantUSB import *


folder_ac = "/proc/acpi/ac_adapter" #alimentation cable
folder_batt = "/proc/acpi/battery" #battery
folder_lid = "/proc/acpi/button/lid/" #lid

audio_file = 'alarm.wav' #an audio file

class Olifant(threading.Thread):
	"""
	This class handles program logic
	"""

	#constants to select mode
	PASSWD_MODE = 0
	USB_MODE = 1
	STRONG_MODE = 2

	#configuration constants
	AC_ALARM = 0
	BATTERY_ALARM = 1
	LID_OPENED_ALARM = 2
	POWER_BUTTON_ALARM = 3
	

	#private section, just use methods to access to these
	__refresh_time_ms = 0.3 #waits for 300 ms each time before checking again system status
 
	__mode = None
	__passwd = None
	__usb_id = None #this an id for usb
	__alarm_on = False
	__wrong_tries = 0 #olifant will register number of wrong tries, so in main application you could handle this
	__current_volume = 0 #we save volume setting before starting so we can turn it back to normal on exit

	#system files section of private section
	__f_batt = None #battery
	__f_ac = None #AC cable
	__f_lid = None #lid

	
	__device_locker = None #locker manager
	__player = None #audio manager
	__pendrive_manager = None #usb manager

	__configuration = [False, False, False, False]  #configuration, each element of this arrays says if a
							#laptop function has to be checked.
							#Indexes correspond to function according to constants
							#(ie. AC_ALARM=0, so first element of array is to check AC 
							#cable)

	
	def __init__(self,mode=PASSWD_MODE,config=[AC_ALARM,BATTERY_ALARM,LID_OPENED_ALARM, POWER_BUTTON_ALARM]):
		"""
		Creates a new olifant object with selected mode (default: PASS_MODE)
		Please use Olifant constants to select it
 
		Modes:
		-PASSWD_MODE: a password will be used to lock/unlock
		-USB_MODE: in order to unlock an usb driver, with an unlock program on, will
		    have to be plugged in *NOT SUPPORTED YET*
		-STRONG_MODE: both an usb driver plugged and an unlock password will
		      be needed *NOT SUPPORTED YET*

		Throws an exception when:
		-Olifant is used with a non-notebook pc (no one would stole a desktop pc
			right? ;) )
		-Battery is not inserted (in this case thief would just remove cable in
			order to shut down your notebook and olifant with it, sad)
		-Cable is not plugged in (in this case thief just removes battery,
			another sad scenario)
		"""
		threading.Thread.__init__(self)

		if not self.__isLaptop():
			raise OlifantException('This pc is not a notebook')

		#init of system files descriptors (we'll use these to check for pc status')
		self.__initSystemFiles()

		if os.getuid() != 0:
			raise OlifantException('This program must be run with root privileges!')

		#setting configuration
		for i in config:
			self.__configuration[i] = True

		self.__mode = mode
		self.__player = AudioPlayer(audio_file) #player init
		self.__device_locker = DeviceLocker() #device locker init
		self.__pendrive_manager = PendriveManager() #pendrive init

		if not self.__checkLaptopStatus():
			raise OlifantException("Your initial setup does not match with entered configuration \
						(ie. you entered 'alarm with cable off' and your cable is already off)")
	
	def setRefreshTime(self,timeMS):
		"""
		Sets checking refresh time (default is each 300 ms)
		"""		
		if timeS > 0:
			self.__refresh_time_ms = timeMS/1000
		else:
			raise OlifantException('A non positive value for time was entered')	

	def lock(self,passwd=None,usbDrive=None):
		"""
		Starts olifant: from this moment on olifant will sound if:
		- Cable is plugged out
		- Battery is removed
		- Monitor is closed/opened 
		According to chosen mode a password has to be inserted (default: None)

		Throws exception if:
		- Cable is not plugged in
		- Battery is not inserted
		- Power lock fails (this most certainly because you're not executing as admin)
		- password is None if you selected PASSWD MODE
		- usbDrive is None if you selected USB MODE
		- both previous if you selected STRONG MODE
		"""		
		if not self.__checkLaptopStatus():
			raise OlifantException("Your initial setup does not match with entered configuration \
						(ie. you entered 'alarm with cable off' and your cable is already off)")
		
		if self.__mode != Olifant.USB_MODE and passwd == None:
			raise OlifantException("Password cannot be empty")
	
		if self.__mode != Olifant.PASSWD_MODE and usbDrive == None:
			raise OlifantException("You have to select an usb driver")

		
		self.__current_volume = self.__player.getCurrentVolume() # saving current volume value
									 # (olifant will set it to maximum
									 # in case of alarm)
	
		self.__device_locker.active_lock_devices() #will disable power button/keyboard/lid and check if power button is pressed
		self.__wrong_tries = 0 #reset of wrong unlock tries
		self.__passwd = passwd
		if usbDrive != None:
			self.__usb_id = usbDrive.ID 

		self.__alarm_on = True
				
		#start of checking loop (as thread)
		ot = self._OlifantThread(self)
		ot.start()

	
	def unlock(self,passwd=None):
		"""
		Stops olifant.
		An exception will be thrown:
		- if something goes wrong,for example if password is wrong
		- if olifant was not started before (are you dumb mate?:D)	
		"""
		#let's see if olifant was activated before
		if(not self.activated()):
			raise OlifantException('Olifant is not currently active!')

		#first we check for password (easier to check)
		if(self.__mode != Olifant.USB_MODE):	#in usb mode password is not used
			if(self.__passwd != passwd):
				self.__wrong_tries = self.__wrong_tries + 1
				raise OlifantException('Entered password is wrong!')

		#now for usb (if mode was PASSWD_MODE we have finished!)
		if(self.__mode != Olifant.PASSWD_MODE):
			if self.__pendrive_manager.getDeviceFromID(self.__usb_id) == None: #we cannot find usb device
				self.__wrong_tries = self.__wrong_tries + 1
				raise OlifantException('Usb device used for lock is not connected')
		
		#ok you're authorized!
		self.__device_locker.unlock_devices()
		self.__alarm_on = False #stops checking loop (and so the thread)
		self.__player.stop() #stops player if it is playing
		self.__player.setVolume(self.__current_volume) # we set back volume to old value

	def getPendriveList(self):
		"""
		Returns usb devices currently connected
		"""
		return self.__pendrive_manager.getPenList()

	def activated(self):
		"""
		Returns True if olifant is active
		"""
		return self.__alarm_on

	def get_failed_tries(self):
		"""
		Returns number of failed unlock tries
		"""
		return self.__wrong_tries

	#destructor
	def __del__(self):
		self.__closeSystemFiles()
	
	
	def _run_thread(self):
		"""
		It's the core method and the trick behind the magic: will periodically check battery and
		AC status, ringing if something goes wrong
		Note that you SHOULD NEVER USE this method, but simply call
		lock/unlock methods which will call and safe-stop it for you!
		"""
		while self.__alarm_on:
			time.sleep(self.__refresh_time_ms)
			if not self.__checkLaptopStatus():		
				self.__player.setMaximumVolume()				
				self.__emergency() #calls emergency (it doesnt stop if cable is re-plugged in or anything, we
						   #don't want to make thief think too much :D

	def __emergency(self):
		while self.__alarm_on:		#this condition will hold till unlock() method is successfully called
			print "ALARM!!BATTERY REMOVED OR CABLE UNPLUGGED!!!!"
			self.__player.play()

	class _OlifantThread(threading.Thread):
		"""
		A thread which will be used to make active wait so that
		olifant class does not block
		"""
		def __init__(self,olifant):
			threading.Thread.__init__(self)
			self.olifant = olifant

		def run(self):
			self.olifant._run_thread()

######################################## utilities ####################################################################

	def __isLaptop(self):
		return os.path.exists(folder_lid)  #a laptop has a lid, a desktop not...that's just some logic!

	#checks for battery inserted
	def __isBatteryInserted(self):
		#return True #TODO this is for debugging on my laptop :D
		result = False

		data_batt = self.__f_batt.read()
		self.__f_batt.seek(0) #rewinding
		state_batt = data_batt.splitlines()[0]
		if "yes" in state_batt:
			result = True
		
		return result
	
	#checks for AC cable plugged
	def __isCablePlugged(self):
		result = False

		data_ac = self.__f_ac.read()
		self.__f_ac.seek(0) #rewinding
		state_ac = data_ac.splitlines()[0]
		if "on-line" in state_ac:
			result = True

		return result
	
	#checks for closed lid
	def __isLidOpen(self):
		result = False

		data_lid = self.__f_lid.read()
		self.__f_lid.seek(0) #rewinding
		state_lid = data_lid.splitlines()[0]
		if "open" in state_lid:
			result = True

		return result

	def __checkLaptopStatus(self):
		"""
		This function returns True if everything is ok, False
		if some of the activation conditions are not met (ie. battery was plugged out)
		"""

		result = True
		
		if self.__configuration[self.AC_ALARM] == True:
			result = result and self.__isCablePlugged()

		if self.__configuration[self.BATTERY_ALARM] == True:
			result = result and self.__isBatteryInserted()

		if self.__configuration[self.LID_OPENED_ALARM] == True:
			result = result and self.__isLidOpen()

		if self.__configuration[self.POWER_BUTTON_ALARM] == True:
			result = result and not(self.__device_locker.wasButtonPressed())

		return result
	

	#opens system files
	def __initSystemFiles(self):
		#battery
		DEV_batt = os.listdir(folder_batt)

		batteryFound = False		#some ppl have more than one battery folder (dunno why)
		nFolder = len(DEV_batt)         #so we'll find first active one (if exists)
		i = 0
		while not batteryFound and i<nFolder:
			file_batt = os.path.join(folder_batt, DEV_batt[i], "state")
			self.__f_batt = open(file_batt, "r")
			if(self.__isBatteryInserted()):
				batteryFound = True
			else:
				i = i + 1
			
		#AC cable
		DEV_ac = os.listdir(folder_ac)[0]
		file_ac = os.path.join(folder_ac, DEV_ac, "state")
		self.__f_ac = open(file_ac, "r")

		#lid
		DEV_lid = os.listdir(folder_lid)[0]
		file_lid = os.path.join(folder_lid, DEV_lid, "state")
		self.__f_lid = open(file_lid, "r")

	#closes system files
	def __closeSystemFiles(self):
		if self.__f_batt != None:
			self.__f_batt.close()
		
		if self.__f_ac != None:
			self.__f_ac.close()

		if self.__f_lid != None:
			self.__f_lid.close()



#let's try it!
if __name__ == "__main__":
	time_to_sleep = 10
	try:
		ol = Olifant(Olifant.PASSWD_MODE, [Olifant.AC_ALARM])
		#devices = ol.getPendriveList()
		ol.lock("phate")#usbDrive=devices[0]) #locking
		print 'Olifant started, in next '+str(time_to_sleep)+' seconds try removing battery or AC cable or pressing power button (LOL)'
		time.sleep(time_to_sleep) #sleeps 10 seconds, do your experiments in this time or substitute with a while True loop
		ol.unlock("phate") #unlocking
		print "Unlocked!"
	except OlifantException as ex:
		print ex.getMessage()


