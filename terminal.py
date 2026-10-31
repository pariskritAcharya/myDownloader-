import sys
import customtkinter as ctk
from app_constants import appColor


class TerminalPrinter:
    def __init__(self,textbox):
        self.textbox = textbox

    def write(self,text):
        self.textbox.configure(state="normal")
        self.textbox.insert("end",text)
        self.textbox.see("end") # scroll to the end
        self.textbox.configure(state="disabled")

    def flush(self):
        pass



class TerminalFrame(ctk.CTkFrame):
    def __init__(self, master,**kwargs):
        super().__init__(master=master,fg_color=appColor["red"],**kwargs)

        self.terminal_textbox = ctk.CTkTextbox(
            master=self,
            fg_color=appColor["cream"],
            text_color=appColor["black"],
            font=("Consolas", 14),
            scrollbar_button_color=appColor["red"],
            scrollbar_button_hover_color = appColor["pblack"]
            )
        self.terminal_textbox.pack(padx=10, pady=10,expand=True, fill="both")
        self.terminal_textbox.configure(state="disabled")
        sys.stdout = TerminalPrinter(self.terminal_textbox)
        print("Terminal")
        
