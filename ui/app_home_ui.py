import tkinter as tk
from tkinter import font
from utils.colors import (
    MAIN_BODY_COLOR, 
    TOP_BAR_COLOR, 
    SIDE_MENU_COLOR, 
    ON_CURSOR_MENU_COLOR
)
import utils.util_images as util_img
import utils.util_windows as util_window
from ui.app_emulator_ui import AppEmulatorUI
from ui.app_graph_ui import AppGraphUI
from ui.app_it7900_ui import IT7900App
from ui.app_it8600_ui import IT8600App
from ui.app_it6000C_ui import IT6000CApp


# Const
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 600
LOGO_PATH = "./assest/logo.png"
PROFILE_IMAGE_PATH = "./assest/Perfil.png"
ICON_PATH = "./assest/logo.ico"

class AppHomeUi(tk.Tk):

    def __init__(self):
        super().__init__()
        self.logo = util_img.load_image(LOGO_PATH, (560, 136))
        self.profile_image = util_img.load_image(PROFILE_IMAGE_PATH, (100, 100))
        self.setup_window()
        self.create_panels()
        self.setup_top_bar_controls()
        self.setup_sidebar_controls()
        self.setup_main_body_controls()

    def setup_window(self):
        """Configure the main window."""
        self.title("GIMEL CONTROL EMULADORES")
        #self.iconbitmap(ICON_PATH)
        util_window.center_window(self, WINDOW_WIDTH, WINDOW_HEIGHT)

    def create_panels(self):
        """Create the main panels: top bar, sidebar, and main body."""
        self.top_bar = tk.Frame(self, bg=TOP_BAR_COLOR, height=50)
        self.top_bar.pack(side=tk.TOP, fill="both")

        self.sidebar = tk.Frame(self, bg=SIDE_MENU_COLOR, width=150)
        self.sidebar.pack(side=tk.LEFT, fill="both", expand=False)

        self.main_body = tk.Frame(self, bg=MAIN_BODY_COLOR)
        self.main_body.pack(side=tk.RIGHT, fill="both", expand=True)    

    def setup_top_bar_controls(self):
        """Set up controls for the top bar."""
        font_awesome = font.Font(family="FontAwesome", size=12)

        # Title label
        self.label_title = tk.Label(
            self.top_bar,
            text="GIMEL",
            fg="#fff",
            font=("Roboto", 15),
            bg=TOP_BAR_COLOR,
            pady=10,
            width=16,
        )
        self.label_title.pack(side=tk.LEFT)

        # Sidebar toggle button
        self.button_sidebar_toggle = tk.Button(
            self.top_bar,
            text="\u2261",
            font=font_awesome,
            command=self.toggle_sidebar,
            bd=0,
            bg=TOP_BAR_COLOR,
            fg="white",
        )
        self.button_sidebar_toggle.pack(side=tk.LEFT)

        # Info label
        self.label_info = tk.Label(
            self.top_bar,
            text="omardbonett@gmail.com",
            fg="#fff",
            font=("Roboto", 10),
            bg=TOP_BAR_COLOR,
            padx=10,
            width=20,
        )
        self.label_info.pack(side=tk.RIGHT)       

    def setup_sidebar_controls(self):
        """Set up controls for the sidebar."""
        menu_width = 20
        menu_height = 2
        font_awesome = font.Font(family="FontAwesome", size=15)
        button_info = [
            ("Emulador AC\n IT7900", "\uf109", self.open_IT7900_panel),
            ("Emulador DC\n IT7900", "\uf007", self.open_IT6000C_panel),
            ("Emulador Carga\n IT8600", "\uf03e", self.open_IT8600_panel),
            ("Ayuda", "\uf129", self.open_under_construction_panel),
            ("Configuración", "\uf013", self.open_under_construction_panel),
        ]

        # Profile image label
        self.label_profile = tk.Label(
            self.sidebar, image=self.profile_image, bg=SIDE_MENU_COLOR
        )
        self.label_profile.pack(side=tk.TOP, pady=10)

                # Create buttons
        for text, icon, command in button_info:
            button = tk.Button(
                self.sidebar,
                text=f"  {icon}    {text}",
                anchor="w",
                font=font_awesome,
                bd=0,
                bg=SIDE_MENU_COLOR,
                fg="white",
                width=menu_width,
                height=menu_height,
                command=command,
            )
            button.pack(side=tk.TOP)
            self.bind_hover_events(button)

    def setup_main_body_controls(self):
        """Set up controls for the main body."""
        label = tk.Label(self.main_body, image=self.logo, bg=MAIN_BODY_COLOR)
        label.place(x=0, y=0, relwidth=1, relheight=1)

    def bind_hover_events(self, button):
        """Bind hover events to change button appearance."""
        button.bind("<Enter>", lambda event: button.config(bg=ON_CURSOR_MENU_COLOR))
        button.bind("<Leave>", lambda event: button.config(bg=SIDE_MENU_COLOR))

    def toggle_sidebar(self):
        """Toggle the visibility of the sidebar."""
        if self.sidebar.winfo_ismapped():
            self.sidebar.pack_forget()
        else:
            #self.sidebar.pack(side=tk.LEFT, fill="y")
            self.sidebar.pack(side=tk.LEFT, fill="both", expand=False)

    
    def open_IT7900_panel(self):
        """Open the graph panel."""
        self.clear_panel(self.main_body)
        IT7900App(self.main_body)
        
    def open_IT6000C_panel(self):
        """Open the graph panel."""
        self.clear_panel(self.main_body)
        IT6000CApp(self.main_body)
        

    def open_under_construction_panel(self):
        """Open the under construction panel."""
        self.clear_panel(self.main_body)
        AppGraphUI(self.main_body)

    def open_IT8600_panel(self):
        """Open the information panel."""
        self.clear_panel(self.main_body)
        IT8600App(self.main_body)

    def clear_panel(self, panel):
        """Clear the content of a given panel."""
        for widget in panel.winfo_children():
            widget.destroy()

    