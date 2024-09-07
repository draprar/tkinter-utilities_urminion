import secrets
import string
import tkinter as tk
from tkinter import ttk, messagebox


class SecretKeyGenerator(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.frame = ttk.Frame(self)
        self.frame.pack(pady=20)

        self.label = ttk.Label(self.frame, text="Enter number of characters:")
        self.label.pack(side=tk.LEFT, padx=10)

        self.length_var = tk.StringVar(value="32")
        self.entry = ttk.Entry(self.frame, textvariable=self.length_var)
        self.entry.pack(side=tk.LEFT, padx=10)

        self.generate_button = ttk.Button(self.frame, text="Generate and Copy", command=self.generate_secret_key)
        self.generate_button.pack(side=tk.LEFT, padx=10)

        self.back_button = ttk.Button(self.frame, text="Back", command=master.init_welcome_screen)
        self.back_button.pack(side=tk.LEFT, padx=10)

        self.text_area_frame = ttk.Frame(self)
        self.text_area_frame.pack(pady=10)

        self.text_area_scroll = ttk.Scrollbar(self.text_area_frame, orient=tk.VERTICAL)
        self.text_area_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area = tk.Text(self.text_area_frame, yscrollcommand=self.text_area_scroll.set, height=30, width=100,
                                 font=("Courier", 10))
        self.text_area.pack()

        self.text_area_scroll.config(command=self.text_area.yview)

    def generate_secret_key(self):
        try:
            length = int(self.length_var.get())
            if length <= 0:
                raise ValueError("Number of characters must be greater than zero.")

            alphabet = string.ascii_letters + string.digits + string.punctuation
            secret_key = ''.join(secrets.choice(alphabet) for _ in range(length))
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, secret_key)
            self.copy_to_clipboard(secret_key)
            messagebox.showinfo("Secret Key", "Generated key copied to clipboard.")
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid value: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {e}")

    def copy_to_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()
