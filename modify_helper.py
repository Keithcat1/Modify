#Contains extras for modify.py
a=('worker', 'soldier1', 'soldier2', 'soldier3', 'soldier4', 'soldier5', 'soldier6', 'soldier7') # Constants for the keyboard property in style
b=('d', 'f', 'g', 'h', 'j', 'k', 'l', ';')
c=dict(zip(a,b))
del a,b
from tolk import *

def get_val(valname, unit): # Speaks a unit's value like damage, or 0 if it's not defined.
 return say(str(unit.friendly_contents.get(valname, 0))+' '+valname)

