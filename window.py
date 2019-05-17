# -*- coding: utf-8 -*-
#Basic window and timer handling
#Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
#Modified by me, keithwipf1@gmail.com

import easykeys, tolk
from copy import copy
import pygame
from pygame.locals import *
#from dialog import *
class singletonWindow():
	"""Just a pygame window wrapper. As the name implies, you mustn't create multiple singletonWindow's in your game. """
	shown=False
	timers=[]
	def __init__(self):
		self.checked_keys=[0]*355
		self.checked_keys=[int(0) for i in self.checked_keys]
#I want to avoid doing initialization at constructor as much as possible, just my liking
	def __del__(self):
		pygame.quit()

	def new_timer(self):
		self.timers.append(wintimer())
		return self.timers[-1]

	def initialize(self,ttl,x=640,y=480):
		"""Initializes the game window. Returns True on success or False for failure. """
		pygame.init()
		self.clock=pygame.time.Clock()
		self.screen = pygame.display.set_mode((x, y))
		pygame.display.set_caption(ttl)
		self.keys=[0]*355
		self.previousKeys=[0]*355
		self.shown=True
		return True

	def update(self, time=60):
		"""A function that must be called once per frame. Calling this function will keep the 60fps speed. Returns True while the game is running and returns False when the process should exit. When returning false, you can immediately exit the game without caring about pygame termination because it's done automatically at the destructor. """
		self.clock.tick(time)
		try:
			self.screen.fill((255,63,10,))
			pygame.display.update()
		except pygame.error:
			return False
		self.previousKeys=copy(self.keys)
		self.keys=pygame.key.get_pressed()
		if self.keys[K_LALT] and self.keys[K_F4]: return False
		for event in pygame.event.get():
			if event.type == QUIT: return False
		for i in range(len(self.timers)):
			self.timers[i].update(time)

		#end event
	#end frameUpdate

	def key_pressed(self, key):
		if self.keys[key] and self.checked_keys[key]:
			return False
		if not self.keys[key] and self.checked_keys[key]:
			self.checked_keys[key]=0
			return False
		if self.keys[key] and not self.checked_keys[key]:
			self.checked_keys[key]=1
			return True

	def pressed(self,key):
		"""Retrieves if the specified key has changed to "pressed" from "not pressed" at the last frame. Doesn't cause key repeats.  """
		return self.keys[key] and not self.previousKeys[key]

	def pressing(self,key):
		"""Retrieves if the specified key is being pressed. Key repeats at 60rp/sec. """
		return self.keys[key]

	def wait(self,msec=5):
		"""waits for a specified period of milliseconds while keeping the window looping. Same as frameUpdate(), you should exit your game when this function returned false. """
		t=timer()
		while t.elapsed<msec:
			if self.update() is False: return False
		#end loop
		return True
	#end wait

	def get_input(self, prompt="Type something in", acceptkeys=r'abcdefghijklmnopqrstuvwxyz123456789\ ', starting_text=''):
		res=starting_text
		tolk.say(prompt)
		while self.wait(25) is True:
			for i in acceptkeys:
				if self.key_pressed(easykeys.k_enter): return res
				if self.key_pressed(easykeys.k_backspace) and len(res)>0:
					tolk.say("%s deleted"%res[-1])
					res=res[0:-1]
				if self.key_pressed(easykeys.k_escape): return None
				curkey=easykeys.get("k_{0}".format(i))
				if self.key_pressed(curkey):
					res+=i
					tolk.say(i)
		return res

#end class singletonWindow

class timer:
	def __init__(self):
		self.restart()

	def restart(self):
		self.startTick=pygame.time.get_ticks()

	@property
	def elapsed(self):
		return pygame.time.get_ticks()-self.startTick

#end class timer



class wintimer:
	def __init__(self):
		self.paused=False
		self.elapsed=0


	def pause(self):
		self.paused=True
	def resume(self):
		self.paused=False
	def update(self, amount=5):
		if self.paused==False: self.elapsed+=amount

