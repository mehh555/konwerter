import tkinter as tk
from pathlib import Path
from tkinter import ttk

from core import ConversionError, available_targets, convert, target_path, validate
from gui import dialogs, style
from gui.widgets import PathRow, card
from gui.worker import Worker

STATUS_STYLES = {"info": "Muted.TLabel", "ok": "Ok.TLabel", "error": "Error.TLabel"}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Konwerter plików")
        self.resizable(False, False)
        style.apply(self)
        self.worker = Worker(self, self.finished)

        page = ttk.Frame(self, padding=20)
        page.pack(fill="both", expand=True)

        header = ttk.Frame(page)
        header.pack(fill="x", pady=(0, 16))
        ttk.Label(header, text="Konwerter plików", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="CSV · JSON · TXT · DOCX · ODT · PDF", style="Muted.TLabel").pack(side="left")
        ttk.Button(header, text="Obsługiwane formaty", style="Link.TButton",
                   command=dialogs.show_formats).pack(side="right")

        self.source = PathRow(page, "Plik", self.pick_file, "plik")

        fmt_card = card(page, "Format")
        self.fmt = tk.StringVar()
        self.combo = ttk.Combobox(fmt_card, textvariable=self.fmt, state="disabled", width=10)
        self.combo.pack(side="left")
        self.combo.bind("<<ComboboxSelected>>", lambda _: self.set_status("Gotowe do konwersji."))
        self.preview = ttk.Label(fmt_card, style="CardMuted.TLabel")
        self.preview.pack(side="left", padx=12)

        self.out_dir = PathRow(page, "Zapisz w", self.pick_dir, "folder")

        self.go_btn = ttk.Button(page, text="Konwertuj", style="Accent.TButton", command=self.start, state="disabled")
        self.go_btn.pack(fill="x", pady=(6, 10))
        self.progress = ttk.Progressbar(page, mode="indeterminate")
        self.status = ttk.Label(page, wraplength=480)
        self.status.pack(fill="x")
        self.set_status("Wybierz plik do konwersji.")

        for var in (self.source.var, self.out_dir.var, self.fmt):
            var.trace_add("write", lambda *_: self.refresh())

    def set_status(self, text, kind="info"):
        self.status.config(text=text, style=STATUS_STYLES[kind])

    def refresh(self):
        ready = self.source.get() and self.out_dir.get() and self.fmt.get()
        self.go_btn.config(state="normal" if ready and not self.worker.busy else "disabled")

        if self.source.get() and self.fmt.get():
            target = target_path(Path(self.source.get()), self.fmt.get(), Path(self.out_dir.get()))
            note = "  (już istnieje)" if self.out_dir.get() and target.exists() else ""
            self.preview.config(text=f"→  {target.name}{note}")
        else:
            self.preview.config(text="")

    def pick_file(self):
        path = dialogs.ask_source()
        if not path:
            return
        path = Path(path)
        targets = [t.lstrip(".").upper() for t in available_targets(path)]
        self.source.set(path)
        self.combo.config(values=targets, state="readonly" if targets else "disabled")
        self.fmt.set(targets[0] if len(targets) == 1 else "")
        if not self.out_dir.get():
            self.out_dir.set(path.parent)

        if len(targets) == 1:
            self.set_status("Gotowe do konwersji.")
        elif targets:
            self.set_status("Wybierz format docelowy.")
        else:
            self.set_status(f"Brak konwersji dla plików {path.suffix or 'bez rozszerzenia'}. Wybierz inny plik.", "error")

    def pick_dir(self):
        path = dialogs.ask_dir()
        if path:
            self.out_dir.set(path)

    def start(self):
        source, fmt, out_dir = Path(self.source.get()), self.fmt.get(), Path(self.out_dir.get())
        try:
            validate(source, fmt, out_dir)
        except ConversionError as e:
            dialogs.show_error(str(e))
            return

        overwrite = False
        target = target_path(source, fmt, out_dir)
        if target.exists():
            overwrite = dialogs.ask_overwrite(target.name)
            if overwrite is None:
                return

        self.worker.start(convert, source, fmt, out_dir, overwrite)
        self.set_busy(True)

    def finished(self, result):
        self.set_busy(False)
        if isinstance(result, Exception):
            self.set_status(f"Błąd: {result}", "error")
            dialogs.show_error(str(result))
        else:
            self.set_status(f"Zapisano: {result}", "ok")
            dialogs.show_done(result)

    def set_busy(self, busy):
        self.source.enable(not busy)
        self.out_dir.enable(not busy)
        self.combo.config(state="disabled" if busy else "readonly")
        if busy:
            self.set_status("Konwertuję...")
            self.progress.pack(fill="x", pady=(0, 8), before=self.status)
            self.progress.start(10)
        else:
            self.progress.stop()
            self.progress.pack_forget()
        self.refresh()