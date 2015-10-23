import os
from os.path import expanduser
import subprocess
import time
import signal
import speech_recognition as sr

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
		if line[1]!="-1" and line[3]=="Home":
			use = line

	print use

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

def openFolder(folderName):
	if checkOpen()==0:
		print "window not open"
		return #window not open
	folderNames = getFolderNames()
	#check case also
	flag=0
	for f in folderNames:
		#Get case sensitive name for folder
		if folderName.lower() == f.lower():
			folderName = f
			flag=1
			break

	if flag==0:#folder not found
		return

	subprocess.call(["xdotool", "windowactivate", str(use[0])])
	subprocess.call(["xdotool", "key", "--window", str(use[0]),  "Ctrl+L"])
	subprocess.call(["xdotool", "type", str(folderName)+"\n"])

	os.chdir(folderName)

def openFile(fileName):
	""" Opens file if present in current directory """
	if checkOpen()==0:
		print "window not open"
		return #window not open
	fileNames = getFileNames()
	#check case also
	flag=0
	for f in fileNames:
		#Get case sensitive name for folder
		temp = f.split(".")[0]
		if fileName.lower() == temp.lower():
			fileName = f
			flag=1
			break

	if flag==0:#file not found
		return

	p = subprocess.Popen(["xdg-open", fileName])

def getDirectoryFromAddressBar():
	time.sleep(0.01)
	subprocess.call(["xdotool", "key", "ctrl+l"])
	subprocess.call(["xdotool", "key", "ctrl+c"])
	xsel = subprocess.check_output(["xsel"]) #get text from clipboard
	subprocess.call(["xdotool", "key", "Escape"])
	print "address: ",xsel
	return xsel
	

genericCommands = {"up":"alt+Up", "home":"alt+Home", "back":"alt+Left", "forward":"alt+Right"}
def genericCommand(command):
	if checkOpen()==0:
		print "window not open"
		return #window not open
	
	subprocess.call(["xdotool", "windowactivate", str(use[0])])
	subprocess.call(["xdotool", "key", genericCommands[command]])

	os.chdir(getDirectoryFromAddressBar())

def create(folderName):
	if checkOpen()==0:
		print "window not open"
		return #window not open
	folderNames = getFolderNames()
	#check case also
	flag=0
	for f in folderNames:
		#Get case sensitive name for folder
		if folderName.lower() == f.lower():
			flag=1
			break

	if flag==1:#folder already present
		return

	p = subprocess.Popen(["mkdir", folderName])

def delete(folderName):
	if checkOpen()==0:
		print "window not open"
		return #window not open
	folderNames = getFolderNames()
	#check case also
	flag=0
	for f in folderNames:
		#Get case sensitive name for folder
		if folderName.lower() == f.lower():
			folderName = f
			flag=1
			break

	if flag==0:#folder not found
		return

	p = subprocess.Popen(["rm", "-rf", folderName])

def rename(oldName, newName):
	if checkOpen()==0:
		print "window not open"
		return #window not open
	folderNames = getFolderNames()
	#check case also
	flag=0
	for f in folderNames:
		#Get case sensitive name for folder
		if oldName.lower() == f.lower():
			oldName = f
			flag=1
			break

	if flag==0:#folder not found
		return

	p = subprocess.Popen(["mv", oldName, newName])	


def exit():
	if checkOpen():
		subprocess.call(["wmctrl",  "-i",  "-c", use[0]])


if __name__ == "__main__":
	init()
	while 1:
		try:
			# obtain audio from the microphone
			r = sr.Recognizer()
			with sr.Microphone() as source:
				print("Say something!")
				audio = r.listen(source)

			s = ""
			try:
				# for testing purposes, we're just using the default API key
				# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
				# instead of `r.recognize_google(audio)`
				s = r.recognize_google(audio)
				s = s.lower()
				print("Google Speech Recognition thinks you said " + s)
			except:
				#Some error in speech recognition
				continue
			# except sr.UnknownValueError:
			#     print("Google Speech Recognition could not understand audio")
			# except sr.RequestError as e:
			#     print("Could not request results from Google Speech Recognition service; {0}".format(e))

			print "mak>", 
			s = s.split(" ", 1)#split once at space
			print s
			if s[0]=="ls":
				ls()
			elif s[0]=="open":
				openFolder(s[1])
			elif s[0] in genericCommands:
				genericCommand(s[0])
			elif s[0]=="create":
				create(s[1])
			elif s[0]=="delete":
				delete(s[1])
			elif s[0]=="rename":
				temp = s[1].split()
				rename(temp[0], temp[1])
			elif s[0]=="file":
				openFile(s[1])
			elif s[0]=="init":
				init()
			elif s[0]=="exit":
				exit()
				break

		except:#catch any error in while
			continue




""" 
# pid = p.pid
# print pid

# os.system("xdotool windowkill `xdotool getactivewindow`")
# os.system("xkill -id `xprop -root _NET_ACTIVE_WINDOW | cut -d\# -f2`")
# p.kill()
# p.terminate()
# os.kill(p.pid, signal.SIGINT)
# p.kill()
"""