#include <fcntl.h>
#include <unistd.h>
#include <iostream>
#include <cstdlib>
#include <cstdio>
#include <errno.h>
#include <linux/input.h>
#include <dirent.h>
#include <string.h>

using namespace std;

const string ROOT_DEV = "/dev/input";
const int DEV_TO_LOCK = 3;

const string POWER_NAME = "Power";
const string POWER_PHYS = "PNP0C0C";

const string KEYBOARD_NAME = "keyboard";
const string KEYBOARD_PHYS = "isa0060";

const string LID_NAME = "Lid";
const string LID_PHYS = "PNP0C0D";

class DeviceLocker{
	private:
	
	int pow_dev;
	int key_dev;
	int lid_dev;

	bool active; //used for active wait
	
	bool isThisDevice(const int dev,const string devName,const string devPhys){
		char name[256] = "Unknown";
		char phys[256] = "Unknown";

		int res1 = 0;
		int res2 = 0;
		bool result = false;

		res1 = ioctl(dev, EVIOCGNAME(sizeof(name)), name); //getting name of peripheral 
		if ( res1 < 0)
			cerr << "Failed getting name of " << devName << endl;

		res2 = ioctl(dev, EVIOCGPHYS(sizeof(phys)), phys);


		if (res1>=0){
			if( string(name).find(devName) != string::npos ) 
					result = true;
			else if (res2>=0)
				if( string(phys).find(devPhys) != string::npos)
					result = true;

		}

		return result;
	}

	public:

	DeviceLocker(){
		pow_dev = -1;
		key_dev = -1;
		lid_dev = -1;
		active = false;
	}

	
	bool lockEmAll(){
		int fdev = -1;
		int res = 0;
		int size = sizeof(struct input_event);
		struct dirent* de = NULL;
  		DIR* d = NULL;

		//opening directory
		d=opendir(ROOT_DEV.c_str());
 	 	if(d == NULL){
    			cerr << "Couldn't open " << ROOT_DEV << "directory" << endl;
    			return(2);
  		}

		while(de = readdir(d)){
			if(string(de->d_name).find("event") != string::npos){ //we're interested in events
				string path = ROOT_DEV+"/"+de->d_name;
				fdev = open(path.c_str(), O_RDONLY);

				if(isThisDevice(fdev,POWER_NAME,POWER_PHYS)){
					pow_dev = fdev;
					res = ioctl(pow_dev, EVIOCGRAB, 1);
					if(res < 0)
						cerr << "Failed acquiring exclusive lock on power\n";
					
					fdev = -1;
					
				}else if(isThisDevice(fdev,KEYBOARD_NAME,KEYBOARD_PHYS)){
					key_dev = fdev;
					res = ioctl(key_dev, EVIOCGRAB, 1);
					if(res < 0)
						printf("errno = %d, '%s'", errno, strerror(errno));
						perror("\nThe following error occurred");
						cerr << "\nFailed acquiring exclusive lock on keyboard\n";
					
					fdev = -1;
					
				}else if(isThisDevice(fdev,LID_NAME,LID_PHYS)){
					lid_dev = fdev;
					res = ioctl(lid_dev, EVIOCGRAB, 1);
					if(res < 0)
						cerr << "Failed acquiring exclusive lock on lid\n";
					
					fdev = -1;
				}else
					close(fdev);
			}
		}

		
		if(pow_dev == -1)
			cerr << "Couldn't find power device\n";

		if(key_dev == -1)
			cerr << "Couldn't find keyboard device\n";

		if(lid_dev == -1)
			cerr << "Couldn't find lid device\n";

		

		return ( (pow_dev != -1) && (key_dev != -1) && (lid_dev != -1) );

	}


	bool activeLockEmAll(){
		struct input_event ev[64];
		if(lockEmAll()){
			active = true; //active mode
			int result = 0;
			fd_set set;
       			struct timeval timeout;
			FD_ZERO (&set);
       			FD_SET (pow_dev, &set);

			timeout.tv_sec = 0; 
       			timeout.tv_usec = 500; //timeout each 500 usecond

			while(active && (result == 0)){
				result = select(FD_SETSIZE,&set,NULL,NULL,&timeout);
				FD_SET (pow_dev, &set);
			}
			return true;
		}else
			return false;		
	}

	void unlockEmAll(){
		active = false;
		if(pow_dev != -1){
			close(pow_dev);
			pow_dev = -1;
		}

		if(key_dev != -1){
			close(key_dev);
			key_dev = -1;
		}

		if(lid_dev != -1){
			close(lid_dev);
			lid_dev = -1;
		}
	}

	~DeviceLocker(){
		unlockEmAll();
	}

};

extern "C" {
	DeviceLocker* DeviceLocker_new(){ return new DeviceLocker(); }
	bool lock_em_all(DeviceLocker* dl){ return dl->lockEmAll(); }
	bool active_lock_em_all(DeviceLocker* dl){ return dl->activeLockEmAll(); }
	void unlock_em_all(DeviceLocker* dl){ dl->unlockEmAll(); }
	void free_object(DeviceLocker* dl) { delete dl; }
}


//An example
int main(int arcg,char* argv[]){
	DeviceLocker dl = DeviceLocker();
	dl.activeLockEmAll();
	sleep(10);
	dl.unlockEmAll();
}

