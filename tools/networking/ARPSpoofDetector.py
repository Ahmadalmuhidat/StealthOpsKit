#!/usr/bin/python2
#put the script in startup folder to run when the system boots
#put in /etc/init.d/script.py make executable sudo chmod 755 /etc/init.d/scipt.py
#Register script to be run at startup sudo update-rc.d superscript defaults

import os
import sys
import scapy.all as scapy

class ARPSpoofDetector:
  def getmac(self, ip):
    try:
      arp_request_header = scapy.ARP(pdst = ip)
      ether_header = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
      arp_request_packet = ether_header / arp_request_header

      answered_list = scapy.srp(
        arp_request_packet,
        timeout = 1,
        verbose = False
	  )[0]

      return answered_list[0][1].hwsrc

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def sniff(self, interface):
    try:
      print("start sniffing")
      scapy.sniff(
        iface = interface,
        store = False,
        prn = self.process_sniffed_packet
      )

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def process_sniffed_packet(self, packet):
    try:
      if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        real_mac = getmac(packet[scapy.ARP].psrc)
        response_mac = packet[scapy.ARP].hwsrc

        if real_mac != response_mac:
          print("[+] You are under attack !!")

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

if __name__ == "__main__":
  p = ARPSpoofDetector()
  p.sniff("enp0s3")
