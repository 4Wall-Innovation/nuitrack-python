from PyNuitrack import py_nuitrack
import keyboard

nuitrack = py_nuitrack.Nuitrack()
nuitrack.init()

emulateKeyboard = True

devices = nuitrack.get_device_list()
for i, dev in enumerate(devices):
	print(dev.get_name(), dev.get_serial_number())
	if i == 0:
		#dev.activate("ACTIVATION_KEY") #you can activate device using python api
		print(dev.get_activation())
		nuitrack.set_device(dev)

print(nuitrack.get_version())
print(nuitrack.get_license())

nuitrack.create_modules()
nuitrack.run()

def sortFunction(e):
	return e.torso.real[2]

def checkLeaning(waist,neck):
	threshold = 50
	if(neck["x"]>(waist["x"]+threshold)):
		return 1
	if(neck["x"]<(waist["x"]-threshold)):
		return -1
	return 0

def checkHandPositions(torso,left,right):
	threshold = 500
	if(left["y"]>(torso["y"]+threshold) or right["y"]>(torso["y"]+threshold) ):
		return 1
	else:
		return 0
	
def pressKey(key):
	if(emulateKeyboard):
		keyboard.press_and_release(key)


while 1:
	nuitrack.update()
	data = nuitrack.get_skeleton()
	data.skeletons.sort(key=sortFunction)
	if(len(data.skeletons)>0):
		skeleton = data.skeletons[0]
		waist = {"x":skeleton.waist.real[0],"y":skeleton.waist.real[1],"z":skeleton.waist.real[2]}
		torso = {"x":skeleton.torso.real[0],"y":skeleton.torso.real[1],"z":skeleton.torso.real[2]}
		neck = {"x":skeleton.neck.real[0],"y":skeleton.neck.real[1],"z":skeleton.neck.real[2]}
		right_hand = {"x":skeleton.right_hand.real[0],"y":skeleton.right_hand.real[1],"z":skeleton.right_hand.real[2]}
		left_hand = {"x":skeleton.left_hand.real[0],"y":skeleton.left_hand.real[1],"z":skeleton.left_hand.real[2]}

		if(checkHandPositions(torso,left_hand,right_hand)==1):
			print("FIRE")
			pressKey("space")
		if(checkLeaning(waist,neck)==1):
			print("LEFT")
			pressKey("left")
		if(checkLeaning(waist,neck)==-1):
			print("RIGHT")
			pressKey("right")

nuitrack.release()
