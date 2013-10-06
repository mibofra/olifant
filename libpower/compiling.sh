g++ -c -fPIC DeviceLocker.cpp -o devicelock.o
g++ -shared -Wl,-soname,libdevicelock.so -o libdevicelock.so devicelock.o
rm devicelock.o
mv libdevicelock.so ..
