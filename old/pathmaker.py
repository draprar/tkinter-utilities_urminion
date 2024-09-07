import os
import random
import string
import tkinter as tk
from tkinter import filedialog, messagebox


def generate_random_string(length=8):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def create_long_path(base_path, max_depth=10):
    current_path = base_path
    for depth in range(random.randint(1, max_depth)):
        dir_name = generate_random_string()
        current_path = os.path.join(current_path, dir_name)
        os.makedirs(current_path, exist_ok=True)
        file_name = generate_random_string() + '.txt'
        with open(os.path.join(current_path, file_name), 'w') as f:
            f.write(f"This is a file at depth {depth + 1} in directory {dir_name}.")
    with open(os.path.join(current_path, 'end.txt'), 'w') as f:
        f.write("This is the end of the nested directories.")
    return current_path


def select_base_path():
    path = filedialog.askdirectory()
    base_path_var.set(path)


def make_path():
    base_path = base_path_var.get()
    if not base_path:
        messagebox.showerror("Error", "Please select a base path.")
        return
    max_depth = int(depth_var.get())
    final_path = create_long_path(base_path, max_depth)
    messagebox.showinfo("Success", f"Final path created: {final_path}")


root = tk.Tk()
root.title("Long Path Generator")

base_path_var = tk.StringVar()
depth_var = tk.StringVar(value="10")

tk.Label(root, text="Base Path:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=base_path_var, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_base_path).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Max Depth:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=depth_var, width=10).grid(row=1, column=1, padx=10, pady=10)

tk.Button(root, text="Generate Path", command=make_path).grid(row=2, column=0, columnspan=3, pady=20)

root.mainloop()
