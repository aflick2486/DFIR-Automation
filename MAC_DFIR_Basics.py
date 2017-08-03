#! /usr/bin/env python

import datetime
import os
import sys
import subprocess
import re
import sqlite3
from getopt import getopt, GetoptError

version = "1.0.1"

def usage():
	print """MAC DFIR Basics v%s

usage: sudo python %s --mount <mount_dir>

Specify all artifacts that you would like to gather. Does nothing by default.

-b, --browser
	Gather web browser information (history, extensions)

-d, --disk
	Gather information about disks and partitions

-e, --emails
	Gather email information (From, Subject, Timestamp)

-h, --history,
	Gather bash history information

-m [path], --mount [path]
	Specify the mount point of the Mac OS Filesystem

-o, --other
	Gather basic device software and hardware information

-s, --startup
	Gather startup item information (LaunchAgents, LaunchDaemons, StartupItems)

-u [username], --username [username]
	Specify a username. DEFAULT is all users

Examples:

$sudo python MAC_DFIR_Basics.py -bdeh
	Gathers information about browser history, disks and partitions, emails, and bash history

$sudo python MAC_DFIR_Basics.py -bdeh -m /mnt/mac/ -u root
	Gathers the information from the /mnt/mac/ directory for the root user

"""%(version,sys.argv[0])

def get_args():
	if len(sys.argv[1:]) == 0:
		usage()
		sys.exit(0)
	try:
		opts, args = getopt(sys.argv[1:], 'mu:hedobs', ["mount=", "username=", "history", "emails", "disk", "other", "browser", "startup"])

	except GetoptError as err:
		sys.stdout.write(str(err))
		usage()
		sys.exit(2)

	for o, a in opts:
		cfg = {}
		cfg['mount'] = "/"
		cfg['username'] = ''
		cfg['history'] = False
		cfg['emails'] = False
		cfg['browser'] = False
		cfg['disk'] = False
		cfg['startup'] = False
		cfg['other'] = False
		if o in ("-h", "--history"):
			cfg['history'] = True
		elif o in ("-u", "--username"):
			cfg['username'] = a
		elif o in ("-m", "--mount"):
			cfg['mount'] = a
		elif o in ("-e", "--emails"):
			cfg['emails'] = True
		elif o in ("-b", "--browser"):
			cfg['browser'] = True
		elif o in ("-d", "--disk"):
			cfg['disk'] = True
		elif o in ("-s", "--startup"):
			cfg['startup'] = True
		elif o in ("-o", "--other"):
			cfg['other'] = True

	if os.path.isdir(cfg["mount"]):
		cfg["mount"] = os.path.abspath(cfg["mount"])
	else:
		print "Invalid mount directory"
		sys.exit(1)

	if cfg['username'] == '':
		cfg['username'] = []
		for user in os.listdir(cfg['mount']+'Users'):
			if user.startswith('.'):
				pass
			else:
				cfg['username'].append(user)

	return cfg

def get_disks_partitions(username, mount):
	partitions = ''
	for files in os.listdir(mount+'dev'):
		if files.startswith("disk"):
			partitions += subprocess.check_output(['diskutil', 'info', mount+'dev/'+files])
			partitions += "----------------\n"
		else:
			pass

	partitions += "\n\n\n"
	return partitions

def get_basic_device_info():
	#Grab basic software information (System Version, Computer Name, User Name)
	software_info = subprocess.check_output(['system_profiler', 'SPSoftwareDataType'])
	#Grab Basic hardware information (Model, Serial Number, Processor)
	hardware_info = subprocess.check_output(['system_profiler', 'SPHardwareDataType'])

	basic_device_info = "Software Info\n"
	basic_device_info += "----------------\n"
	basic_device_info += software_info
	basic_device_info += "----------------\n\n"

	basic_device_info += "Hardware Info\n"
	basic_device_info += "----------------\n"
	basic_device_info += hardware_info
	basic_device_info += "----------------\n\n\n"

	return basic_device_info

