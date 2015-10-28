import os
from os.path import expanduser
import subprocess
import time
import signal
import speech_recognition as sr
import traceback

# def tts(text):
# 	subprocess.call(["espeak", text])

def notify(text):
	#expire in 2 seconds, icon of sad face, title is Error!, text is text
	subprocess.call(["notify-send", "-t", "2000", "-i", "face-sad", "Error!", text])
	# pass

use  = []
def start():
	#check if a file explorer is already open
	global use
	if use and checkOpen()==1:
		notify("File explorer already open!")
		print "File explorer already open!"
		return

	home = expanduser("~")
	os.chdir(home)

	#xdg-open uses default file browser
	#works for file and folder
	p = subprocess.Popen(["xdg-open", os.curdir])

	time.sleep(1)
	wm = subprocess.check_output(["wmctrl", "-l"])
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

def list():
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
	subprocess.call(["xdotool", "windowactivate", str(use[0])])
	subprocess.call(["xdotool", "key", "--window", str(use[0]),  "Ctrl+L"])#useless statement
	subprocess.call(["xdotool", "type", str(folderName)+"\n"])

	os.chdir(folderName)

def openFile(fileName):
	p = subprocess.Popen(["xdg-open", fileName])


def open(folderName):
	if checkOpen()==0:
		notify("File explorer not open. Say \"start\" to open a new file explorer or \"exit\" to end this session.")
		print "File explorer not open"
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

	if flag==1:#found folder
		openFolder(folderName)
	else:#folder not found, search for file
		fileNames = getFileNames()
		#check case also
		flag2=0
		fileName = folderName
		for f in fileNames:
			#Get case sensitive name for folder
			temp = f.split(".")[0]
			if fileName.lower() == temp.lower():
				fileName = f
				flag2=1
				break

		if flag2==1:
			openFile(fileName)
		else:#file not found
			notify("Could not find file/folder named: " + folderName)


def getDirectoryFromAddressBar():
	time.sleep(0.1)
	subprocess.call(["xdotool", "key", "ctrl+l"])
	subprocess.call(["xdotool", "key", "ctrl+c"])
	xsel = subprocess.check_output(["xsel"]) #get text from clipboard
	subprocess.call(["xdotool", "key", "Escape"])
	print "address: ",xsel
	return xsel
	
#removed up since recognition is not good
genericCommands = {"home":"alt+Home", "back":"alt+Up", "last":"alt+Left", "next":"alt+Right"}
def genericCommand(command):
	if checkOpen()==0:
		notify("File explorer not open. Say \"start\" to open a new file explorer or \"exit\" to end this session.")
		print "File explorer not open"
		return #window not open
	
	subprocess.call(["xdotool", "windowactivate", str(use[0])])
	subprocess.call(["xdotool", "key", genericCommands[command]])

	os.chdir(getDirectoryFromAddressBar())

def create(folderName):
	if checkOpen()==0:
		notify("File explorer not open. Say \"start\" to open a new file explorer or \"exit\" to end this session.")
		print "File explorer not open"
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
		notify("Folder named: " + folderName + " is already present in this directory")
		return

	p = subprocess.Popen(["mkdir", folderName])

def delete(folderName):
	if checkOpen()==0:
		notify("File explorer not open. Say \"start\" to open a new file explorer or \"exit\" to end this session.")
		print "File explorer not open"
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
		notify("Folder named: " + folderName + " is not present in this directory")
		return

	p = subprocess.Popen(["rm", "-rf", folderName])

def rename(oldName, newName):
	if checkOpen()==0:
		notify("File explorer not open. Say \"start\" to open a new file explorer or \"exit\" to end this session.")
		print "File explorer not open"
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
		notify("Folder named: " + oldName + " is not present in this directory")
		return

	p = subprocess.Popen(["mv", oldName, newName])	

def show():
	""" Show the file explorer """
	if checkOpen()==0:
		notify("File explorer not open. Say \"start\" to open a new file explorer or \"exit\" to end this session.")
		print "File explorer not open"
		return #window not open
	subprocess.call(["xdotool", "windowactivate", str(use[0])])	


def exit():
	if checkOpen():
		subprocess.call(["wmctrl",  "-i",  "-c", use[0]])


if __name__ == "__main__":
	try:
		start()
		# obtain audio from the microphone
		r = sr.Recognizer()
		with sr.Microphone() as source:
			r.adjust_for_ambient_noise(source)
			
			while 1:
				try:
					print("Say something!")
					audio = r.listen(source)
				
					s = ""
					try:
						# for testing purposes, we're just using the default API key
						# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
						# instead of `r.recognize_google(audio)`
						s = r.recognize_google(audio, language = "en-IN")
						s = s.lower()
						print("Google Speech Recognition thinks you said " + s)
					except:
						#Some error in speech recognition
						notify("Sorry! I could not recognize that.")
						traceback.print_exc()
						continue
					# except sr.UnknownValueError:
					#     print("Google Speech Recognition could not understand audio")
					# except sr.RequestError as e:
					#     print("Could not request results from Google Speech Recognition service; {0}".format(e))

					print "mak>", 
					s = s.split(" ", 1)#split once at space
					print s
					if s[0]=="list":
						list()
					elif s[0]=="open":#open file/folder
						open(s[1])
					elif s[0]=="show":
						show()
					elif s[0] in genericCommands:
						genericCommand(s[0])
					elif s[0]=="create":
						create(s[1])
					elif s[0]=="delete":
						delete(s[1])
					elif s[0]=="rename":
						temp = s[1].split()
						rename(temp[0], temp[1])
					elif s[0]=="start":
						start()
					elif s[0]=="exit":
						exit()
						break
					else:
						temp = "".join(s)
						notify(temp + " is not a valid command.")

				except:#catch any error in while
					notify("Sorry! I could not recognize that.")
					traceback.print_exc()
					continue

	except:
		notify("Sorry! Could not read the microphone.")
		traceback.print_exc()



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