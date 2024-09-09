import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess


class LongPathFinder(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.path_map = None
        self.default_long_path_length = 260
        self.long_path_length = self.default_long_path_length

        self.frame = ttk.Frame(self)
        self.frame.pack(pady=20)

        self.open_button = ttk.Button(self.frame, text="Open Directory", command=self.open_directory)
        self.open_button.pack(side=tk.LEFT, padx=10)

        self.start_button = ttk.Button(self.frame, text="Search for Long Paths", command=self.search_long_paths)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.open_selected_button = ttk.Button(self.frame, text="Open Path", command=self.open_end_of_path)
        self.open_selected_button.pack(side=tk.LEFT, padx=10)

        self.back_button = ttk.Button(self.frame, text="Back", command=master.init_welcome_screen)
        self.back_button.pack(side=tk.LEFT, padx=10)

        self.length_label = ttk.Label(self.frame, text='Set long path length (default: 260)', wraplength=1000, justify=tk.LEFT)
        self.length_label.pack(padx=10)

        self.length_entry = ttk.Entry(self.frame)
        self.length_entry.insert(0, str(self.default_long_path_length))
        self.length_entry.pack(side=tk.LEFT, padx=10)

        self.text_area_frame = ttk.Frame(self)
        self.text_area_frame.pack(pady=10)

        self.text_area_scroll = ttk.Scrollbar(self.text_area_frame, orient=tk.VERTICAL)
        self.text_area_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self.text_area_frame, selectmode=tk.EXTENDED,
                                  yscrollcommand=self.text_area_scroll.set, height=40, width=120, font=("Courier", 10))
        self.listbox.pack()

        self.text_area_scroll.config(command=self.listbox.yview)

        self.directory = ""
        self.long_paths = []

    def open_directory(self):
        self.directory = filedialog.askdirectory()
        if self.directory:
            messagebox.showinfo("Directory Selected", f"Selected directory: {self.directory}")

    def search_long_paths(self):
        if not self.directory:
            messagebox.showwarning("No Directory", "Please select a directory first.")
            return

        try:
            self.long_path_length = int(self.length_entry.get())
        except ValueError:
            messagebox.showwarning("Invalid input", f"Please enter a valid number for the long path length.")
            return

        self.listbox.delete(0, tk.END)
        self.long_paths = []
        seen_paths = set()
        self.path_map = {}

        for root, dirs, files in os.walk(self.directory):
            for name in dirs + files:
                full_path = os.path.join(root, name)
                if len(full_path) > self.long_path_length:
                    if not any(full_path.startswith(p) for p in seen_paths):
                        seen_paths.add(full_path)
                        display_entry = f"Length: {len(full_path)} - {full_path}"
                        self.path_map[display_entry] = full_path
                        self.long_paths.append(full_path)
                        self.listbox.insert(tk.END, display_entry)

        if not self.long_paths:
            messagebox.showinfo("No Long Paths", "No long paths were found.")

    def open_end_of_path(self):
        selected_entries = [self.listbox.get(i) for i in self.listbox.curselection()]
        for entry in selected_entries:
            file = self.path_map.get(entry)
            if file:
                try:
                    directory = os.path.dirname(file)
                    if os.name == 'nt':
                        os.startfile(os.path.normpath(directory))
                    elif os.name == 'posix':
                        subprocess.call(('open', os.path.normpath(directory)))
                    else:
                        subprocess.call(('xdg-open', os.path.normpath(directory)))
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to open directory: {e}")