def get_launch_start_items(username, mount):
	#List files that run at login
	launch_agents = ''
	launch_agents += subprocess.check_output(['ls', '-la', mount+'Library/LaunchAgents'])
	launch_agents += subprocess.check_output(['ls', '-la', mount+'System/Library/LaunchAgents'])
	if isinstance(username, list):
		for user in username:
			launch_agents += subprocess.check_output(['ls', '-la', mount+'Users/'+user+'/Library/LaunchAgents'])
	elif isinstance(username, basestring):
		launch_agents += subprocess.check_output(['ls', '-la', mount+'Users/'+username+'/Library/LaunchAgents'])

	#List files that run at boot
	launch_daemons = ''
	launch_daemons += subprocess.check_output(['ls', '-la', mount+'Library/LaunchDaemons'])
	launch_daemons += subprocess.check_output(['ls', '-la', mount+'System/Library/LaunchDaemons'])

	#List other files that run on startup
	startup = ''
	startup += subprocess.check_output(['ls', '-la', mount+'Library/StartupItems'])
	startup += subprocess.check_output(['ls', '-la', mount+'System/Library/StartupItems'])

	results = "Launch Agents\n"
	results += "----------------\n"
	results += launch_agents
	results += "----------------\n\n"

	results += "Launch Daemons\n"
	results += "----------------\n"
	results += launch_daemons
	results += "----------------\n\n"

	results += "Startup Items\n"
	results += "----------------\n"
	results += startup
	results += "----------------\n\n\n"

	return results

