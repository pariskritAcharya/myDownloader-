import customtkinter as ctk
import app_constants as color
from file_manager import get_queue









class RightFrame(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master=master,fg_color=color.appColor["red"],corner_radius=0)
        
