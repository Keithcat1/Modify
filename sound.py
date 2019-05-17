# -*- coding: utf-8 -*-
#BGT-ish Sound_lib wrapper
#Original author: Carter Temm
#Edited by Yukio Nozawa <personal@nyanchangames.com>
#Modified by me, keithwipf1@gmail.com
import math, ctypes
import sound_lib
from sound_lib import output
from sound_lib import stream
o=output.Output()
class sound():
	def __init__(self, filename="", vol=0, playing=False, looping=False):
		self.handle=None
		self.freq=44100
		if len(filename)>0:
			self.load(filename)
			self.handle.looping=looping
		self.volume=vol
		self.looping=looping
		if playing==True:
			self.play(ignore_loop=False)

	def load(self,filename=""):
		if self.handle:
			self.close()
#end close previous
		self.handle =stream.FileStream(file=filename)
		self.freq=self.handle.get_frequency()

	def __del__(self):
		self.stop()
		self.close()

	def play(self, ignore_loop=True):
		if ignore_loop==True:
			self.handle.looping=False
		return self.handle.play()

	def play_wait(self):
		self.handle.looping=False
		return self.handle.play_blocking()

	def play_looped(self):
		self.handle.looping=True
		return self.handle.play()

	def stop(self):
		if self.handle and self.handle.is_playing:
			self.handle.stop()
			self.handle.set_position(0)

	def fadeout(self, fadetime, amount=0.05):
		"""The faded sound might be kept playing internally. Make sure that you call stop() before fading in or playing again. Fading will be performed by BASS's internal thread, so playing this instance after calling fadeout() may sound strangely."""
		if self.handle and self.handle.is_playing:
			self.handle.slide_attribute("volume",amount,fadetime)

	@property
	def volume(self):
		if not self.handle:
			return False
		return round(math.log10(self.handle.volume)*20)
	@volume.setter
	def volume(self,value):
		if not self.handle:
			return False
		self.handle.set_volume(10**(float(value)/20))

	@property
	def pitch(self):
		if not self.handle:
			return False
		return (self.handle.get_frequency()/self.freq)*100

	@pitch.setter
	def pitch(self, value):
		if not self.handle:
			return False
		self.handle.set_frequency((float(value)/100)*self.freq)

	@property
	def pan(self):
		if not self.handle:
			return False
		return self.handle.get_pan()*100

	@pan.setter
	def pan(self, value):
		if not self.handle:
			return False
		if value<-100 or value>100:
			raise ValueError("The pan value is not between -100 and 100")
		self.handle.set_pan(float(value)/100)

	@property
	def playing(self):
		if not self.handle:
			return False
		return self.handle.is_playing

	def close(self):
		if self.handle:
			self.handle.free()
			self.handle=None

	def seek(self, position):
		return self.handle.set_position(position)

	@property
	def position(self):
		return self.handle.get_position()/1000000

	@position.setter
	def position(self, val):
		self.handle.set_position(val)/1000000


def sound_from_bytes(bytes):
 """Takes some bytes and returns a sound() object that you can play, pan, ETC"""
 snd=sound()
 snd.__buffer=ctypes.create_string_buffer(bytes)
 addr=ctypes.addressof(snd.__buffer)
 h=stream.FileStream(mem=True, file=addr, length=len(snd.__buffer))
 snd.handle=h
 return snd