def get_browser_info(username, mount):
	#List all Google Chrome Extensions and History
	if os.path.isdir(mount+'Applications/Google Chrome.app/'):
		chrome_history = ''
		chrome_ext = ''
		if isinstance(username, list):
			for user in username:
				if os.path.isdir(mount+'Users/'+user+'/Library/Application Support/Google/Chrome/Default/Extensions'):
					chrome_ext += user + "\n"
					chrome_ext += str(os.listdir(mount+'Users/'+user+'/Library/Application Support/Google/Chrome/Default/Extensions')) + "\n"
					conn = None

					try:
						conn = sqlite3.connect(mount+"Users/"+user+"/Library/Application Support/Google/Chrome/Default/History")

						cur = conn.cursor()
						cur.execute("SELECT datetime(urls.last_visit_time/1000000-11644473600,'unixepoch','localtime'), urls.url, urls.title FROM urls, visits WHERE urls.id = visits.url ORDER BY visits.visit_time ASC")

						rows = cur.fetchall()
						chrome_history += user + "\n"
						for row in rows:
							chrome_history += str(row) + "\n"
					except sqlite3.Error as e:
						print "Chrome Error: %s" % e
					finally:
						if conn:
							conn.close()
		elif isinstance(username, basestring):
			if os.path.isdir(mount+'Users/'+username+'/Library/Application Support/Google/Chrome/Default/Extensions'):
				chrome_ext += username + "\n"
				chrome_ext += str(os.listdir(mount+'Users/'+username+'/Library/Application Support/Google/Chrome/Default/Extensions')) + "\n"
				conn = None

				try:
					conn = sqlite3.connect(mount+"Users/"+username+"/Library/Application Support/Google/Chrome/Default/History")

					cur = conn.cursor()
					cur.execute("SELECT datetime(urls.last_visit_time/1000000-11644473600,'unixepoch','localtime'), urls.url, urls.title FROM urls, visits WHERE urls.id = visits.url ORDER BY visits.visit_time ASC")

					rows = cur.fetchall()
					chrome_history += username + "\n"
					for row in rows:
						chrome_history += str(row) + "\n"
				except sqlite3.Error as e:
					print "Chrome Error: %s" % e
				finally:
					if conn:
						conn.close()

	#List all Firefox Extensions and History
	if os.path.isdir(mount+'Applications/Firefox.app/'):
			firefox_history = ''
			firefox_ext = ''
			if isinstance(username, list):
				for user in username:
					if os.path.isdir(mount+'Users/'+user+'/Library/Application Support/Firefox/Profiles/'):
						print "OK"
						profiles = os.listdir(mount+'Users/'+user+'/Library/Application Support/Firefox/Profiles/')
						firefox_ext += user + "\n"
						firefox_history += user + "\n"
						for profile in profiles:
							if profile.startswith('.'):
								pass
							else:
								if os.path.isdir(mount+'Users/'+user+'/Library/Application Support/Firefox/Profiles/'+profile+'/extensions'):
									firefox_ext += str(os.listdir(mount+'Users/'+user+'/Library/Application Support/Firefox/Profiles/'+profile+'/extensions')) + "\n"
									conn = None

									try:
										conn = sqlite3.connect(mount+"Users/"+user+"/Library/Application Support/Firefox/Profiles/"+profile+"/places.sqlite")

										cur = conn.cursor()
										cur.execute("SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch','localtime'), moz_places.url, moz_places.title, moz_places.rev_host FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id ORDER BY moz_historyvisits.visit_date ASC")

										rows = cur.fetchall()
										for row in rows:
											firefox_history += str(row) + "\n"
									except sqlite3.Error as e:
										print "Firefox Error: %s" % e
									finally:
										if conn:
											conn.close()
			elif isinstance(username, basestring):
				if os.path.isdir(mount+'Users/'+username+'/Library/Application Support/Firefox/Profiles/'):
					profiles = os.listdir(mount+'Users/'+username+'/Library/Application Support/Firefox/Profiles/')
					firefox_ext += username + "\n"
					firefox_history += user + "\n"
					for profile in profiles:
						if profile.startswith('.'):
							pass
						else:
							if os.path.isdir(mount+'Users/'+username+'/Library/Application Support/Firefox/Profiles/'+profile+'/extensions'):
								firefox_ext += str(os.listdir(mount+'Users/'+username+'/Library/Application Support/Firefox/Profiles/'+profile+'/extensions')) + "\n"
								conn = None

								try:
									conn = sqlite3.connect(mount+"Users/"+username+"/Library/Application Support/Firefox/Profiles/"+profile+"/places.sqlite")

									cur = conn.cursor()
									cur.execute("SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch','localtime'), moz_places.url, moz_places.title, moz_places.rev_host FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id ORDER BY moz_historyvisits.visit_date ASC")

									rows = cur.fetchall()
									for row in rows:
										firefox_history += str(row) + "\n"
								except sqlite3.Error as e:
									print "Firefox Error: %s" % e
								finally:
									if conn:
										conn.close()

		#List all Safari Extensions and History
	if os.path.isdir(mount+'Applications/Safari.app/'):
			safari_history = ''
			safari_ext = ''

			if isinstance(username, list):
				for user in username:
					if os.path.isdir(mount+'Users/'+user+'/Library/Safari/Extensions'):
						safari_ext += user + "\n"
						for file in os.listdir(mount+'Users/'+user+'/Library/Safari/Extensions'):
							if '.safariextz' in file:
								safari_ext += str(file) + "\n"
						conn = None

						try:
							conn = sqlite3.connect(mount+"Users/"+user+"/Library/Safari/History.db")

							cur = conn.cursor()
							cur.execute("SELECT datetime(history_visits.visit_time + 978307200,'unixepoch','localtime'), history_items.url, history_visits.title FROM history_visits, history_items WHERE history_items.id = history_visits.history_item ORDER BY history_visits.visit_time ASC")

							rows = cur.fetchall()
							safari_history += user + "\n"
							for row in rows:
								safari_history += str(row) + "\n"
						except sqlite3.Error as e:
							print "Safari Error: %s" % e
						finally:
							if conn:
								conn.close()
			elif isinstance(username, basestring):
				if os.path.isdir(mount+'Users/'+username+'/Library/Safari/Extensions'):
					safari_ext += username + "\n"
					for file in os.listdir(mount+'Users/'+username+'/Library/Safari/Extensions'):
						if '.safariextz' in file:
							safari_ext += str(file) + "\n"
					conn = None

					try:
						conn = sqlite3.connect(mount+"Users/"+username+"/Library/Safari/History.db")

						cur = conn.cursor()
						cur.execute("SELECT datetime(history_visits.visit_time + 978307200,'unixepoch','localtime'), history_items.url, history_visits.title FROM history_visits, history_items WHERE history_items.id = history_visits.history_item ORDER BY history_visits.visit_time ASC")

						rows = cur.fetchall()
						safari_history += username + "\n"
						for row in rows:
							safari_history += str(row) + "\n"
					except sqlite3.Error as e:
						print "Safari Error: %s" % e
					finally:
						if conn:
							conn.close()


	results = "Chrome Information\n"
	results += "--------------------\n"
	results += "Extensions:\n"
	results += chrome_ext
	results += "--------------------\n"
	results += "History:\n"
	results += chrome_history
	results += "--------------------\n\n"

	results += "Firefox Information\n"
	results += "--------------------\n"
	results += "Extensions:\n"
	results += firefox_ext
	results += "--------------------\n"
	results += "History:\n"
	results += firefox_history
	results += "--------------------\n\n"

	results += "Safari Information\n"
	results += "--------------------\n"
	results += "Extensions:\n"
	results += safari_ext
	results += "--------------------\n"
	results += "History:\n"
	results += safari_history
	results += "--------------------\n\n\n"

	return results



