from usb import core
from usb import util

class USBDevice:
	"""
	A simple container for easy access to name and
	ID of a device
	"""
	Device = None
	Name = None
	ID = None

	def __init__(self,device,name,ID):
		self.Device = device
		self.Name = name
		self.ID = ID

class PendriveManager:
	"""
	This class handles pendrive handling, you can
	get a list of current pendrives and an id
	for each of them
	"""
	
	__pen_list = None #an USBDevice objects list
	
	def __init__(self):
		self.update()

	def update(self):
		"""
		updates pendrive list if, for example
		a new pendrive is entered
		"""	
		self.__pen_list = []
		devices = core.find(find_all=True, bDeviceClass=0)	
		for device in devices:
			cfg = device.get_active_configuration()
			interface_class = cfg[(0,0)].bInterfaceClass
        		if interface_class == 8:
				name = self.__getName(device)
				ID = self.__getDeviceID(device)
				usbDevice = USBDevice(device,name,ID)
				self.__pen_list.append(usbDevice)

	def getPenList(self):
		return self.__pen_list

	def __getName(self,pen):
		"""
		Get pen's name for user displaying
		"""
		name = (util.get_string(dev=pen,length=20,index=1))+" "+(util.get_string(dev=pen,length=20,index=2))
		return name

	def __getDeviceID(self,pen):
		"""
		Gets an (almost) unique id for this pen
		"""
		penID = str(pen.idVendor)+"/"+str(pen.idProduct)
		return penID

	def getDeviceFromID(self,penID):
		"""
		Returns device if a pen with entered ID is present,
		None otherwise
		"""
		device = None
		self.update()

		found = False
		i = 0
		while (not found) and (i < len(self.__pen_list)):
			if self.__pen_list[i].ID == penID:
				device = self.__pen_list[i]
				found = True
			else:
				i = i + 1

		return device


if __name__ == "__main__":
	import time

	manager = PendriveManager()
	ll = manager.getPenList()
	for l in ll:
		print "Device name: "+ l.Name
		print "Device ID: "+l.ID

	print "Remove or leave attached your first device"
	time.sleep(10)
	if manager.getDeviceFromID(ll[0].ID) != None:
		print "Device is still connected"
	else:
		print "Device removed"
