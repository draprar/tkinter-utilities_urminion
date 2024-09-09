import os
import hashlib
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess


def get_file_hash(file_path, hash_algorithm='sha256'):
    try:
        hash_func = hashlib.new(hash_algorithm)
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        print(f"Could not hash file {file_path}: {e}")
        return None


def find_duplicates(directory):
    file_hash_map = {}
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_hash = get_file_hash(file_path)

            if file_hash:
                if file_hash in file_hash_map:
                    file_hash_map[file_hash].append(file_path)
                else:
                    file_hash_map[file_hash] = [file_path]

    duplicates = {hash_value: paths for hash_value, paths in file_hash_map.items() if len(paths) > 1}
    return duplicates


class DuplicateFinder(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.directory = ""
        self.duplicates = {}

        self.frame = ttk.Frame(self)
        self.frame.pack(pady=20)

        self.open_button = ttk.Button(self.frame, text="Open directory", command=self.open_directory)
        self.open_button.pack(side=tk.LEFT, padx=10)

        self.start_button = ttk.Button(self.frame, text="Start search", command=self.start_search)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = ttk.Button(self.frame, text="Delete selected", command=self.delete_selected)
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.open_selected_button = ttk.Button(self.frame, text="Open selected directory", command=self.open_selected)
        self.open_selected_button.pack(side=tk.LEFT, padx=10)

        self.back_button = ttk.Button(self.frame, text="Back", command=master.init_welcome_screen)
        self.back_button.pack(side=tk.LEFT, padx=10)

        self.lower_label = ttk.Label(self, text="The search is done by FILE CONTENT (hash comparison). Please double-check before deletion!", wraplength=1000, justify=tk.LEFT)
        self.lower_label.pack(pady=10)

        self.text_area_frame = ttk.Frame(self)
        self.text_area_frame.pack(pady=10)

        self.text_area_scroll = ttk.Scrollbar(self.text_area_frame, orient=tk.VERTICAL)
        self.text_area_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self.text_area_frame, selectmode=tk.EXTENDED, yscrollcommand=self.text_area_scroll.set, height=40, width=120, font=("Courier", 10))
        self.listbox.pack()

        self.text_area_scroll.config(command=self.listbox.yview)

    def open_directory(self):
        self.directory = filedialog.askdirectory()
        if self.directory:
            messagebox.showinfo("Directory selected", f"Selected directory: {self.directory}")

    def start_search(self):
        if not self.directory:
            messagebox.showwarning("No directory", "Please select a directory first.")
            return

        self.duplicates = find_duplicates(self.directory)
        if self.duplicates:
            self.listbox.delete(0, tk.END)
            self.listbox.insert(tk.END, "Duplicate files:\n")
            for file_hash, paths in self.duplicates.items():
                self.listbox.insert(tk.END, f"\nHash: {file_hash}\n")
                for path in paths:
                    self.listbox.insert(tk.END, path)
        else:
            messagebox.showinfo("No duplicates", "No duplicate files found.")

    def delete_selected(self):
        selected_indices = self.listbox.curselection()
        selected_files = [self.listbox.get(i) for i in selected_indices if not self.listbox.get(i).startswith("\n") and not self.listbox.get(i).startswith("Duplicate files:")]

        if not selected_files:
            messagebox.showwarning("No selection", "Please select files to delete.")
            return

        if messagebox.askyesno("Delete confirmation", "Are you sure you want to delete the selected files?"):
            for file_path in selected_files:
                try:
                    os.remove(file_path)
                    messagebox.showinfo("Deleted", f"File deleted: {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete file: {e}")

            self.start_search()

    def open_selected(self):
        selected_indices = self.listbox.curselection()
        selected_files = [self.listbox.get(i) for i in selected_indices if not self.listbox.get(i).startswith("\n") and not self.listbox.get(i).startswith("Duplicate files:")]

        if not selected_files:
            messagebox.showwarning("No selection", "Please select files to open.")
            return

        for file_path in selected_files:
            try:
                directory = os.path.dirname(file_path)
                if os.name == 'nt':
                    os.startfile(os.path.normpath(directory))
                elif os.name == 'posix':
                    subprocess.call(('open', os.path.normpath(directory)))
                else:
                    subprocess.call(('xdg-open', os.path.normpath(directory)))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open directory: {e}")
