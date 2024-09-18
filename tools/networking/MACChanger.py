#!/usr/bin/python2.7

import os
import sys
import subprocess
import optparse
import re

class MAC_Changer:
  def __init__(self) -> None:
    try:
      self.interface = None
      self.NewAddress = None

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def ReadArguments(self):
    tryt:
      parser = optparse.ArgumentParser()
      parser.add_option(
        "-i",
        "--interface",
        dest = "interface",
        help = "Interface to change the mac address"
      )
      parser.add_option(
        "-m",
        "--mac",
        dest = "new_mac",
        help = "add new mac address"
      )

      options = parser.parse_args()

      if not options.interface:
        parser.error("[-] Specify an Interface use python macchanger --help for more details")
      elif not options.new_mac:
        parser.error("[-] Specify an MacAddr use python macchanger --help for more details")

      self.interface = options.interface
      self.NewAddress = options.new_mac

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def macchanger(self):
    try:
      subprocess.call(["ifconfig", self.interface, "down"])
      subprocess.call(["ifconfig", self.interface, "hw", "ether", self.NewAddress])
      subprocess.call(["ifconfig", self.interface, "up"])

      print(f"[+] Changing Mac Address of Interface {interface} to {macaddr}")

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def getmac(self):
    try:
      ifconfig_result = subprocess.check_output(["ifconfig", self.interface])
      current_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

      if current_mac:
        return current_mac.group(0)
      else:
        return None

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

if __name__ == "__main__":
  p = MAC_Changer()
  p.ReadArguments()
  # option gets the value of interface and mac returned by get_argument function

  p.macchanger()
  # main program which change the mac address

  final_mac = getmac()
  # verify whether the mac is changed or Not

  if final_mac == options.new_mac:
    print("Mac Address Successfully Chaged with new one %r"%final_mac)
  else:
    print("Error Occured Fix It")
