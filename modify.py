"""Sound RTS Modify, mod modafier.
Built by keithwipf1@gmail.com
"""
#Most interactive code starts at line 246


import menu, window, sound, tolk, time, traceback as tb, sys
#Exception handler that lets you view the exception.
def myexc(type, exc, trace):
 data=''.join(tb.format_exception(type, exc, trace))
 say("This error occured: "+data+": Press escape or alt + F4 to exit or press e to rehear the error")
 pygame.display.set_caption("Modify - "+type.__name__+": "+str(exc))
 while win.wait(30):
  if win.key_pressed(k_e): say(data)
  if win.key_pressed(k_escape): sys.exit()

 sys.exit()
sys.excepthook=myexc

from modify_helper import *
from tolk import *
import pygame, wx, pathlib, os.path, time, sys, random
rules=object()
win=window.singletonWindow()
win.initialize("Modafy")
time.sleep(1)

def get_unit(name, source=rules, use_tts=True): # This returns an object with internal name that matches name. Source is rules by default, though you can set it to style. Though all rule units will already have a style attribute pointing to there style contents.
 if use_tts==False:
  c=source.children
  for i in c:
   if name==i.name: return i
 else: return source.children[source.children.index(name)]

def set_up_inherit(obj, source=rules): # Used for the 'is_a' property which is common. This function stores all the inherited attributes in the friendly_contents attribute, which is used for playing back sounds in the unit manager.
 if 'is_a' not in obj.contents:
  obj.friendly_contents=obj.contents
  return obj
 badlist=['building', 'unit', 'walking_unit', 'footman', 'peasant', 'archer', 'thing', 'guardtower', 'zombie']
 unit=obj
 lst=[unit]
 while 'is_a' in unit.contents:
  nxt=unit.contents['is_a']
  if len(nxt)<1: return unit
  stopit=False
  for i in badlist:
   if i==nxt: stopit=True
  if stopit==True: break
  unit=get_unit(nxt, source, False)
  lst.append(unit)
 lst.reverse()
 for i in lst: print("Got", i.name)
 for i in lst:
  obj.friendly_contents.update(i.contents)
 return obj

def random_sound(name, unit): # Plays a sound, name is the name of the attribute that has the sound.
 global sounds
 if not name in unit.style.friendly_contents or 'loop' in unit.style.friendly_contents[name]:
  say(name+"Not in "+unit.tts_name)
  return False
 data=unit.style.friendly_contents[name].split()
 if data[0]=='repeat': data=data[2:]
 fle=mod+'/ui/sounds/'+random.choice(data)+'.ogg'
 testpath=pathlib.Path(fle)
 if not testpath.exists():
  say("Error! File not found. This preticular sound could be in another sounds folder")
  return False
 sounds=[sound.sound(playing=True, filename=fle)]
 return None

app=wx.App()
from easykeys import *

def dumby(x):
 return x

def set_sound(property, unit): # Tries to allow the user to set the sound of a units action like moving, but only seems to work with ogg files.
 soundfile=wx.FileSelector("Select an ogg file for the "+property+" of "+unit.tts_name+"", '', '', '.ogg')
 if not soundfile.endswith('.ogg'):
  say("Must be a .ogg file")
  return False
 p=pathlib.Path(soundfile)
 pbytes=p.read_bytes()
 p=list(pathlib.path(mod+'/ui/sounds').iterdir())
 if not p.exists(): return False
 p=[os.path.join(i).split(".og")[0] for i in p]
 print(p)
 intp=sorted([int(i) for i in p])
 largest_sound=intp[-1]+1
 p=pathlib.Path(mod+'/ui/sounds/'+str(largest_sound)+'.ogg')
 p.write_bytes(pbytes)
 u.style.contents[property]+=largest_tts
 return True

def set_val(name, unit, is_number=True, set_it=True): # Uses singletonWindow.get_input method to get the value of the property.
 keys='abcdefghijklmnopqrstuvwxyz123456789' # List of keys that will be accepted by the function if the user presses them.
 if is_number==True: keys='123456789.' # is_number is true if this is a numerical property like damage.
 num=win.get_input("Enter the "+name+"", keys)
 if not num=='':
  if set_it==False: # set_it is weather or not to set it if it's false, just return the result.
   return num
  unit.contents[name]=num
  say(""+name+" set")
  return num
 else:
  say("You must enter something. No changes were made")
  return ''

