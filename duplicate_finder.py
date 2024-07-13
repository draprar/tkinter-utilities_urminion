import os
import tkinter as tk
from tkinter import filedialog, messagebox


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

        self.text_area = tk.Text(self.root, height=20, width=80)
        self.text_area.pack(pady=10)

        self.directory = ""

    def open_directory(self):
        self.directory = filedialog.askdirectory()
        if self.directory:
            messagebox.showinfo("Directory Selected", f"Selected directory: {self.directory}")

    def start_search(self):
        if not self.directory:
            messagebox.showwarning("No Directory", "Please select a directory first.")
            return

        duplicates = self.find_duplicates(self.directory)
        if duplicates:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, "Duplicate Files:\n")
            for name, paths in duplicates.items():
                self.text_area.insert(tk.END, f"\n{name}:\n")
                for path in paths:
                    self.text_area.insert(tk.END, f"{path}\n")
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


if __name__ == "__main__":
    root = tk.Tk()
    app = DuplicateFinder(root)
    root.mainloop()
