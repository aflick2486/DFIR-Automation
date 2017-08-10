#! /usr/bin/env python

import argparse
import datetime
import os
import sys
import subprocess
import re
import sqlite3


version = '0.0.1'

def usage():
	print """Windows DFIR Basics v%s

usage: sudo python %s

Specify all artifacts that you would like to gather. Does nothing by default.

I Dont know how this script is going to work yet..

Going to use powershell script instead??

"""(version, sys.argv[0])

def get_args():
	cfg = {}

	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
		description=("""\
-----------------------
 Windows DFIR Basics
 Author: Adam Flickema
-----------------------
Specify all artifacts that you would like to gather. Does nothing by default."""))

	parser.add_argument('--all', action='store_true', dest='all', default=False,
						help="Gather all artifact information")

	parser.add_argument('-a', '--account', action='store_true', dest='account', default=False,
						help="Gather information on accoutn usage artifacts.")

	parser.add_argument('-b', '--browser', action='store_true', dest='browser', default=False,
						help="Gather information on browser usage artifacts.")

	parser.add_argument('-d', '--downloads', action='store_true', dest='downloads', default=False,
						help="Gather all file download artifacts. (Open/Save MRU, Email Attachments, Skype History, Index.dat/Places.sqlite, Downloads.sqlite)")

	parser.add_argument('-e', '--execution', action='store_true', dest='execute', default=False,
						help="Gather all program execution artifacts.")

	parser.add_argument('-f', '--files', action='store_true', dest='files', default=False,
						help="Gather information on file opening and creation artifacts.")

	parser.add_argument('-k', '--knowledge', action='store_true', dest='knowledge', default=False,
						help="Gather information on deleted files and file knowledge artifacts.")

	parser.add_argument('--mount', action='store', dest='mount', default="C:\\",
						help="Specify the mount directory for the image. Default is 'C:\\")

	parser.add_argument('-p', '--physical', action='store_true', dest='physical', default=False,
						help="Gather information on the physical location artifacts of the imaged device.")

	parser.add_argument('-u', '--usb', action='store_true', dest='usb', default=False,
						help="Gather information on USB and drive usage artifacts.")

	parser.add_argument('--username', action='store', dest='username', default="",
						help="Specify one username to run search the given artifacts for. Default is all users.")

	if len(sys.argv[1:]) == 0:
		parser.print_help()
		parser.exit()
		sys.exit(0)

	if results.all == True:
		cfg['account'] = True
		cfg['browser'] = True
		cfg['downloads'] = True
		cfg['execution'] = True
		cfg['files'] = True
		cfg['knowledge'] = True
		cfg['physical'] = True
		cfg['usb'] = True
	else:
		cfg['account'] = results.account
		cfg['browser'] = results.browser
		cfg['downloads'] = results.downloads
		cfg['execution'] = results.execute
		cfg['files'] = results.files
		cfg['knowledge'] = results.knowledge
		cfg['physical'] = results.physical
		cfg['usb'] = results.usb

	cfg['mount'] = str(results.mount_point)
	if cfg['mount'] != "":
		if os.path.isdir(cfg["mount"]):
			cfg["mount"] = os.path.abspath(cfg["mount"])
		else:
			print "Invalid mount directory"
			sys.exit(1)

	if results.username == "":
		cfg['username'] = []
		for user in os.listdir(cfg['mount']+'Users'):
			if user.startswith('.'):
				pass
			else:
				cfg['username'].append(user)
	else:
		cfg['username'] = str(results.username)

	return cfg


#Need to determine which OS the image is from
# subprocess.check_output(['wmic', 'datafile', 'where', 'name="c:\\windows\\explorer.exe"', 'get', 'version'])
# 5.1.2600 == xp
# 5.2.3790 == Server 2003
# 6.0* == Vista
# 6.1* == Win7 or Server 2008
# 6.2* == Win 8 or Server 2012
# 6.3* == Win 8.1 or Server 2012 R2
# 10.0* == Win 10 or Server 2016

if

def get_file_downloads():
#Open/Save MRU
# Windows XP
# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSaveMRU
# Windows 7
# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePIDlMRU



#Email Attachments
# Windows XP
# %USERPROFILE%\Local Settings\Application Data\Microsoft\Outlook
# Windows 7
# %USERPROFILE%\AppData\Local\Microsoft\Outlook



#Skype history
# Windows XP
# C:\Documents and Settings\<username>\Application\Skype\<skype-name>
# Windows 7
# C:\Users\<username>\AppData\Roaming\Skype\<skype-name>


#Index.dat/Places.sqlite
# Internet Explorer
# Windows XP
# %userprofile%\Local Settings\History\History.IE5
# Windows 7
# %userprofile%\AppData\Local\Microsoft\Windows\History\History.IE5
# %userprofile%\AppData\Local\Microsoft\Windows\History\Low\History.IE5
# Firefox
# Windows XP
# %userprofile%\Application Data\Mozilla\Firefox\Profiles\<random text>.default\places.sqlite
# Windows 7
# %userprofile%\AppData\Roaming\Mozilla\Firefox\Profiles\<random text>.default\places.sqlite


#Downloads.sqlite (Firefox)
# Windows XP
# %userprofile%\Application Data\Mozilla\Firefox\Profiles\<random text>.default\downloads.sqlite
# Windows 7
# %userprofile%\AppData\Roaming\Mozilla\Firefox\Profiles\<random text>.default\downloads.sqlite


def get_program_execution():

#UserAssist
# NTUSER.DAT\Software\Microsoft\Windows\Currentversion\Explorer\UserAssist\{GUID}\Count
# GUID Windows XP
#	75048700
# GUID Windows 7
#	CEBFF5CD
#	F4E57C4B
# Data is ROT13 encoded


#Last Visited MRU
# Windows XP
# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedMRU
# Windows 7
# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU


#RunMRU Start->Run
# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU


#Application Compatibility Cache
# Windows XP
# SYSTEM\CurrentControlSet\Control\SessionManager\AppCompatibility\
# Windows 7
# SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache


#Win7 Jump Lists
# Only Windows 7
# C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations


#Prefetch
# C:\Windows\Prefetch\(exename)-(hash).pf


#Services Events
# Event ID
# 7034 - Service crashed unexpectedly
# 7035 - Service sent a Start/Stop Control
# 7036 - Service started or stopped
# 7040 - Start type changed (Boot|On Request|Disabled)



def get_file_open_create():

#Open/Save MRU
# Windows XP
# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSaveMRU
# Windows 7
# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePIDlMRU

#Last Visited MRU
# Windows XP
# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\ LastVisitedMRU
# Windows 7
# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU

#Recent Files
# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs

#Office Recent Files
# NTUSER.DAT\Software\Microsoft\
# Office\VERSION
# • 14.0 = Office 2010
# • 12.0 = Office 2007
# • 11.0 = Office 2003
# • 10.0 = Office XP

#Shell Bags
# Windows XP
# NTUSER.DAT\Software\Microsoft\Windows\Shell\Bags
# NTUSER.DAT\Software\Microsoft\Windows\Shell\BagMRU
# NTUSER.DAT\Software\Microsoft\Windows\ShellNoRoam\Bags
# NTUSER.DAT\Software\Microsoft\Windows\ShellNoRoam\BagMRU
# Windows 7
# USRCLASS.DAT\Local Settings\Software\Microsoft\Windows\Shell\Bags
# USRCLASS.DAT\Local Settings\Software\Microsoft\Windows\Shell\BagMRU
# NTUSER.DAT\Software\Microsoft\Windows\Shell\BagMRU
# NTUSER.DAT\Software\Microsoft\Windows\Shell\Bags

#Shortcut LNK Files
# Windows XP
# C:\Documents and Settings\<username>\Recent\
# Windows 7
# C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Recent\
# C:\Users\<user>\AppData\Roaming\Microsoft\Office\Recent\

#Win7 Jump Lists
# C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations

#Prefetch
# C:\Windows\Prefetch

#Index.dat file://
# Windows XP
# %userprofile%\Local Settings\History\History.IE5
# Windows 7
# %userprofile%\AppData\Local\Microsoft\Windows\History\History.IE5
# %userprofile%\AppData\Local\Microsoft\Windows\History\Low\History.IE5


def get_deleted_file_knowledge():

