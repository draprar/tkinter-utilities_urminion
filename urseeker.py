import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess

ascii_art = """
          _______  _______  _______  _______  _        _______  _______ 
|\     /|(  ____ )(  ____ \(  ____ \(  ____ \| \    /\(  ____ \(  ____ )
| )   ( || (    )|| (    \/| (    \/| (    \/|  \  / /| (    \/| (    )|
| |   | || (____)|| (_____ | (__    | (__    |  (_/ / | (__    | (____)|
| |   | ||     __)(_____  )|  __)   |  __)   |   _ (  |  __)   |     __)
| |   | || (\ (         ) || (      | (      |  ( \ \ | (      | (\ (   
| (___) || ) \ \__/\____) || (____/\| (____/\|  /  \ \| (____/\| ) \ \__
(_______)|/   \__/\_______)(_______/(_______/|_/    \/(_______/|/   \__/


"""


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.long_path_finder = None
        self.duplicate_finder = None
        self.title("UrSeeker")
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
        self.clear_screen()

        welcome_label = ttk.Label(self, text=ascii_art, font=("Courier", 10), justify=tk.LEFT)
        welcome_label.pack(pady=20)

        desc_label = ttk.Label(self, text="Wybierz jedną z poniższych funkcji:", style="Header.TLabel")
        desc_label.pack(pady=10)

        find_duplicates_button = ttk.Button(self, text="Znajdź duplikaty w katalogu",
                                            command=self.init_find_duplicates_screen)
        find_duplicates_button.pack(pady=10)

        find_long_paths_button = ttk.Button(self, text="Znajdź zbyt długie ścieżki plików/katalogów",
                                            command=self.init_find_long_paths_screen)
        find_long_paths_button.pack(pady=10)

        low_label = ttk.Label(self, text="Wszelkie uwagi proszę zgłaszać do: Michał", font=("Helvetica", 12))
        low_label.pack(pady=20)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def init_find_duplicates_screen(self):
        self.clear_screen()
        self.duplicate_finder = DuplicateFinder(self)
        self.duplicate_finder.pack(fill="both", expand=True)

    def init_find_long_paths_screen(self):
        self.clear_screen()
        self.long_path_finder = LongPathFinder(self)
        self.long_path_finder.pack(fill="both", expand=True)


def find_duplicates(directory):
    file_map = {}
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename in file_map:
                file_map[filename].append(os.path.join(dirpath, filename))
            else:
                file_map[filename] = [os.path.join(dirpath, filename)]

    duplicates = {name: paths for name, paths in file_map.items() if len(paths) > 1}
    return duplicates


