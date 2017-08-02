#! /usr/bin/env python

import os
import sys
import subprocess
import re
import sqlite3
from getopt import getopt, GetoptError

version = "0.3.1"

def usage():
	print """MAC DFIR Basics v%s

usage: %s --mount <mount_dir>

-b, --browser
	Gather web browser information (history, extensions)

-e, --emails
	Gather email information (From, Subject, Timestamp)

-m [path], --mount [path]
	Specify the mount point of the Mac OS Filesystem

-u [username], --username [username]
	Specify a username. DEFAULT is all users

"""%(version,sys.argv[0])

def get_args():
	if len(sys.argv[1:]) == 0:
		usage()
		sys.exit(0)
	try:
		opts, args = getopt(sys.argv[1:], 'mu:he', ["mount=", "username=", "help", "emails"])

	except GetoptError as err:
		sys.stdout.write(str(err))
		usage()
		sys.exit(2)

	for o, a in opts:
		cfg = {}
		cfg['mount'] = "/"
		cfg['username'] = "*"
		cfg['emails'] = False
		if o in ("-h", "--help"):
			usage()
			sys.exit(0)
		elif o in ("-u", "--username"):
			cfg['username'] = a
		elif o in ("-m", "--mount"):
			cfg['mount'] = a
		elif o in ("-e", "--emails"):
			cfg['emails'] = True

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
		chrome_ext += subprocess.check_output(['ls', '/Users/'+username'/Library/Application\ Support/Google/Chrome/Default/Extensions'])
		conn = None

		try:
			conn = sqlite3.connect("/Users/"+username+"/Library/Application\ Support/Google/Chrome/Default/History")

			cur = conn.cursor()
			cur.execute("SELECT urls.last_visit_time, urls.url, urls.title FROM urls, visits WHERE urls.id = visits.url ORDER BY visits.visit_time ASC")

			rows = cur.fetchall()

			for row in rows:
				chrome_history += row + "\n"
		except sqlite3.Error as e:
			print e
		finally:
			if conn:
				conn.close()

	#List all Firefox Extensions and History
	elif os.path.isfile('/Applications/Firefox.app'):
		firefox_history = ''
		firefox_ext = ''
		chrome_ext += subprocess.check_output(['ls', '/Users/'+username'/Library/Application\ Support/Mozilla/Extensions'])
		conn = None

		try:
			conn = sqlite3.connect("/Users/"+username+"/Library/Application\ Support/Firefox/Profiles/*/places.sqlite")

			cur = conn.cursor()
			cur.execute("SELECT moz_historyvisits.visit_date, moz_places.url, moz_places.title, moz_places.rev_host FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id ORDER BY moz_historyvisits.visit_date ASC")

			rows = cur.fetchall()

			for row in rows:
				chrome_history += row + "\n"
		except sqlite3.Error as e:
			print e
		finally:
			if conn:
				conn.close()

	#List all Safari Extensions and History
	elif os.path.isfile('/Applications/Safari.app'):
		safari_history = ''
		safari_ext = ''

def get_downloaded_files():
	downloads = ""
	path = os.path.join("Users", username, "Library", "Preferences", "com.apple.LaunchServices.QuarantineEventsV2")
	conn = None
	try:
		conn = sqlite3.connect(path)
		cur = conn.cursor()
		cur.execute("SELECT LSQuarantineDataURLString FROM LSQuarantineEvent")
		rows = cur.fetchall()
		for row in rows:
			downloads += row + "\n"

	except sqlite3.Error as e:
		print e
	finally:
		if conn:
			conn.close()


def get_emails(emails):
	emails = ''
	rootdir = "/Users/"+username+"/Library/Mail"

	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			if "[Gmail]" in subdir:
				if ".emlx" in file:
					print file
					with open(os.path.join(subdir, file), "r") as email:
						for line in email:
							match = re.compile('From: (.*)')
							email_from = match.match(line)
							if email_from:
								print email_from.group()
							else:
								pass
							match = re.compile('Date: (.*)')
							timestamp = match.match(line)
							if timestamp:
								print timestamp.group()
							match = re.compile('Subject: (.*)')
							subject = match.match(line)
							if subject:
								print subject.group()
					print "\n----------------------------------\n"
