"""
This module handles audio playing with AudioPlayer class (requires pyaudio, you can install it from synaptic)
"""

import pyaudio
import wave
import sys
import alsaaudio

class AudioPlayer:
	"""
	A simple audio player
	"""

	chunk = 1024 #default chunk size

	__wf = None
	__stream = None
	__p = None
	__mixer = None

	__audio_on = False
	
	
	def __init__(self,filename):
		try:
			self.__wf = wave.open(filename,'rb')
		except IOError:
			raise OlifantException('Sound file does not exists!')

		self.__p = pyaudio.PyAudio()
		self.__stream = self.__p.open(format=self.__p.get_format_from_width(self.__wf.getsampwidth()),\
			channels=self.__wf.getnchannels(),rate=self.__wf.getframerate(),output=True)

		self.__mixer = alsaaudio.Mixer()


	def play(self):
		"""
		Plays audio stream loaded througth
		constructor
		"""
		self.__audio_on = True

		data=self.__wf.readframes(self.chunk)
		while self.__audio_on and data != '':
			self.__stream.write(data)
			data = self.__wf.readframes(self.chunk)
		
		self.__wf.rewind()

	def stop(self):
		"""
		If playing stops audip
		"""
		self.__audio_on = False

	def setMaximumVolume(self):
		"""
		Sets volume to maximum and umutes too if
		it's mute (*not working if unmute is set
		by keyboard..T_T*)
		"""
		self.__mixer.setmute(0)
		self.__mixer.setvolume(100)

	def getCurrentVolume(self):
		vol = self.__mixer.getvolume()
		return vol[0]

	def setVolume(self,vol):
		self.__mixer.setvolume(vol)

	def __del__(self):
		self.__wf.close()
		self.__stream.close()
		self.__p.terminate()

#Used this way:

if __name__ == "__main__":
	au = AudioPlayer('alarm.wav')
	print au.getCurrentVolume()
	au.setMaximumVolume()
	au.play()


