from PIL import Image
from PIL import ImageGrab
from strongholdCalculations import *
from debugReadingFunctions import *
import keyboard
import time

hudSize = int(input("What GUI Scale are you using? Needed to read debug screen. 1/2/3/4\n"))
monitorSize = int(input("What monitor size are you using? 1 = 1920x1080"))

hotkeyinput = input("You will use a hotkey to tell the program when to acknowledge\
the debug screen. The default key is F9. Type a new hotkey here optionally, press\
 ENTER to use default.\n")

imageGrabMode = int(input("How would you like the debug screen to be read? If you are\
using two monitors, then a screenshot may not work, so getting an image from the\
clipboard with snip&sketch may be necessary. 0 = Take Screenshot, 1 = Use Clipboard"))

if hotkeyinput == '':
    hotkey = 'F9'
else:
    hotkey = hotkeyinput
    
print("Waiting for hotkey to acknowledge debug screen...")
keyboard.wait(hotkey)
if imageGrabMode:
    firstpoint = ImageGrab.grabclipboard()
else:
    firstpoint = ImageGrab.grab()
firstpointscaled = scaleDebugScreen(firstpoint, hudSize, monitorSize)
firstpointvalues = readProcessedScreen(firstpointscaled);
time.sleep(1)

print("Acknowledged first point... go to second one!")
keyboard.wait(hotkey)
if imageGrabMode:
    secondpoint = ImageGrab.grabclipboard()
else:
    secondpoint = ImageGrab.grab()
secondpointscaled = scaleDebugScreen(secondpoint, hudSize, monitorSize)
secondpointvalues = readProcessedScreen(secondpointscaled)
time.sleep(1)

strongholdvalues = findStronghold(firstpointvalues[0], firstpointvalues[1], firstpointvalues[2],\
                                  secondpointvalues[0], secondpointvalues[1], secondpointvalues[2])
                  
print("Found Stronghold! X =", strongholdvalues[0], "Z =", strongholdvalues[1])
input("Press ENTER to exit")