class DuplicateFinder(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.frame = ttk.Frame(self)
        self.frame.pack(pady=20)

        self.open_button = ttk.Button(self.frame, text="Otwórz katalog", command=self.open_directory)
        self.open_button.pack(side=tk.LEFT, padx=10)

        self.start_button = ttk.Button(self.frame, text="Rozpocznij wyszukiwanie", command=self.start_search)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = ttk.Button(self.frame, text="Usuń zaznaczone", command=self.delete_selected)
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.open_selected_button = ttk.Button(self.frame, text="Otwórz katalog zaznaczonych",
                                               command=self.open_selected)
        self.open_selected_button.pack(side=tk.LEFT, padx=10)

        self.back_button = ttk.Button(self.frame, text="Wstecz", command=master.init_welcome_screen)
        self.back_button.pack(side=tk.LEFT, padx=10)

        self.lower_label = ttk.Label(self,
                                     text="Wyszukiwanie odbywa się po NAZWIE pliku, także radziłbym się upewnić "
                                          "przed usunięciem (: ", wraplength=1000, justify=tk.LEFT)
        self.lower_label.pack(pady=10)

        self.text_area_frame = ttk.Frame(self)
        self.text_area_frame.pack(pady=10)

        self.text_area_scroll = ttk.Scrollbar(self.text_area_frame, orient=tk.VERTICAL)
        self.text_area_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self.text_area_frame, selectmode=tk.EXTENDED,
                                  yscrollcommand=self.text_area_scroll.set, height=40, width=120, font=("Courier", 10))
        self.listbox.pack()

        self.text_area_scroll.config(command=self.listbox.yview)

        self.directory = ""
        self.duplicates = {}

    def open_directory(self):
        self.directory = filedialog.askdirectory()
        if self.directory:
            messagebox.showinfo("Katalog wybrany", f"Wybrany katalog: {self.directory}")

    def start_search(self):
        if not self.directory:
            messagebox.showwarning("Brak katalogu", "Proszę wybrać katalog najpierw.")
            return

        self.duplicates = find_duplicates(self.directory)
        if self.duplicates:
            self.listbox.delete(0, tk.END)
            self.listbox.insert(tk.END, "Duplikaty plików:\n")
            for name, paths in self.duplicates.items():
                self.listbox.insert(tk.END, f"\n{name}:\n")
                for path in paths:
                    self.listbox.insert(tk.END, path)
        else:
            messagebox.showinfo("Brak duplikatów", "Nie znaleziono duplikatów plików.")

    def delete_selected(self):
        selected_indices = self.listbox.curselection()
        selected_files = [self.listbox.get(i) for i in selected_indices if
                          not self.listbox.get(i).startswith("\n") and not self.listbox.get(i).startswith(
                              "Duplikaty plików:")]

        if not selected_files:
            messagebox.showwarning("Brak zaznaczenia", "Proszę zaznaczyć pliki do usunięcia.")
            return

        if messagebox.askyesno("Potwierdzenie usunięcia", "Czy na pewno chcesz usunąć zaznaczone pliki?"):
            for file_path in selected_files:
                try:
                    os.remove(file_path)
                    messagebox.showinfo("Usunięto", f"Plik usunięty: {file_path}")
                except Exception as e:
                    messagebox.showerror("Błąd", f"Nie udało się usunąć pliku: {e}")

            self.start_search()

    def open_selected(self):
        selected_indices = self.listbox.curselection()
        selected_files = [self.listbox.get(i) for i in selected_indices if
                          not self.listbox.get(i).startswith("\n") and not self.listbox.get(i).startswith(
                              "Duplikaty plików:")]

        if not selected_files:
            messagebox.showwarning("Brak zaznaczenia", "Proszę zaznaczyć pliki do otwarcia.")
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
                messagebox.showerror("Błąd", f"Nie udało się otworzyć katalogu: {e}")


class LongPathFinder(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.path_map = None
        self.frame = ttk.Frame(self)
        self.frame.pack(pady=20)

        self.open_button = ttk.Button(self.frame, text="Otwórz katalog", command=self.open_directory)
        self.open_button.pack(side=tk.LEFT, padx=10)

        self.start_button = ttk.Button(self.frame, text="Szukaj długich ścieżek", command=self.search_long_paths)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.open_selected_button = ttk.Button(self.frame, text="Otwórz ścieżkę", command=self.open_end_of_path)
        self.open_selected_button.pack(side=tk.LEFT, padx=10)

        self.back_button = ttk.Button(self.frame, text="Wstecz", command=master.init_welcome_screen)
        self.back_button.pack(side=tk.LEFT, padx=10)

        self.lower_label = ttk.Label(self,
                                     text="Jeżeli ścieżka jest za długa (>260) - trzeba będzie się wklikać dalej już "
                                          "z poziomu Eksploratora (:", wraplength=1000, justify=tk.LEFT)
        self.lower_label.pack(pady=10)

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
            messagebox.showinfo("Katalog wybrany", f"Wybrany katalog: {self.directory}")

    def search_long_paths(self):
        if not self.directory:
            messagebox.showwarning("Brak katalogu", "Proszę wybrać katalog najpierw.")
            return

        self.listbox.delete(0, tk.END)
        self.long_paths = []
        seen_paths = set()
        self.path_map = {}

        for root, dirs, files in os.walk(self.directory):
            for name in dirs + files:
                full_path = os.path.join(root, name)
                if len(full_path) > 260:
                    if not any(full_path.startswith(p) for p in seen_paths):
                        seen_paths.add(full_path)
                        display_entry = f"Długość: {len(full_path)} - {full_path}"
                        self.path_map[display_entry] = full_path
                        self.long_paths.append(full_path)
                        self.listbox.insert(tk.END, display_entry)

        if not self.long_paths:
            messagebox.showinfo("Brak długich ścieżek", "Nie znaleziono zbyt długich ścieżek.")

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
                    messagebox.showerror("Błąd", f"Nie udało się otworzyć katalogu: {e}")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
