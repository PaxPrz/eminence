import os
import subprocess
import re

class SNMPCheck:
	def __init__(self, ip):
		self.ip = ip

	def check_snmp_check(self):
		result = os.system("snmp-check")
		if result != 0:
			print("system doesn't have snmp-check")
			return False
		else:
			output = subprocess.check_output(["snmp-check", self.ip])
			self.snmpOutput = output.decode()
			return True

	def show_snmp_result(self):
		if self.snmpOutput:
			print(self.snmpOutput)
		else:
			print("No snmpOutput generated")

	def printAllUsers(self):
		for user in self.allUsers:
			print(user)

	def find_username(self):
		if self.snmpOutput:
			self.username=None
			hostname_regex = 'Hostname[\s]*:[\s]*([\w]*)-.*'
			try:
				self.username = re.search(hostname_regex, self.snmpOutput).group(1)
			except Exception as e:
				print("No hostname found from username")
			self.allUsers=[]
			allusers_regex = 'User accounts:[\s]*([.\s\S]*?)(?=\[)'
			try:
				users = re.search(allusers_regex, self.snmpOutput).group(1)
				self.allUsers = [x.strip() for x in users.splitlines()]
			except Exception as e:
				print("Cannot find any users")
			if isinstance(self.username, str) and self.username in self.allUsers:
				return self.username
			else:
				print("Try from these hostnames")
				for user in self.allUsers:
					print(user)
				return False
		else:
			print("Begin check_snmp_check first")
			return False


