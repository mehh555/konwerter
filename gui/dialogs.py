from tkinter import filedialog, messagebox

from core import REGISTRY


def ask_source():
    exts = " ".join(sorted({"*" + src for src, _ in REGISTRY}))
    return filedialog.askopenfilename(filetypes=[("Obsługiwane pliki", exts), ("Wszystkie pliki", "*.*")])


def ask_dir():
    return filedialog.askdirectory()


def ask_overwrite(name):
    return messagebox.askyesnocancel(
        "Plik istnieje",
        f"{name} już istnieje.\n\nTak – nadpisz\nNie – zapisz pod nową nazwą\nAnuluj – przerwij",
    )


def show_formats():
    pairs = "\n".join(f"{src}  →  {dst}" for src, dst in sorted(REGISTRY))
    messagebox.showinfo("Obsługiwane formaty", pairs)


def show_error(message):
    messagebox.showerror("Błąd", message)


def show_done(path):
    messagebox.showinfo("Gotowe", f"Zapisano plik:\n{path}")