def unit_manager(u):
#Main unit manager, that accepts input from the user.
#keys without the shift key allow you to view and listen to properties or sounds.
#Holding the shift key with a key that says a property will allow you to change most properties.
#1-7: properties
#Q-P: sounds
 pygame.display.set_caption(u.tts_name)
 c, stc, fc=u.contents, u.style.contents, u.friendly_contents
 while win.wait(20):
  if win.pressing(k_ctrl) and win.key_pressed(k_n):
   # This allows to create a new unit, but this code should probably be moved to the unit list menu.
   temp=data()
   internal_name=win.get_input("Enter the new unit's name")
   if len(internal_name)==0 or internal_name==None:
    say("Canceled")
    continue
   external_name=win.get_input("Enter the units name that will be shown to the player. Just press enter to use the internal name")
   if len(external_name)==0: external_name=internal_name
   temp.name=internal_name
   temp.tts_name=external_name
   largest_tts=list(tts.contents.keys())
   largest_tts=[int(i) for i in largest_tts]
   largest_tts=sorted(largest_tts)[-1]
   largest_tts+=1
   tts.contents[str(largest_tts)]=external_name
   m=menu.menu(sorted([str(i.tts_name) for i in units]), win)
   res=m.run(prompt='Select a unit that can be used to take initial properties from or just press escape')
   temp.style=data()
   if res!=-1:
    tempunit=rules.children[rules.children.index(res)]
    temp.style.contents['title']=str(largest_tts)
    temp.style.name=internal_name
    temp.style.contents['is_a']=tempunit.name
    temp.contents['is_a']=tempunit.name
    temp=set_up_inherit(temp, rules)
    temp.style=set_up_inherit(temp.style, style)
    rules.children.append(temp)
    style.children.append(temp.style)
    units.append(temp)
    say("Done, made "+temp.tts_name+" as "+temp.name)
    unit_manager(temp) # View the new unit.
    return
  if win.pressing(k_shift):
   if win.key_pressed(k_1): set_val('hp_max', u)
   if win.key_pressed(k_2): set_val('damage', u)
   if win.key_pressed(k_3): set_val('armor', u)
   if win.key_pressed(k_4): set_val('speed', u)
   if win.key_pressed(k_5): set_val('range', u)
   if win.key_pressed(k_6): set_val('cooldown', u)
   if win.key_pressed(k_7): set_val('can_use', u, False)
   if win.key_pressed(k_w): set_sound("launch_attack", u)
   if win.key_pressed(k_e): set_sound("attack_hit", u)
   if win.key_pressed(k_r): set_sound("move", u)
   if win.key_pressed(k_y): set_sound("death", u)

  if win.key_pressed(k_q) and 'noise' in stc and 'repeat' not in stc['noise']: sounds=[sound.sound(playing=True, filename=mod+'/ui/sounds/'+stc['noise'][5:].split()[0]+'.ogg')] # Different from the other sounds because noise can be either loop or repeat
  if win.key_pressed(k_w): random_sound("launch_attack", u)
  if win.key_pressed(k_e): random_sound("attack_hit", u)
  if win.key_pressed(k_r): random_sound("move", u)
  if win.key_pressed(k_t): random_sound('noise', u)
  if win.key_pressed(k_y): random_sound("death", u)
  if win.key_pressed(K_F1): say(u.name) # Speaks the internal not tts name

  if win.key_pressed(k_1): get_val('hp_max', u)
  if win.key_pressed(k_2): get_val('damage', u)
  if win.key_pressed(k_3): get_val('armor', u)
  if win.key_pressed(k_4): get_val('speed', u)
  if win.key_pressed(k_5): get_val('range', u)
  if win.key_pressed(k_6): get_val('cooldown', u)
  if win.key_pressed(k_7) and 'can_use' in c: tolk.say(c['can_use'].replace(' ', ', ').replace('a_', 'ability_'))
  if win.key_pressed(k_escape): return

