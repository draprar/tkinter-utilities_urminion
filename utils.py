def clear_screen(root):
    for widget in root.winfo_children():
        widget.destroy()
