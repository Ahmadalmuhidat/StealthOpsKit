import os
import sys
import customtkinter
import socket
import atexit
import threading

from client import Client

class ChatRoom(Client):
  def __init__(
    self,
    RoomID,
    OrderType,
    host,
    port
  ) -> None:
    try:
      super().__init__()

      self.RoomID = RoomID
      self.Username = "ahmad"
      self.host = host
      self.port = port

      self.CloseThreads = False

      self.threads = []

      self.ConnectToServer()

      atexit.register(self.Cleanup)

      if OrderType == "join":
        self.JoinCharRoom(RoomID)
      else:
        self.CreateChatRoom(RoomID)
        self.JoinCharRoom(RoomID)

      threading.Thread(target = self.ReceiveMessages).start()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def SubmitMessage(self):
    try:
      message = f"{self.Username}> {self.entry.get()}"
      self.SendMessage(message)
      self.entry.delete(0, customtkinter.END)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def ReceiveMessages(self):
    try:
      while True:
        if self.CloseThreads:
          break

        message = self.GetMessageJson().get("Message") + "\n\n"
        self.MessagesBox.configure(state="normal")
        self.MessagesBox.insert(customtkinter.END, message)
        self.MessagesBox.configure(state="disabled")

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def SendMessage(self, message):
    try:
      if not message:
        return

      if message.strip() != "":
        self.SendMessageJson(message, self.RoomID)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass
  
  def OnClosing(self):
    try:
      self.CloseThreads = True

      self.window.destroy()
      sys.exit(0)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def StartTheProgram(self):
    try:
      customtkinter.set_appearance_mode("dark")

      self.window = customtkinter.CTk()

      self.window.geometry("800x750")
      self.window.resizable(
        width = 0,
        height = 0
      )

      self.window.title(f"Room ID: {self.RoomID}")

      self.window.protocol(
        "WM_DELETE_WINDOW",
        self.OnClosing
      )

      self.MessagesBox = customtkinter.CTkTextbox(
        self.window,
        state='disabled',
        width=750,
        height=600
      )
      self.MessagesBox.pack(pady = 10)

      self.entry = customtkinter.CTkEntry(
        self.window,
        width = 750,
        height = 50
      )
      self.entry.pack(pady = 10)

      SubmitButton = customtkinter.CTkButton(
        self.window,
        width = 750,
        text = "Submit",
        command = self.SubmitMessage
      )
      SubmitButton.pack(pady = 10)

      self.window.mainloop()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
    except KeyboardInterrupt:
      pass

if __name__ ==  "__main__":
  IndividualsFaceDetector = ChatRoom(
    1,
    "create",
    socket.gethostname(),
    1234
  )
  IndividualsFaceDetector.StartTheProgram()