sounds=[] # Global sounds array to stop sounds going out of focus and dying.
class data:
 """Main class for storing units and Sound RTS objects in memory
Functions:
output: Returns data that's readable by Sound RTS and represents the current state of the object.
Calling this on rules will print out the data of rules.txt
Calling this on style will print out the data of style.txt
"""


 def __setitem__(self, item, value):
  self.contents[item]=value

 def __eq__(self, other):
  if type(other).__name__=='str' and hasattr(self, 'tts_name') and other==self.tts_name: return True
  return False

 def __getitem__(self, item):
  return self.children[item]

 def __init__(self, file=None, name='', inherit=True):
  self.name=name
  self.contents, self.style, self.friendly_contents={}, object(), {}
  self.children=[]
  if file:
   position=0
   stuff=file.readlines()
   places={}
   for i in range(len(stuff)):
    if stuff[i].startswith('def '): places[i]=stuff[i]
   for position in places.keys():
    name=stuff[position].split(' ', 2)[-1]
    values=[]
    for j in range(position, len(stuff)-1):
     line=stuff[j]
     if line=='def '+name: continue
     if line.startswith('def '):
      break
     if line.startswith(';'): continue
     values.append(line)
    temp=data()
    name=name.rstrip('\n')
    temp.name=name
    for i in values:
     if i==None or len(i)<2: continue
     if i[-1]==' ':
      temp.contents[i.strip()]=' '

      continue
     atrname=i.split(' ')[0]
     atrvalue=i.split(' ', 1)[-1]
     atrvalue=atrvalue.split(';')[0].strip()
     temp.contents[atrname]=atrvalue
    self.children.append(temp)
  if inherit==True:
   for i in self.children: i=set_up_inherit(i, self)

 def output(self):
  data=''
  for i in self.children:
   data+='\ndef '+i.name+'\n'
   for j in i.contents.keys():
    data+=j+' '+i.contents[j]+'\n'
  for k in self.contents.keys():
   data+=k+' '+self.contents[k]+'\n'
  return data

mod=win.get_input("Tell me the name of the folder where you're mod is stored.")
if mod==None or len(mod)==0:
 say("Fine then")
 pygame.display.quit()
 time.sleep(1)
 sys.exit()
say("Loading tts")
tts=data()
f=open(mod+'/ui/tts.txt')
stuff=f.readlines()
f.close()
tts.name='file tts'
for i in stuff:
 if len(i)<2 or i[0]==';': continue
 num=i.split()[0]
 val=i.split()[1:]
 val=' '.join(val)
 tts.contents[num]=val

def is_unit(obj):
 '''Filter function'''
 try:
  cl=obj.friendly_contents['class']
 except Exception as e:
  return False
 if cl=='soldier' or cl=='building' or cl=='worker': return True
 else: return False

def is_upgrade(obj):
 if 'class' in obj.contents and obj.contents['class']=='upgrade': return True
 return False
say("Loading style")
style=data(open(mod+'\\ui\\style.txt', 'r'), name='file_style', inherit=False)


say("Loading rules")
rules=data(open(mod+'\\rules.txt', 'r'))
say("Checking units")
units=list(filter(is_unit, rules.children))
#Units is a list of all buildings, soldiers, peasants and other such units.
upgrades=list(filter(is_upgrade, rules.children))

for i in rules.children:
 for j in style:
  if j.name==i.name:
   i.style=j
   i.style=set_up_inherit(i.style, style)
   try: i.tts_name=tts.contents[i.style.contents['title']]
   except:
    i.tts_name=i.name
units=[dumby(i) for i in units if hasattr(i, 'tts_name')]
say("Loaded")
def main_menu():
 m=menu.menu(['Manage units', 'exit'], win)
 res=m.run()
 if res=='Manage units':
  m=menu.menu(sorted([str(i.tts_name) for i in units]), win)
  res=m.run(prompt='Select a unit')
  unit_manager(rules.children[rules.children.index(res)])
  pygame.display.set_caption('Modify')
  main_menu()
main_menu()
#Don't write to the same style for now, because I don't completely trust my nice mod with this program :D
f=open(mod+'/generated_style.txt', "w")
f.write(style.output())
f.close()
f=open(mod+'/generated_rules.txt', "w")
f.write(rules.output())
f.close()
f=open(mod+'/ui/tts.txt', "w")
f.write(tts.output())
f.close()


#End program