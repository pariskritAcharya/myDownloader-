import customtkinter as ctk 
from app_constants import appColor
import json


from file_manager import QUEUE_FILE
from left_frame import LeftFrame
from right_frame import RightFrame
from terminal import TerminalFrame
from queue_handler import run_background_worker , download_queue
from file_manager import get_queue

class Mydownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.configure(fg_color =appColor["cream"])
        self.title("My Downloader")
        self.geometry("1280x720")

        # self.update_idletasks()
        # app_width = self.winfo_width()
        # app_height = self.winfo_height()


        self.leftFrame = LeftFrame(master=self)
        self.leftFrame.place(relx=0.0, rely=0.0, relwidth=0.7, relheight=1.0)
      

        self.rightFrame = RightFrame(master=self)
        self.rightFrame.place(relx=0.7, rely=0.0, relwidth=0.3, relheight=1.0)

        self.terminalFrame = TerminalFrame(master=self.leftFrame)
        self.terminalFrame.place(relx=0.05,rely=0.8, relwidth = 0.9, relheight = 0.2)
        






if __name__ == "__main__":


    #run background worker 
    queue_data = get_queue()
    for data in queue_data:
        download_queue.put(data)


    run_background_worker()

    #start app UI
    app = Mydownloader()
    app.mainloop()