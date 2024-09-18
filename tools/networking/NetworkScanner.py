import os
import sys
import argparse

import scapy.all as scapy 

class NetworkScanner:
  def __init__(self) -> None:
    try:
      self.clients_list = []
      self.range = None

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def ReadArguments(self):
    try:
      parser = argparse.ArgumentParser()
      parser.add_argument(
        "-r",
        "--range",
        dest = "ipadrr",
        help = "Specify an IP Address or a range of IP Address"
      )
      options = parser.parse_args()

      if not options.ipadrr:
        parser.error("[-] Specify an IP Address or a range of IP Address --help for more details")

      self.range = options.ipadrr

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def ScanTarget(self):
    try:
      arp_header = scapy.ARP(pdst = self.range.ipadrr)
      ether_header = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
      arp_request_packet = ether_header / arp_header
      answered_list = scapy.srp(
	    arp_request_packet,
        timeout = 1
      )[0]
	
      for elements in answered_list:
        client_dict = {
          "ip": elements[1].psrc,
          "mac": elements[1].hwsrc
        }

      self.clients_list.append(client_dict)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def DisplayResults(self):
    try:
      print("IP Adress", "\t\t", "Mac Address")
      print("------------------------------------------")

      for client in self.clients_list:
        print(client['ip'], "\t\t", client['mac'])

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

if __name__ == "__main__":
  Network_Scanner = NetworkScanner()
  Network_Scanner.ReadArguments()
  Network_Scanner.ScanTarget()
  Network_Scanner.DisplayResults()

  input("\ndone scanning") # prevent terminal auto close
