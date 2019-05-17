#Menu class made by me, using the singleton window class
import window, easykeys as keys, tolk
class MenuError(Exception):
 pass

class menu:
 def __init__(self, items, win, first_letter=True):
  self.items=items
  self.window=win
  if win.shown==False:
   raise MenuError("You must show a window if you want to get any keyboard input. The window you passed expects to be shown.")
  self.keys='abcdefghijklmnopqrstuvwxyz'
  self.first_letter=first_letter

 def __getitem__(self, ind):
  ind+=1
  if ind>=len(self.items):
   ind=0
  elif ind<0:
   ind=len(self.items)-1
  return self.items[ind]

 def run(self, start=0, prompt="Please choose an option", callback=None):
  tolk.say(prompt)
  while True:
   self.window.wait(20)
   position=start
   if self.window.key_pressed(keys.k_down):
    position+=1
   if self.window.key_pressed(keys.k_up):
    position-=1
   if position<0:
    position=len(self.items)-1
   elif position>=len(self.items):
    position=0
   if self.window.key_pressed(keys.k_escape):
    return -1
   if self.window.key_pressed(keys.k_enter):
    return self.items[position]
   if callable(callback)==True and callback((position, self[position]))==False: return self[position]
   if self.first_letter==True:
    for i in self.keys:
     if self.window.key_pressed(keys.get('k_'+i)):
      if self.window.pressing(keys.k_shift): i=i.upper()
      list=self.items[position+1:]
      list+=self.items[:position+1]
      for j in list:
       if j[0]==i:
        position=self.items.index(j)
        break
   if position!=start:
    tolk.say(self.items[position])
    start=position




