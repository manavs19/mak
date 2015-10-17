import os
from os.path import expanduser
import subprocess
import time
import signal

use  = []
def init():
	home = expanduser("~")
	os.chdir(home)

	#xdg-open uses default file browser
	#works for file and folder
	p = subprocess.Popen(["xdg-open", os.curdir])

	time.sleep(1)
	wm = subprocess.check_output(["wmctrl", "-l"])
	global use
	for line in wm.splitlines():
		line = line.split()
		# print type(line)
		# print line
		if line[1]!="-1" and line[3]=="Home":
			use = line

	print use

# subprocess.call(["wmctrl",  "-i",  "-c", use[0]])

def getFolderNames():
	folderNames = [f for f in os.listdir('.') if not os.path.isfile(f)]
	return folderNames

def getFileNames():
	fileNames = [f for f in os.listdir('.') if os.path.isfile(f)]
	return fileNames	

def ls():
	# files = [f for f in os.listdir('.') if os.path.isfile(f)]
	# for f in files:
	# 	print f
	print getFolderNames()

def checkOpen():
	""" Checks if window is open """
	wm = subprocess.check_output(["wmctrl", "-l"])
	for line in wm.splitlines():
		line = line.split()
		if line[0]==use[0]:
			return 1
	return 0

def cd(folderName):
	if checkOpen()==0:
		print "window not open"
		return #window not open
	folderNames = getFolderNames()
	#check case also
	if folderName not in folderNames:
		return #folder not found
	subprocess.call(["xdotool", "windowactivate", str(use[0])])
	subprocess.call(["xdotool", "key", "--window", str(use[0]),  "Ctrl+L"])
	subprocess.call(["xdotool", "type", str(folderName)+"\n"])

	os.chdir(folderName)
	# print getDirectoryFromAddressBar()


def getDirectoryFromAddressBar():
	time.sleep(1)
	subprocess.call(["xdotool", "windowactivate", str(use[0])])
	time.sleep(1)
	subprocess.call(["xdotool", "key", "--window", str(use[0]),  "Ctrl+L"])
	time.sleep(1)
	subprocess.call(["xdotool", "key", "--window", str(use[0]),  "Ctrl+C"])
	time.sleep(1)
	# subprocess.call(["xdotool", "windowactivate", str(use[0])])
	# time.sleep(1)
	xsel = subprocess.check_output(["xsel"]) #get text from clipboard
	print "dsfds",xsel
	return xsel
	

genericCommands = {"up":"alt+Up", "home":"alt+Home", "back":"alt+Left", "forward":"alt+Right"}
def genericCommand(command):
	if checkOpen()==0:
		print "window not open"
		return #window not open
	print command
	subprocess.call(["xdotool", "windowactivate", str(use[0])])
	time.sleep(1)
	print subprocess.call(["xdotool", "key", "--window", str(use[0]),  genericCommands[command]])

	# os.chdir(getDirectoryFromAddressBar())


# pid = p.pid
# print pid

# os.system("xdotool windowkill `xdotool getactivewindow`")
# os.system("xkill -id `xprop -root _NET_ACTIVE_WINDOW | cut -d\# -f2`")
# p.kill()
# p.terminate()
# os.kill(p.pid, signal.SIGINT)
# p.kill()


if __name__ == "__main__":
	init()
	while 1:
		print "mak>", 
		s = raw_input().strip().split()
		print s[0]
		if s[0]=="ls":
			ls()
		elif s[0]=="cd":
			cd(s[1])
		elif s[0]=="init":
			init()
		# elif s[0] in genericCommands:
		# 	genericCommand(s[0])
		elif s[0]=="exit":
			break
