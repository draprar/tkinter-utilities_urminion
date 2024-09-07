import os
import tkinter as tk
from tkinter import ttk
from utils import clear_screen
from duplicate_finder import DuplicateFinder
from long_path_finder import LongPathFinder
from secret_key_generator import SecretKeyGenerator

ascii_art = """
  _    _      __  __ _       _             
 | |  | |    |  \/  (_)     (_)            
 | |  | |_ __| \  / |_ _ __  _  ___  _ __  
 | |  | | '__| |\/| | | '_ \| |/ _ \| '_ \ 
 | |__| | |  | |  | | | | | | | (_) | | | |
  \____/|_|  |_|  |_|_|_| |_|_|\___/|_| |_|

"""


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.long_path_finder = None
        self.duplicate_finder = None
        self.secret_key_generator = None
        self.title("UrMinion")
        self.geometry("1024x768")
        self.icon_path = os.path.join(os.path.dirname(__file__), "favicon.ico")
        self.iconbitmap(self.icon_path)
        self.init_styles()
        self.init_welcome_screen()

    @staticmethod
    def init_styles():
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10)
        style.configure("TLabel", font=("Helvetica", 14))
        style.configure("Header.TLabel", font=("Helvetica", 16, "bold"))

    def init_welcome_screen(self):
        clear_screen(self)

        welcome_label = ttk.Label(self, text=ascii_art, font=("Courier", 10), justify=tk.LEFT)
        welcome_label.pack(pady=20)

        desc_label = ttk.Label(self, text="Select one of the options below:", style="Header.TLabel")
        desc_label.pack(pady=10)

        find_duplicates_button = ttk.Button(self, text="Find duplicates in directory",
                                            command=self.init_find_duplicates_screen)
        find_duplicates_button.pack(pady=10)

        find_long_paths_button = ttk.Button(self, text="Find too long file/directory paths",
                                            command=self.init_find_long_paths_screen)
        find_long_paths_button.pack(pady=10)

        generate_secret_key_button = ttk.Button(self, text="Generate password/secret key",
                                                command=self.init_secret_key_generator_screen)
        generate_secret_key_button.pack(pady=10)

        low_label = ttk.Label(self, text="", font=("Helvetica", 12))
        low_label.pack(pady=20)

    def init_find_duplicates_screen(self):
        clear_screen(self)
        self.duplicate_finder = DuplicateFinder(self)
        self.duplicate_finder.pack(fill="both", expand=True)

    def init_find_long_paths_screen(self):
        clear_screen(self)
        self.long_path_finder = LongPathFinder(self)
        self.long_path_finder.pack(fill="both", expand=True)

    def init_secret_key_generator_screen(self):
        clear_screen(self)
        self.secret_key_generator = SecretKeyGenerator(self)
        self.secret_key_generator.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
