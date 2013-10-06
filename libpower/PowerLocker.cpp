#include <fcntl.h>
#include <iostream>
#include <cstdlib>
#include <linux/input.h>
#include <dirent.h>
#include <string.h>

//#define ROOT_DEV "/dev/input"

using namespace std;

const string ROOT_DEV = "/dev/input";

class PowerLocker{
	private:
	
	int fdev;
	int keydev;

	bool active; //used for active wait
	
	bool isPowerButton(string path){
		int fevdev = -1;
		char name[256] = "Unknown";
		int res = 0;
		bool result = false;

		fevdev = open(path.c_str(), O_RDONLY);
		if (fevdev == -1) 
			cerr << "failed opening " << path << endl;
		else{
			res = ioctl(fevdev, EVIOCGNAME(sizeof(name)), name); //getting name of peripheral
			if ( res < 0)
				cerr << "Failed getting name of " << path << endl;
			else
				if(string(name).find("Power") != string::npos) //let's see if it's a power button..
					result = true;
		
			close(fevdev);
		}

		return result;
	}

	bool isKeyboardDevice(string path){
		int fevdev = -1;
		char name[256] = "Unknown";
		int res = 0;
		bool result = false;

		fevdev = open(path.c_str(), O_RDONLY);
		if (fevdev == -1) 
			cerr << "failed opening " << path << endl;
		else{
			res = ioctl(fevdev, EVIOCGNAME(sizeof(name)), name); //getting name of peripheral
			if ( res < 0)
				cerr << "Failed getting name of " << path << endl;
			else
				if(string(name).find("keyboard") != string::npos) //let's see if it's a power button..
					result = true;
		
			close(fevdev);
		}

		return result;
	}

	bool findPowerDevice(char* devPath){
    		int size = sizeof(struct input_event);
		bool found = false;
		struct dirent* de = NULL;
  		DIR* d = NULL;

		string path = ROOT_DEV + "/event1"; //usually power is event1...let's hope we're lucky!
		if(isPowerButton(path)){
			strcpy(devPath,path.c_str()); //yay lucky!! :D
			found = true; 

		}else{			//no luck...we'll have to check each file in /dev/input!
		
			d=opendir(ROOT_DEV.c_str());
			if(d == NULL){
    				cerr << "Couldn't open directory";
				return false;	
  			}

			// Loop while not NULL (end of files) or found
  			while((!found) && (de=readdir(d)))
    				if(de->d_type != DT_DIR){			//if isn't a directory
					path = ROOT_DEV+"/"+de->d_name;		//make path
			
					if(isPowerButton(path)){		//check for power button
						strcpy(devPath,path.c_str()); 	//found it!
						found = true;
					}
				}

			closedir(d);
		}

		return found;
	}

	bool findKeyboardDevice(char* devPath){
    		int size = sizeof(struct input_event);
		bool found = false;
		struct dirent* de = NULL;
  		DIR* d = NULL;

		string path = ROOT_DEV + "/event2"; //usually keyboard is event1...let's hope we're lucky!
		if(isKeyboardDevice(path)){
			strcpy(devPath,path.c_str()); //yay lucky!! :D
			found = true; 

		}else{			//no luck...we'll have to check each file in /dev/input!
		
			d=opendir(ROOT_DEV.c_str());
			if(d == NULL){
    				cerr << "Couldn't open directory";
				return false;	
  			}

			// Loop while not NULL (end of files) or found
  			while((!found) && (de=readdir(d)))
    				if(de->d_type != DT_DIR){			//if isn't a directory
					path = ROOT_DEV+"/"+de->d_name;		//make path
			
					if(isPowerButton(path)){		//check for power button
						strcpy(devPath,path.c_str()); 	//found it!
						found = true;
					}
				}

			closedir(d);
		}

		return found;
	}

	public:

	PowerLocker(){
		fdev = -1;
		active = false;
	}

	bool lock(){
		bool locked = false;
		int result1 = 0;
		int result2 = 0;
		char dev_path[256];
		char key_path[256];

		if(findPowerDevice(dev_path) and findKeyboardDevice(key_path)){
			fdev = open(dev_path, O_RDONLY);
			keydev = open(key_path, O_RDONLY);

			result1 = ioctl(fdev, EVIOCGRAB, 1);
			result2 = ioctl(keydev, EVIOCGRAB, 1);
	
			if( (result1 < 0) or (result2 < 0)){
				cerr << "Could not lock power button!!" << endl;
				unlock();
			}else
				locked = true;
		}else
			cerr << "Could not find a power button!!" << endl;
		
		return locked;
	}

	bool active_lock(){
		struct input_event ev[64];
		if(lock()){

			active = true; //active mode
			int result = 0;
			fd_set set;
       			struct timeval timeout;
			FD_ZERO (&set);
       			FD_SET (fdev, &set);

			timeout.tv_sec = 0; 
       			timeout.tv_usec = 500; //timeout each 500 usecond

			while(active && (result == 0)){
				result = select(FD_SETSIZE,&set,NULL,NULL,&timeout);
				FD_SET (fdev, &set);
			}
			return true;
		}else
			return false;		
	}

	void unlock(){
		active = false;
		close(fdev); //we just close fdev
		close(keydev);
	}

};

extern "C" {
	PowerLocker* PowerLocker_new(){ return new PowerLocker(); }
	bool lock_power(PowerLocker* pl){ return pl->lock(); }
	bool active_lock_power(PowerLocker* pl){ return pl->active_lock(); }
	void unlock_power(PowerLocker* pl){ pl->unlock(); }
	void free_object(PowerLocker* pl) { delete pl; }
}

/*
//An example
int main(int arcg,char* argv[]){
	PowerLocker pl = PowerLocker();
	pl.active_lock();
	pl.unlock();
}*/

