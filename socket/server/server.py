import os
import sys
import socket
import threading
import ssl
import warnings
import atexit
import json
import struct

# Filter out DeprecationWarning messages
warnings.filterwarnings("ignore", category = DeprecationWarning)

class ChatRoom:
  def __init__(self, id):
    try:
      self.id = id
      self.clients = []

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def AddClient(self, client):
    try:
      self.clients.append(client)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def RemoveClient(self, client):
    try:
      self.clients.remove(client)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def NotifyUsers(self, message):
    try:
      notification = "[Server] " + message
      for client in self.clients:
        data = json.dumps({
          "Code": 2,
          "Message": notification,
          "Error": None
        }).encode('utf-8')

        client.send(struct.pack("i", len(data)) + data)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

class Server:
  def __init__(self, host, port, certfile, keyfile):
    try:
      self.host = host
      self.port = port
      self.certfile = certfile
      self.keyfile = keyfile
      self.ChatRooms = {}
      self.lock = threading.Lock()

      self.StartListening()
      self.AcceptConnection()

      atexit.register(self.CleanUp)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def StartListening(self):
    try:
      self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.server_socket.bind((self.host, self.port))
      self.server_socket.listen(5)
      print("Server is listening...")

    except Exception as e:
      print("Server error:", e)
      pass

  def AcceptConnection(self):
    try:
      while True:
        ClientSocket, ClientAddress = self.server_socket.accept()
        print("Connection established with:", ClientAddress)

        # client = ssl.wrap_socket(
        #   ClientSocket,
        #   server_side = True,
        #   certfile = self.certfile,
        #   keyfile = self.keyfile
        # )

        while True:
          size_data = ClientSocket.recv(struct.calcsize("i"))

          if not size_data:
            print("Client disconnected")
            break
          
          size = struct.unpack("i", size_data)[0]
          data = b""

          while len(data) < size:
            message = ClientSocket.recv(size - len(data))

            if not message:
              continue
            data += message

          test = json.loads(data.decode('utf-8'))

          message = test.get("Message")
          RoomID = test.get("RoomID")

          if message == "create":
            self.CreateChatRoom(RoomID, ClientSocket)
          elif message == "join":
            self.JoinChatRoom(RoomID, ClientSocket)
          else:
            self.broadcast(message, RoomID)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass
    except KeyboardInterrupt:
      print("Server shutting down...")

      for chat_id in self.ChatRooms:
        for client in self.ChatRooms[chat_id].clients:
          client.close()
      print("All sockets have been terminated")

  def SendMessageJson(self, message, code, ClientSocket):
    try:
      data = json.dumps({
        "Code": code,
        "Message": message,
        "Error": None
      }).encode('utf-8')

      ClientSocket.send(struct.pack("i", len(data)) + data)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def CreateChatRoom(self, chatID, ClientSocket):
    try:
      if chatID not in self.ChatRooms:
        self.ChatRooms[chatID] = ChatRoom(chatID)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass
        
  def JoinChatRoom(self, chatID, ClientSocket):
    try:
      if chatID in self.ChatRooms:
        with self.lock:
          self.ChatRooms[chatID].AddClient(ClientSocket)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def broadcast(self, message, ChatID):
    try:
      if ChatID not in self.ChatRooms:
        return

      with self.lock:
        for ClientSocket in self.ChatRooms[ChatID].clients:
          self.SendMessageJson(
            message,
            1,
            ClientSocket
          )

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass
    
  def RemoveClient(self, client, chatID):
    try:
      with self.lock:
        self.ChatRooms[chatID].RemoveClient(client)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def CleanUp(self):
    try:
      if self.server_socket:
        self.server_socket.close()
        print("Cleaning up.")

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

if __name__ == '__main__':
  try:
    host = "0.0.0.0"
    port = 1234
    server_private_key = "server_private_key.pem"
    server_certificate = "server_certificate.pem"
    server = Server(
      host,
      port,
      server_certificate,
      server_private_key
    )

  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    print(exc_obj)
    pass