#XP Search - ACMRU
# NTUSER.DAT\Software\Microsoft\Search Assistant\ACMru\####
# • Search the Internet – ####=5001
# • All or part of a document name – ####=5603
# • A word or phrase in a file – ####=5604
# • Printers, Computers and People – ####=5647

#Win7 Search - WordWheelQuery
# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery

#Last Visited MRU
# Windows XP
# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\ LastVisitedMRU
# Windows 7
# NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU


#Vista/Win7 Thumbnails
# C:\Users\<username>\AppData\Local\Microsoft\Windows\Explorer\

#XP Recycle Bin
# • Hidden System Folder
# • Windows XP
# - C:\RECYCLER” 2000/NT/XP/2003
# - Subfolder is created with user’s SID
# - Hidden file in directory called “INFO2”
# - INFO2 Contains Deleted Time and Original Filename
# - Filename in both ASCII and UNICODE

#Win7 Recycle Bin
# • Hidden System Folder
# • Windows 7
#  - C:\$Recycle.bin
#  - Deleted Time and Original Filename contained
# in separate files for each deleted recovery file

#Index.dat file://
# Windows XP
# %userprofile%\Local Settings\History\History.IE5
# Windows 7
# %userprofile%\AppData\Local\Microsoft\Windows\History\History.IE5
# %userprofile%\AppData\Local\Microsoft\Windows\History\Low\History.IE5


def get_physical_location():

#Timezone
# SYSTEM\CurrentControlSet\Control\TimeZoneInformation


#Vista/Win7 Network History
# • SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged
# • SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Managed
# • SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Nla\Cache

#Cookies
# Internet Explorer
# Windows XP
# %userprofile%\Cookies
# Windows 7
# %userprofile%\AppData\Roaming\Microsoft\Windows\Cookies
# %userprofile%\AppData\Roaming\Microsoft\Windows\Cookies\Low
# Firefox
# Windows XP
# %userprofile%\Application Data\Mozilla\Firefox\Profiles\<random text>.default\cookies.sqlite
# Windows 7
# %userprofile%\AppData\Roaming\Mozilla\Firefox\Profiles\<random text>.default\cookies.sqlite

#Browser Search Terms
#Internet Explorer
# Windows XP
# %userprofile%\Local Settings\History\History.IE5
# Windows 7
# %userprofile%\AppData\Local\Microsoft\Windows\History\History.IE5
# %userprofile%\AppData\Local\Microsoft\Windows\History\Low\History.IE5
# Firefox
# Windows XP
# %userprofile%\Application Data\Mozilla\Firefox\Profiles\<random text>.default\places.sqlite
# Windows 7
# %userprofile%\AppData\Roaming\Mozilla\Firefox\Profiles\<random text>.default\places.sqlite


def get_usb():

#Key Identification
# • SYSTEM\CurrentControlSet\Enum\USBSTOR
# • SYSTEM\CurrentControlSet\Enum\USB

#First/Last Times
# Location: First Time
# • Plug and Play Log Files
# XP C:\Windows\setupapi.log
# Win7 C:\Windows\inf\setupapi.dev.log
# Location: Last Time
# • NTUSER.DAT Hive: NTUSER//Software/Microsoft/Windows/CurrentVersion/Explorer/MountPoints2/{GUID}

#User
# • Look for GUID from SYSTEM\MountedDevices
# • NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\MountPoints2

#Volume Serial Number
# • SOFTWARE\Microsoft\Windows NT\CurrentVersion\ENDMgmt
# • Use Volume Name and USB Unique Serial Number to find
# • Last integer number in line
# • Convert Decimal Serial Number into Hex Serial Number

#Drive Letter & Volume Name
# Location: XP
# • Find ParentIdPrefix
# - SYSTEM\CurrentControlSet\Enum\USBSTOR
# • Using ParentIdPrefix Discover Last Mount Point
# - SYSTEM\MountedDevices
# Location: Win7
# • SOFTWARE\Microsoft\Windows Portable Devices\Devices
# • SYSTEM\MountedDevices
# - Examine Drive Letter’s looking at Value Data Looking
# for Serial Number

#Shortcut LNK Files
# XP C:\Documents and Settings\<username>\Recent\
# Win7 C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Recent\
# Win7 C:\Users\<user>\AppData\Roaming\Microsoft\Office\Recent\

