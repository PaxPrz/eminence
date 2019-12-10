import nmap
import netifaces as ni
import math
import sys

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
                manualEnter()
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
        return False, portscanner.ip
    
    else:
        return False, False


if __name__=="__main__":
    scanner_homepage()