# eminence
Targeting metasploitable 3

## About Eminence project
Eminence project is developed in python to test a few vulnerabilities available in
Metasploitable 3. It consist of scanners to scan network for available hosts as well as to
scan all open ports, vulnerabilities, system details, etc on specific host. Similarly, the project
includes SNMP-check module executed from system and the output is further analyzed by
python regex to gather important details from the enumeration. It can perform SSH brute
forcing to detect weak passwords and WinRM feature to execute arbitrary code in remote
system.

## About Metasploitable 3
Metasploitable3 is a free virtual machine that allows you to simulate attacks largely using
Metasploit. It has been used by people in the security industry for a variety of reasons: such
as training for network exploitation, exploit development, software testing, technical job
interviews, sales demonstrations, or CTF junkies who are looking for kicks, etc. Metasploit
consists of number of vulnerabilities both on OS side as well as program side.

## To run the project

### Install python3 and required libraries
> apt install python3

> pip3 install -r requirements.txt

### Run eminence.py
> python3 eminence.py

### Video Link:
https://youtu.be/NF19V_viFlA


## Reconnaissance
### python-nmap
python-nmap library let us perform nmap scan on system. The version of
python-nmap implemented is 0.6.1. It provides all the necessary functions to
produce hosts and ports scans. Besides we can perform vulnerability scan by using
nse scripts. The default nse script used in this scan is nmap-vulners. If system
couldn’t find the script, user can manually download and add their own script.
Netifaces module was used inorder to gather interfaces, ip address and netmask
automatically from host machine. Math module was use to calculate subnet mask
from netmask.

### SNMP-check
SNMP check enables gathering of various information of system. Since the machine
was intended to be vulnerable, lots of details could be extracted from the system.
The project runs system command to execute snmp check and implement regular
expression to gather important details from the output.

# Exploitation

## 1. SSH Brute Force

Paramiko module is use to create an ssh client by python. Then a dictionary attack
is implemented to detect password for users. If the dictionary attack fails, user can
then use other methods and set the password in program.

Port: 22

Access:
- Use an SSH client to connect and run commands remotely on the target

Start/Stop:
- Enabled by default

Vulnerabilities:
- Multiple users with weak passwords exist on the target. Those passwords
can be easily cracked. Once a session is opened, remote code can be
executed using SSH.

Modules:
- Paramiko
- Socket

## 2. WinRM:

Windows Remote Management (WinRM) is a feature of Windows Vista that allows
administrators to remotely run management scripts. It handles remote connections
by means of the WS-Management Protocol, which is based on SOAP (Simple Object
Access Protocol).
WinRM is use to run nc at victim machine. If nc is not available on system, nc is
downloaded from web using powershell Invoke-WebRequest and saved to
system32. Then nc is run at the victim pc while attacker pc listens to the specific port

Port: ​ 5958

Start/Stop:
- Stop: Open services.msc. Stop the Windows Remote Management service.
- Start: Open services.msc. Start the Windows Remote Management service.

Vulnerabilities:
- Multiple users with weak passwords exist on the target. Those passwords
can be easily cracked and WinRM can be used to run remote code on the
target.

Modules:
- wimrm

