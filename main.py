import os
import sys
import subprocess

from tabulate import tabulate

class Interface:
  def __init__(self) -> None:
    try:
      self.MainMenu()

    except KeyboardInterrupt:
        pass
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      self.MainMenu(error="{}".format(e))

  def MainMenu(self, error = None):
    try:
      subprocess.run(["clear"])

      if error:
        print(error)

      tools = [
        self.ChatRoom,
        self.MAC_Changer,
        self.ARPSpoof,
        self.ARPSpoofDetector,
        self.DNS_spoof,
        self.NetworkScanner,
        self.PacketSniffer,
      ]

      options = [
        [0, "Chat Room", "join chat rooms"],
        [1, "MAC changer", ""],
        [2, "ARP spoof", ""],
        [3, "ARP spoof detector", ""],
        [4, "DNS spoof", ""],
        [5, "network scanner", ""],
        [6, "packet sniffer", ""],
        # [7, "spider", "not ready"],
      ]

      col_names = ["#", "Tool Name", "Tool Description"]
      print("\n", tabulate(options, headers = col_names), "\n")

      user_input = input(f"({self.AppName}) > ")

      if user_input == "quit":
        return
      else:
        tools[int(user_input)]()

    except KeyboardInterrupt:
        pass
    except IndexError:
        self.MainMenu(error="sorry, option is not available")
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      self.MainMenu(error="{}".format(e))

  def ChatRoom(self):
    try:
      terminal_command = "gnome-terminal -- sudo python3 socket/client/ChatRoom.py"
      subprocess.Popen(terminal_command, shell=True)

      self.MainMenu()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      self.MainMenu(error="{}".format(e))
    
  def NetworkScanner(self):
    try:
      subprocess.run(["clear"])
      IP_Range = input("IP Range: ")

      sudo_command = f"gnome-terminal -- sudo python3 tools/networking/NetworkScanner.py -r {IP_Range}"
      subprocess.run(
        sudo_command,
        shell=True
      )

    except KeyboardInterrupt:
        self.MainMenu()
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      self.MainMenu(error="{}".format(e))

  def ARPSpoof(self):
    try:
      Target_IP = input("Target IP: ")
      Gateway_IP = input("Gateway IP: ")

      terminal_command = f"gnome-terminal -- sudo python3 arp_spoof.py -t {Target_IP} -s {Gateway_IP}"
      subprocess.Popen(
        terminal_command,
        shell = True
      )

      self.MainMenu()

    except KeyboardInterrupt:
      self.MainMenu()
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      self.MainMenu(error="{}".format(e))

  def ARPSpoofDetector(self): # fix
    try:
      terminal_command = "gnome-terminal -- sudo python3 arpspoof_detector.py"
      subprocess.Popen(
        terminal_command,
        shell=True
      )

      self.MainMenu()

    except KeyboardInterrupt:
        self.MainMenu()
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      self.MainMenu(error="{}".format(e))

  def DNS_spoof(self):
    try:
      pass

    except KeyboardInterrupt:
        self.lunch()
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      self.MainMenu(error="{}".format(e))

  def MAC_Changer(self): # fix
    try:
      inf = input("Interface: ")
      mac = input("MAC: ")

      sudo_command = f"gnome-terminal -- sudo python3 macchanger.py -i {inf} -m {mac}"
      subprocess.run(sudo_command, shell=True)

    except KeyboardInterrupt:
        self.MainMenu()
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      self.MainMenu(error="{}".format(e))

  def PacketSniffer(self): # fix
    try:
      subprocess.run(["clear"])
      self.current_tool = "MAC changer"

      inf = input("interface > ")

      sudo_command = f"gnome-terminal -- sudo python3 packet_sniffer.py -i {inf}"
      subprocess.run(sudo_command, shell=True)

    except KeyboardInterrupt:
        self.MainMenu()
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      self.MainMenu(error="{}".format(e))

if __name__ == '__main__':
  interface = Interface()
