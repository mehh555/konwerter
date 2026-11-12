import tkinter as tk
from tkinter import ttk


def card(parent, title):
    ttk.Label(parent, text=title, style="Section.TLabel").pack(anchor="w", pady=(0, 4))
    frame = ttk.Frame(parent, style="Card.TFrame", padding=12)
    frame.pack(fill="x", pady=(0, 12))
    return frame


class PathRow:
    def __init__(self, parent, title, command, what):
        self.what = what
        self.var = tk.StringVar()
        box = card(parent, title)
        ttk.Entry(box, textvariable=self.var, width=48, state="readonly").pack(side="left", fill="x", expand=True)
        self.button = ttk.Button(box, text=f"Wybierz {what}...", command=command)
        self.button.pack(side="left", padx=(8, 0))

    def get(self):
        return self.var.get()

    def set(self, value):
        self.var.set(value)
        self.button.config(text=f"Zmień {self.what}...")

    def enable(self, on):
        self.button.config(state="normal" if on else "disabled")