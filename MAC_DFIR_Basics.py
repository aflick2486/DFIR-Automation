#! /usr/bin/env python

import os
import sys
import subprocess
from getopt import getopt, GetoptError

version = "0.1"

def usage():
	print """MAC DFIR Basics v%s

usage: %s --mount <mount_dir>

-u [username], --username [username]
	Specify a user

-m [path], --mount [path]
	Specify the mount point of the Mac OS Filesystem

"""%(version,sys.argv[0])

def get_args():
	if len(sys.argv[1:]) == 0:
		usage()
		sys.exit(0)
	try:
		opts, args = getopt(sys.argv[1:], 'mu:h', ["mount=", "username=", "help"])

	except GetoptError as err:
		sys.stdout.write(str(err))
		usage()
		sys.exit(2)

	for o, a in opts:
		cfg = {}
		cfg['mount'] = "/"
		cfg['username'] = "*"
		if o in ("-h", "--help"):
			usage()
			sys.exit(0)
		elif o in ("-u", "--username"):
			cfg['username'] = a
		elif o in ("-m", "--mount"):
			cfg['mount'] = a

	if os.path.isdir(cfg["mount_dir"]):
		cfg["mount_dir"] = os.path.abspath(cfg["mount_dir"])
	else:
		print "Invalid mount directory"
		sys.exit(1)

	return cfg

def get_disks_partitions():
	partitions = ''
	for files in os.listdir('/dev'):
		if files.startswith("disk"):
			partitions += subprocess.check_output(['diskutil', 'info', '/dev/'+files])
		else:
			pass

def get_basic_device_info():
	#Grab basic software information (System Version, Computer Name, User Name)
	software_info = subprocess.check_output(['system_profiler', 'SPSoftwareDataType'])
	#Grab Basic hardware information (Model, Serial Number, Processor)
	hardware_info = subprocess.check_output(['system_profiler', 'SPHardwareDataType'])


def get_launch_start_items():
	#List files that run at login
	launch_agents = ''
	launch_agents += subprocess.check_output(['ls', '-la', '/Library/LaunchAgents'])
	launch_agents += subprocess.check_output(['ls', '-la', '/System/Library/LaunchAgents'])
	launch_agents += subprocess.check_output(['ls', '-la', '/Users/'+username+'/Library/LaunchAgents'])

	#List files that run at boot
	launch_daemons = ''
	launch_daemons += subprocess.check_output(['ls', '-la', '/Library/LaunchDaemons'])
	launch_daemons += subprocess.check_output(['ls', '-la', '/System/Library/LaunchDaemons'])

	#List other files that run on startup
	startup = ''
	startup += subprocess.check_output(['ls', '-la', '/Library/StartupItems'])
	startup += subprocess.check_output(['ls', '-la', '/System/Library/StartupItems'])


def browser_info():
	#List all Google Chrome Extensions and History
	if os.path.isfile('/Applications/Google Chrome.app'):
		chrome_history = ''
		chrome_ext = ''
		chrome_ext += subprocess.check_output(['ls', '/Users/*/Library/Application\ Support/Google/Chrome/Default/Extensions'])

	#List all Firefox Extensions and History
	elif os.path.isfile('/Applications/Firefox.app'):
		firefox_history = ''
		firefox_ext = ''

	#List all Safari Extensions and History
	elif os.path.isfile('/Applications/Safari.app'):
		safari_history = ''
		safari_ext = ''

def get_downloaded_files():
