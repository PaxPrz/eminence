import nmap
import netifaces as ni
import math
import sys
import os

class HostScanner:
    '''
    Scans for all available hosts
    HostScanner(ip='automatic scan if not given', subnet='24')
    '''
    def __init__(self, ip=0, subnet=0):
        self.ip = ip
        self.subnet = subnet
        if ip == 0 or subnet==0:
            MANUAL_ENTER=False
            interfaces = ni.interfaces()
            try:
                interfaces.remove('lo')
            except:
                pass
            for intf in interfaces:
                try:
                    self.ip = ni.ifaddresses(intf)[ni.AF_INET][0]['addr']
                    self.netmask = ni.ifaddresses(intf)[ni.AF_INET][0]['netmask']
                    self.intf = intf
                    print("Getting interface ", self.intf, "with \n\t IP: ", self.ip, "\n\t Netmask: ", self.netmask)
                    break
                except:
                    pass
            if self.ip == 0 or self.netmask == 0:
                print("Couldn't get ip and subnet automatically!!")
                MANUAL_ENTER = True
                self.manualEnter()
            if MANUAL_ENTER == False:
                octets = [int(i) for i in self.netmask.split('.')]
                for octet in octets:
                    self.subnet += int(8-math.log2(256-octet))
                print("\t Subnet: ", self.subnet)
        
    def manualEnter(self):
        self.ip = input("Enter IP address: ")
        self.subnet = input("Enter subnet mask: ")

    def scan(self, arguments=''):
        self.OS_DETECT=True
        print("Scanning network ", self.ip, "/", self.subnet, "\n\tArguments: ", arguments)
        self.nm = nmap.PortScanner()
        try:
            arguments = "-O"
            self.nm.scan(hosts=str(self.ip)+'/'+str(self.subnet), arguments=arguments)
        except Exception as e:
            self.OS_DETECT=False
            arguments = ""
            self.nm.scan(hosts=str(self.ip)+'/'+str(self.subnet), arguments=arguments)
        self.allHosts = self.nm.all_hosts()
    
    def showHosts(self):
        count = 1
        for host in self.allHosts:
            try:
                print("\n", count, ") Host: ", host)
                print("PORT \t STATE \t SERVICE")
                for port in list(self.nm[host]['tcp'].keys()):
                    print(port, "\t", self.nm[host]['tcp'][port]['state'], "\t", self.nm[host]['tcp'][port]['name'])
            except KeyError as k:
                print("Host: ", host, " is not available!!!")
                print("*** Try to do a rescan ***\n")
            count +=1



class PortScanner:
    '''
    Scan for ports in specific host
    PortScanner(ip='127.0.0.1', specificPort='80,443')
    '''
    def __init__(self, ip, specificPort=None):
        self.ip = ip
        self.specificPort = specificPort
    
    def scan(self, arguments='-sV'):
        print("Scanning")
        print("\t Host: ", self.ip)
        if self.specificPort!=None:
            print("\t Ports: ", self.specificPort)
        if arguments!="":
            print("\t arguments: ", arguments)
        self.nm = nmap.PortScanner()
        self.nm.scan(self.ip, ports=self.specificPort, arguments=arguments)
    
    def scanForVulnerability(self, port="80", arguments='-sV'):
        print("Scanning for vulnerabiility")
        if os.path.isfile('./nmap-vulners/vulners.nse'):
            arguments = '-sV --script=./nmap-vulners/vulners.nse'
        else:
            print("Nmap vulnerability database not found")
            nse_path = input("Enter path to nse file: ")
            arguments = '-sV --script='+nse_path
        try:
            vnm = nmap.PortScanner()
            vnm.scan(self.ip, ports=str(port), arguments=arguments)
        except Exception as e:
            print("Couldn't perform scan")
            print(e)
            return False
        self.showVulnerability(vnm)
        return True

    def showVulnerability(self, vnm):
        for port in list(vnm[self.ip]['tcp'].keys()):
            try:
                print("PORT: "+str(port)+"\t SERVICE: "+ vnm[self.ip]['tcp'][port]['name'])
                print("Vulnerabilities: ")
                print(vnm[self.ip]['tcp'][port]['script']['vulners'])
            except Exception as e:
                print("--- Cannot scan vulnerability ---")

    def showResult(self):
        try:
            print("PORT \t STATE \t PRODUCT \t SERVICE \t VERSION")
            for port in list(self.nm[self.ip]['tcp'].keys()):
                print(port, self.nm[self.ip]['tcp'][port]['state'], '\t', self.nm[self.ip]['tcp'][port]['product'], '\t', self.nm[self.ip]['tcp'][port]['name'], '\t', self.nm[self.ip]['tcp'][port]['version'])
        except KeyError as k:
            print("Host: ", self.ip, " is not available!!!")
            print("*** Try to scan available host ***\n")

def scanner_homepage():
    print('''
    ##### NMAP SCANNER #####
        Choose
        \t1. HostScanner
        \t2. PortScanner
        \t3. Exit
        ''')
    choice = input('> ')
    if choice=='1':
        print('''
        \t1. Manual IP
        \t2. Automatic
        ''')
        choice1 = input('>> ')
        hostscanner=None
        if choice1=='1':
            ip = input("Enter IP address: ")
            subnet = input("Enter subnet mask: ")
            hostscanner = HostScanner(ip, subnet)
        elif choice1=='2':
            hostscanner = HostScanner()
        else:
            print("Invalid option!")
            sys.exit()
        hostscanner.scan()
        hostscanner.showHosts()
        while 1:
            try:
                i=int(input("Select Host by id: "))
                if i>len(hostscanner.allHosts):
                    raise(Exception())
                break
            except Exception as e:
                pass
        # Here vulnerability scanner
        vulscanChoice = input("Do you want to perform PortScan and vulnerability scan (y/N): ")
        if vulscanChoice=='y':
            specificPort = input("Enter specific port (80,111,443,...): ")
            if specificPort=='':
                portscanner = PortScanner(hostscanner.allHosts[i-1])
            else:
                portscanner = PortScanner(hostscanner.allHosts[i-1], specificPort=specificPort)
            portscanner.scan()
            portscanner.showResult()
            doVulScan(portscanner)
        return hostscanner.ip, hostscanner.allHosts[i-1]
    
    elif choice=='2':
        ip = input("Enter IP address: ")
        specificPort = input("Enter specific port (80,111,443,...): ")
        portscanner=None
        if specificPort=='':
            portscanner = PortScanner(ip)
        else:
            portscanner = PortScanner(ip, specificPort=specificPort)
        portscanner.scan()
        portscanner.showResult()
        # Here vulnerability scanner
        vulscanChoice = input("Do you want to scan for vulnerability (y/N): ")
        if vulscanChoice=='y':
            doVulScan(portscanner)
        return False, portscanner.ip
    
    else:
        return False, False


def doVulScan(ps):
    ports = input("\nEnter ports for vulnerability scan (22,80,...): ")
    vulScanResult = ps.scanForVulnerability(ports)
    print("\n\n")

if __name__=="__main__":
    scanner_homepage()