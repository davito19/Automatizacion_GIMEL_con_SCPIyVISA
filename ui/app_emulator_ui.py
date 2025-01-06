import tkinter as tk
import utils.util_windows as util_window

class AppEmulatorUI(tk.Toplevel):
    """
    A class representing the information window design.

    This window displays the version and author information.
    """

    def __init__(self) -> None:
        super().__init__()
        self.configure_window()
        self.build_widgets()

    def configure_window(self) -> None:
        """Configure the initial settings of the window."""
        self.title("GIMEL CONTROL EMULADORES")
        #self.iconbitmap("./imagenes/logo.ico")
        window_width, window_height = 400, 100
        util_window.center_window(self, window_width, window_height)

    def build_widgets(self) -> None:
        """Build and pack the widgets for the information window."""
        VERSION_TEXT = "Version : 1.0"
        AUTHOR_TEXT = "Author : David Bonett"

        # Version label
        version_label = tk.Label(self, text=VERSION_TEXT)
        version_label.config(
            fg="#000000", font=("Roboto", 15), pady=10, width=20
        )
        version_label.pack()

        # Author label
        author_label = tk.Label(self, text=AUTHOR_TEXT)
        author_label.config(
            fg="#000000", font=("Roboto", 15), pady=10, width=20
        )
        author_label.pack()