def get_downloaded_files(username, mount):
	downloads = ""
	if isinstance(username, list):
		for user in username:
			path = os.path.join(mount, "Users", user, "Library", "Preferences", "com.apple.LaunchServices.QuarantineEventsV2")
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

			downloads += "\n\n"
	elif isinstance(username, basestring):
		path = os.path.join(mount, "Users", username, "Library", "Preferences", "com.apple.LaunchServices.QuarantineEventsV2")
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

		downloads += "\n\n"

	return downloads


def get_emails(username, mount):
	emails = ''
	if isinstance(username, list):
		for user in username:
			rootdir = mount+"Users/"+user+"/Library/Mail"
			for subdir, dirs, files in os.walk(rootdir):
				for file in files:
					if "[Gmail]" in subdir:
						if ".emlx" in file:
							emails += "\n-------------------\n"
							emails += file
							with open(os.path.join(subdir, file), "r") as email:
								for line in email:
									match = re.compile('From: (.*)')
									email_from = match.match(line)
									if email_from:
										emails += email_from.group()
									else:
										pass
									match = re.compile('Date: (.*)')
									timestamp = match.match(line)
									if timestamp:
										emails += timestamp.group()
									match = re.compile('Subject: (.*)')
									subject = match.match(line)
									if subject:
										emails += subject.group()
	elif isinstance(username, basestring):
		rootdir = mount+"Users/"+username+"/Library/Mail"
		for subdir, dirs, files in os.walk(rootdir):
			for file in files:
				if "[Gmail]" in subdir:
					if ".emlx" in file:
						emails += "\n-------------------\n"
						emails += file
						with open(os.path.join(subdir, file), "r") as email:
							for line in email:
								match = re.compile('From: (.*)')
								email_from = match.match(line)
								if email_from:
									emails += email_from.group()
								else:
									pass
								match = re.compile('Date: (.*)')
								timestamp = match.match(line)
								if timestamp:
									emails += timestamp.group()
								match = re.compile('Subject: (.*)')
								subject = match.match(line)
								if subject:
									emails += subject.group()

	emails += "\n\n\n"
	return emails

def get_bash_history(username, mount):
	bash_history = ''
	if isinstance(username, list):
		for user in username:
			bash_history += subprocess.check_output(['cat', mount+'Users/'+username+'/.bash_history'])
			bash_history += "\n\n\n"
	elif isinstance(username, basestring):
		bash_history += subprocess.check_output(['cat', mount+'Users/'+username+'/.bash_history'])
		bash_history += "\n\n\n"
	return bash_history


if __name__ == '__main__':
	cfg = get_args()
	results = ''

	if cfg['browser']:
		results += "Browser Information\n"
		results += "------------------------------------\n"
		results += get_browser_info(cfg['username'], cfg['mount'])
		results += "\n------------------------------------\n\n"
	if cfg['disk']:
		results += "Disk and Partition Information\n"
		results += "------------------------------------\n"
		results += get_disks_partitions(cfg['username'], cfg['mount'])
		results += "\n------------------------------------\n\n"
	if cfg['emails']:
		results += "Email Information\n"
		results += "------------------------------------\n"
		results += get_emails(cfg['username'], cfg['mount'])
		results += "\n------------------------------------\n\n"
	if cfg['history']:
		results += "Bash History Log\n"
		results += "------------------------------------\n"
		results += get_bash_history(cfg['username'], cfg['mount'])
		results += "\n------------------------------------\n\n"
	if cfg['other']:
		results += "Basic Device Software and Hardware Information\n"
		results += "------------------------------------\n"
		results += get_basic_device_info()
		results += "\n------------------------------------\n\n"
	if cfg['startup']:
		results += "Startup Items Information\n"
		results += "------------------------------------\n"
		results += get_launch_start_items(cfg['username'], cfg['mount'])
		results += "\n------------------------------------\n\n"

	date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
	output_file = open("MAC_DFIR_Basics_Information_"+date+".txt", "w")
	output_file.write(results)
