import customtkinter
import os
from PIL import Image
from frames.frame1 import MyFrame1
from frames.frame2 import MyFrame2
from frames.frame3 import MyFrame3
from frames.frame4 import MyFrame4
from frames.frame5 import MyFrame5
from frames.home import Home


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Project GUI")
        self.geometry("900x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(30, 30))
        
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(30, 30))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(30, 30))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(30, 30))
        
        self.so_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark_so.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "light_so.png")), size=(30, 30))
        
        self.predict_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark_predict.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "light_predict.png")), size=(30, 30))
        self.automate_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dark_automate.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "light_automate.png")), size=(30, 30))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(7, weight=1)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="new")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Elasticsearch Alerts",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="new")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Security Onion Machine",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.so_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="new")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Prediction Panel",
                                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                        image=self.predict_image, anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="new")

        self.frame_5_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Automation Panel",
                                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                        image=self.automate_image, anchor="w", command=self.frame_5_button_event)
        self.frame_5_button.grid(row=5, column=0, sticky="new")


        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=7, column=0, padx=20, pady=20, sticky="s")

        # create Home frame
        self.home_frame = Home(self, corner_radius=0, fg_color="transparent")

        # create first frame
        self.second_frame = MyFrame1(self, corner_radius=0, fg_color="transparent")

        # create second frame
        self.third_frame = MyFrame2(self, corner_radius=0, fg_color="transparent")
        
        # create third frame
        self.fourth_frame = MyFrame3(self, corner_radius=0, fg_color="transparent")

        # create fourth frame
        self.fifth_frame = MyFrame4(self, corner_radius=0, fg_color="transparent")

        # create fifth frame
        #self.sixth_frame = MyFrame5(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")
        self.frame_5_button.configure(fg_color=("gray75", "gray25") if name == "frame_5" else "transparent")
        #self.frame_6_button.configure(fg_color=("gray75", "gray25") if name == "frame_6" else "transparent")


        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()
        if name == "frame_5":
            self.fifth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fifth_frame.grid_forget()
        #if name == "frame_6":
        #    self.sixth_frame.grid(row=0, column=1, sticky="nsew")
        #else:
        #    self.sixth_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")
    
    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    def frame_5_button_event(self):
        self.select_frame_by_name("frame_5")

    #def frame_6_button_event(self):
    #    self.select_frame_by_name("frame_6")
        
    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()


