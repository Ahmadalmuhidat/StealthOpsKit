import os
import sys
import socket
import ssl
import warnings
import json
import struct

# Filter out DeprecationWarning messages
warnings.filterwarnings("ignore", category = DeprecationWarning)

class Client:
  def __init__(self):
    try:
      self.host = None
      self.port = None

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def ConnectToServer(self):
    try:
      self.ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      # self.SecuredSocket = ssl.wrap_socket(self.ClientSocket)
      self.ClientSocket.connect((self.host, self.port))

    except ssl.SSLError as e:
      print(f"SSL error: {e}")
      pass
    except socket.error as e:
      print(f"Socket error: {e}")
      pass
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def GetMessageJson(self):
    try:
      size_data = self.ClientSocket.recv(struct.calcsize("i"))
      size = struct.unpack("i", size_data)[0]
      data = b""
  
      while len(data) < size:
        message = self.ClientSocket.recv(size - len(data))

        if not message:
          continue

        data += message
        result = json.loads(data.decode('utf-8'))

        return result

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def SendMessageJson(self, Message, RoomID):
    try:
      data = json.dumps({
        "Code": 1,
        "Message": Message,
        "RoomID": RoomID,
        "Error": None
      }).encode('utf8')

      self.ClientSocket.send(struct.pack("i", len(data)) + data)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def CreateChatRoom(self, RoomID):
    try:
      order = "create"
      self.SendMessageJson(order, RoomID)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def JoinCharRoom(self, RoomID):
    try:
      order = "join"
      self.SendMessageJson(order, RoomID)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def Cleanup(self):
    try:
      if self.ClientSocket:
        self.ClientSocket.close()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass