<!DOCTYPE html><html><head><title>Readme</title></head><body>
<h1>Modify</h1>
<p>
A completely accessible Python program that can read mods from Sound RTS (sound Real Time strategy) game for the blind and allow you to view and change them

</p>
<h1>Status: Beta</h1>
<p>
This project can load mods, but there is no good way to do much of anything useful.
All it needs is a keyboard interface, to modify the parts of the mod that can't be modified now.
Currently you can only view units and change or view some basic attributes and sounds.

</p>
<h1>Modifying modify</h1>
<p>
You can of course change this program if you want to.
The modify.py file is the main program.
It requires sound_lib, wx, pygame and all the other modules in the same folder.
It also uses Python 3.7
The libs in the /libs folder work on 32 bit computers, but different libs might be needed for 64 bit computers.
The most important class is the data class.
Each instance either stores info on a single unit or upgrade, or a text file and all the objects in it, like rules.txt
rules is infact a global variable, of the data class.
style is pretty much the same thing, it's available globally.
Both of them have a children attribute, this is a list of data objects, each one a unit or something that came from the respective file.
units is a global list of data objects from rules.txt
each object has:
name: the internal name, not the tts name
tts-name: the name from tts.txt, style is used to find this
style: a data object that is this unit's data from style.txt
contents: a dictionary of properties for just this object. This is the dictionary that is modified when changing properties of a unit.
friendly_contents: A dictionary of all properties from this unit, but also any properties from inherited units. Preferably, show values from this dictionary to the user.


<br>
The modify.py is commented, so that should help.
Currently, the program can load up mods by it's self and generate mostly sound RTS loadable files with out any problems, though it doesn't respect the 'clear' line in a mod.
What needs to be done is allow the user to modify the mod.





</p>


</body></html>
