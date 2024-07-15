import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

class DuplicateFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Duplicate Finder")

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        self.open_button = tk.Button(self.frame, text="Open Directory", command=self.open_directory)
        self.open_button.pack(side=tk.LEFT, padx=10)

        self.start_button = tk.Button(self.frame, text="Start Search", command=self.start_search)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(self.frame, text="Delete Selected", command=self.delete_selected)
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.open_button = tk.Button(self.frame, text="Open Directory of Selected", command=self.open_selected)
        self.open_button.pack(side=tk.LEFT, padx=10)

        self.label = tk.Label(self.root, text="Open Directory => Start Search => Open Directory of Selected OR Delete Selected")
        self.label.pack(pady=10)

        self.text_area_frame = tk.Frame(self.root)
        self.text_area_frame.pack(pady=10)

        self.text_area_scroll = tk.Scrollbar(self.text_area_frame, orient=tk.VERTICAL)
        self.text_area_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self.text_area_frame, selectmode=tk.EXTENDED, yscrollcommand=self.text_area_scroll.set, height=20, width=80)
        self.listbox.pack()

        self.text_area_scroll.config(command=self.listbox.yview)

        self.label = tk.Label(self.root, text="Author: MW")
        self.label.pack(pady=10)

        self.directory = ""
        self.duplicates = {}

    def open_directory(self):
        self.directory = filedialog.askdirectory()
        if self.directory:
            messagebox.showinfo("Directory Selected", f"Selected directory: {self.directory}")

    def start_search(self):
        if not self.directory:
            messagebox.showwarning("No Directory", "Please select a directory first.")
            return

        self.duplicates = self.find_duplicates(self.directory)
        if self.duplicates:
            self.listbox.delete(0, tk.END)
            self.listbox.insert(tk.END, "Duplicate Files:\n")
            for name, paths in self.duplicates.items():
                self.listbox.insert(tk.END, f"\n{name}:\n")
                for path in paths:
                    self.listbox.insert(tk.END, f"{path}")
        else:
            messagebox.showinfo("No Duplicates", "No duplicate files found.")

    def find_duplicates(self, directory):
        file_map = {}
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                if filename in file_map:
                    file_map[filename].append(os.path.join(dirpath, filename))
                else:
                    file_map[filename] = [os.path.join(dirpath, filename)]

        duplicates = {name: paths for name, paths in file_map.items() if len(paths) > 1}
        return duplicates

    def delete_selected(self):
        selected_indices = self.listbox.curselection()
        selected_files = [self.listbox.get(i) for i in selected_indices if not self.listbox.get(i).startswith("\n") and not self.listbox.get(i).startswith("Duplicate Files:")]

        if not selected_files:
            messagebox.showwarning("No Selection", "Please select the file path to delete.")
            return

        if messagebox.askyesno("Delete Confirmation", f"Are you sure you want to delete the selected files?"):
            for file_path in selected_files:
                try:
                    os.remove(file_path)
                    messagebox.showinfo("Deleted", f"File deleted: {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete file: {e}")

            self.start_search()

    def open_selected(self):
        selected_indices = self.listbox.curselection()
        selected_files = [self.listbox.get(i) for i in selected_indices if not self.listbox.get(i).startswith("\n") and not self.listbox.get(i).startswith("Duplicate Files:")]

        if not selected_files:
            messagebox.showwarning("No Selection", "Please select the file path to open.")
            return

        for file_path in selected_files:
            try:
                directory = os.path.dirname(file_path)
                if os.name == 'nt':
                    os.startfile(directory)
                elif os.name == 'posix':
                    subprocess.call(('open', directory))
                else:
                    subprocess.call(('xdg-open', directory))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open directory: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DuplicateFinder(root)
    root.mainloop()
