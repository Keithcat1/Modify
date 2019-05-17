#Defines lowercase constants for easier using of pygame.locals keys
import pygame.locals as loc
tmp=loc.__dict__
del loc
for i in tmp:
 if i[0]=="K":
  globals()[i]=tmp[i]
k_alt=K_LALT
k_backspace=K_BACKSPACE
k_tab=K_TAB
k_enter=K_RETURN
k_escape=K_ESCAPE
k_space=K_SPACE
k_exclaim=K_EXCLAIM
k_dollar=K_DOLLAR
k_quote=K_QUOTE
k_leftparen=K_LEFTPAREN
k_rightparen=K_RIGHTPAREN
k_plus=K_PLUS


alpha="abcdefghijklmnopqrstuvwxyz1234567890"
for i in alpha:
 globals()["k_{0}".format(i)]=tmp["K_{0}".format(str(i))]
k_up=K_UP
k_down=K_DOWN
k_left=K_LEFT
k_right=K_RIGHT
k_shift=K_LSHIFT
k_ctrl=K_LCTRL
k_period=K_PERIOD
k_backslash=K_BACKSLASH
k_space=K_SPACE


def get(key):
 k=key.split('_')[1]
 if k==' ': return K_SPACE
 if k=='.': return k_period
 if k=='\\': return K_BACKSLASH
 return globals()[key]