#Plug and Play Event Log
# Win7 %system root%\System32\winevt\logs\System.evtx

def get_account_usage():

#Last Login
# • C:\windows\system32\config\SAM
# • SAM\Domains\Account\Users

#Last Password Change
# • C:\windows\system32\config\SAM
# • SAM\Domains\Account\Users

#Success/Fail Logons
# XP %system root%\System32\config\SecEvent.evt
# Win7 %system root%\System32\winevt\logs\Security.evtx
# Interpretation:
# • XP/Win7 - Interpretation
# • Event ID - 528/4624 – Successful Logon
# • Event ID - 529/4625 – Failed Logon
# • Event ID - 538/4634 – Successful Logoff
# • Event ID - 540/4624 – Successful Network Logon
# (example: file shares)

#Logon Types
# XP Event ID 528
# Win7 Event ID 4624
# Interpretation:
# Logon Type Explanation
# 2 			Logon via console
# 3 			Network Logon
# 4 			Batch Logon
# 5 			Windows Service Logon
# 7 			Credentials used to unlock screen
# 8 			Network logon sending credentials (cleartext)
# 9 			Different credentials used than logged on user
# 10 			Remote interactive logon (RDP)
# 11 			Cached credentials used to logon

#RDP Usage
# XP %system root%\System32\config\SecEvent.evt
# Win7 %system root%\System32\winevt\logs\Security.evtx


def get_browser_usage():

#History
# Location: Internet Explorer
# XP %userprofile%\Local Settings\History\ History.IE5
# Win7 %userprofile%\AppData\Local\Microsoft\Windows\History\History.IE5
# Win7 %userprofile%\AppData\Local\Microsoft\Windows\History\Low\History.IE5
# Location: Firefox
# XP %userprofile%\Application Data\Mozilla\Firefox\Profiles\<random text>.default\places.sqlite
# Win7 %userprofile%\AppData\Roaming\Mozilla\Firefox\Profiles\<random text>.default\places.sqlite

#Cookies
# Location: Internet Explorer
# XP %userprofile%\Cookies
# Win7 %userprofile%\AppData\Roaming\Microsoft\Windows\Cookies
# Win7 %userprofile%\AppData\Roaming\Microsoft\Windows\Cookies\Low
# Location: Firefox
# XP %userprofile%\Application Data\Mozilla\Firefox\Profiles\<random text>.default\cookies.sqlite
# Win7 %userprofile%\AppData\Roaming\Mozilla\Firefox\Profiles\<random text>.default\cookies.sqlite


#Cache
# Location: Internet Explorer
# XP %userprofile%\Local Settings\Temporary Internet Files\Content.IE5
# Win7 %userprofile%\AppData\Local\Microsoft\Windows\Temporary Internet Files\Content.IE5
# Win7 %userprofile%\AppData\Local\Microsoft\Windows\Temporary Internet Files\Low\Content.IE5
# Location: Firefox
# XP %userprofile%\Local Settings\Application Data\Mozilla\ Firefox\Profiles\<random text>.default\Cache
# Win7 %userprofile%\AppData\Local\Mozilla\ Firefox\Profiles\<random text>.default\Cache


#Session Restore
# Location: Internet Explorer
# XP %userprofile%/Local Settings/Application Data/Microsoft/Internet Explorer/Recovery
# Win7 %userprofile%/AppData/Local/Microsoft/InternetExplorer/Recovery
# Location: Firefox
# XP %userprofile%\Application Data\Mozilla\Firefox\Profiles\<random text>.default\sessionstore. js
# Win7 %userprofile%\AppData\Roaming\Mozilla\Firefox\Profiles\<random text>.default\sessionstore. js


#Flash and Super Cookies
# Location: Internet Explorer
# XP %APPDATA%\Macromedia\Flash Player\
# XP %APPDATA%\Macromedia\Flash
# XP %APPDATA%\Macromedia\Flash Player\macromedia.com\support\flashplayer\sys
# Win7 %APPDATA%\Roaming\Macromedia\Flash Player\
# Win7 %APPDATA%\Roaming\Macromedia\Flash Player\#SharedObjects\<random profile id>
# Win7 %APPDATA%\Roaming\Macromedia\Flash Player\macromedia.com\support\flashplayer\sys
