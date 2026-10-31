import customtkinter as ctk
from app_constants import appColor , appSettings

from queue_handler import enqueue
from mobile_transfer_usb import push_files_to_android
import wifi_transfer
from file_manager import get_settings





class InputUrl(ctk.CTkFrame):
    def __init__(self, master ,**kwargs):
        super().__init__(
                            master=master,
                            fg_color=appColor["red"],
                            bg_color="transparent",
                            corner_radius=100,
                            **kwargs
                        )
        #constants and vars 


        #search bar
        self.searchBar = ctk.CTkEntry(
                                    master = self,
                                    placeholder_text="Enter url of video / audio".capitalize(),
                                    fg_color= appColor["red"],
                                    text_color=appColor["pblack"],
                                    placeholder_text_color=appColor["black"],
                                    font=("Consolas", 16),
                                    corner_radius=20,
                                    border_color= appColor["red"],
                                    
                                 )
        self.searchBar.pack(pady=5,padx = (30,10), expand=True ,side= "left" , fill = "both")

        

        #button attached 
        self.enter_button = ctk.CTkButton(
                                            master=self,
                                            text="Enter",
                                            width=15,
                                            text_color=appColor["black"],
                                            font=("Consolas", 16),
                                            fg_color="transparent",
                                            hover_color=appColor["red"],
                                            command=self.master.send_input
                                        )
        self.searchBar.bind("<Return>", self.master.send_input)
        self.enter_button.pack(side="left", padx=(0, 30),pady=5, fill="y")

    def get_inputURL(self, event=None):
        url =  self.searchBar.get()
        self.searchBar.delete(0,"end")
        self.searchBar.focus()
        print(url)
        return url
    

class InputFrame(ctk.CTkFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master=master,**kwargs)
    
        #variables/ logic
        self.selectedOption = "video"
        self.downloadNum = 1


    
        # UI elements

        ## input url
        self.input_url = InputUrl(master=self)
        self.input_url.place(relx = .2, rely=.40, relwidth = .70 , relheight= .09)
        

        #input Top Frame
        self.buttonFrame = ctk.CTkFrame(master=self, fg_color="transparent")
        
        # number input 
        self.entry_Number = ctk.StringVar()
        self.entry_Number.trace_add("write", self.validate_number)
        self.number_input =ctk.CTkEntry(
                                            master=self.buttonFrame,
                                            text_color=appColor["pblack"],
                                            font=("Consolas", 16),
                                            fg_color=appColor["cream"],
                                            border_color=appColor["red"], 
                                            border_width=3,
                                            justify = "center",
                                            width=30,
                                            textvariable=self.entry_Number,
                                        )
        self.entry_Number.set("1")
        
        self.number_input.pack(side = "left" , padx = 10 , pady=5)

        ## buttons
        
        self.video_button = ctk.CTkButton(
                                            master=self.buttonFrame,
                                            text="Video",
                                            text_color=appColor["pblack"],
                                            font=("Consolas", 16),
                                            fg_color=appColor["red"],
                                            hover_color=appColor["yellow"],
                                            corner_radius=30,
                                            height=40,
                                            command= self.vbutton_clicked,
                                        )
        self.video_button.pack(side = "left", padx = 10)
        self.audio_button = ctk.CTkButton(
                                            master=self.buttonFrame,
                                            text="Audio",
                                            text_color=appColor["pblack"],
                                            font=("Consolas", 16),
                                            fg_color=appColor["grey"],
                                            hover_color=appColor["yellow"],
                                            corner_radius=30,
                                            height=40,
                                            command= self.abutton_clicked
                                        )
        self.audio_button.pack(side = "left", padx=10)
        self.buttonFrame.place(relx = .35, rely=.30, relwidth = .40 , relheight= .1)
    def vbutton_clicked(self):
        self.selectedOption = "video"
        self.video_button.configure(fg_color = appColor["red"])
        self.audio_button.configure(fg_color = appColor["grey"])

    def abutton_clicked(self):
        self.selectedOption = "audio" 
        self.video_button.configure(fg_color = appColor["grey"])
        self.audio_button.configure(fg_color = appColor["red"])

    def validate_number(self, var_name, index, mode):
            current_text = self.entry_Number.get()
            MAX_DOWNLOAD = appSettings["MAX_DOWNLOAD"]
            if current_text == "":
                return
            if not current_text.isdigit():
                # Revert the box to the last known valid number
                self.entry_Number.set(str(self.downloadNum))
                return

            number = int(current_text)
            if number <= 0:
                self.entry_Number.set("1")
                self.downloadNum = 1
            if number > MAX_DOWNLOAD:
                self.entry_Number.set(str(MAX_DOWNLOAD))
                self.downloadNum = MAX_DOWNLOAD
            else:
                self.downloadNum = number

    def send_input(self,event=None):
        enqueue(self.input_url.get_inputURL(),self.selectedOption , self.downloadNum)











#################################################################3

#left frame 

class LeftFrame(ctk.CTkFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master=master,
                         fg_color=appColor["cream"],
                         corner_radius=0,
                         **kwargs
                         )
        self.input_frame = InputFrame(master=self, fg_color ="transparent")
        self.input_frame.place(relx = 0, rely= 0, relwidth = 1, relheight= 1)

        self.usb_transfer_button = ctk.CTkButton(master= self , text="USB Transfer" , command=push_files_to_android)
        self.usb_transfer_button.place(relx = 0.6 ,rely = 0.01 , relwidth  = 0.1 , relheight= 0.04 )

        self.wifi_transfer_button = ctk.CTkButton(master= self , text="wifi Transfer" , command=self.show_qr_popup)
        self.wifi_transfer_button.place(relx = 0.75 ,rely = 0.01 , relwidth  = 0.1 , relheight= 0.04 )
        
        


    # Attach this to your button's command parameter: command=self.show_qr_popup
    def show_qr_popup(self):
        settings = get_settings()
        download_folder = settings["local_downloadFolder"]

        # 1. Start server and get the RGB image
        qr_pil_image = wifi_transfer.get_qr_image_and_start_server(download_folder)
        
        # 2. SAVE TO SELF: Prevent Python from deleting the image from memory
        self.qr_ctk_image = ctk.CTkImage(light_image=qr_pil_image, dark_image=qr_pil_image, size=(250, 250))
        
        # 3. Create the popup window
        popup = ctk.CTkToplevel(self)
        popup.title("Wi-Fi Transfer")
        popup.geometry("350x400")
        popup.attributes("-topmost", True)
        
        # 4. Display the QR code using the saved self variable
        qr_label = ctk.CTkLabel(popup, text="", image=self.qr_ctk_image)
        qr_label.pack(pady=20)
        
        instruction_label = ctk.CTkLabel(popup, text="1. Connect phone to same Wi-Fi\n2. Scan with camera to download", font=("Arial", 14))
        instruction_label.pack(pady=10)