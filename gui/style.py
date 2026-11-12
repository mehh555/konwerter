from tkinter import ttk

BG = "#f3f4f6"
CARD = "#ffffff"
BORDER = "#e5e7eb"
TEXT = "#111827"
MUTED = "#6b7280"
ACCENT = "#2563eb"
ACCENT_HOVER = "#1d4ed8"
ACCENT_OFF = "#a5b4fc"
OK = "#15803d"
ERROR = "#b91c1c"
FONT = "Segoe UI"


def apply(root):
    root.configure(bg=BG)
    s = ttk.Style(root)
    s.theme_use("clam")

    s.configure(".", background=BG, foreground=TEXT, font=(FONT, 10))
    s.configure("Title.TLabel", font=(FONT, 18, "bold"))
    s.configure("Muted.TLabel", foreground=MUTED)
    s.configure("Ok.TLabel", foreground=OK)
    s.configure("Error.TLabel", foreground=ERROR)

    s.configure("Section.TLabel", font=(FONT, 10, "bold"))
    s.configure("Card.TFrame", background=CARD, bordercolor=BORDER, relief="solid", borderwidth=1)
    s.configure("CardMuted.TLabel", background=CARD, foreground=MUTED)

    s.configure("TButton", padding=(12, 5), background=CARD, bordercolor=BORDER)
    s.map("TButton", background=[("active", BG)])
    s.configure("Link.TButton", background=BG, foreground=ACCENT, borderwidth=0, padding=(4, 2))
    s.map("Link.TButton", background=[("active", BG)], foreground=[("active", ACCENT_HOVER)])

    s.configure("Accent.TButton", background=ACCENT, foreground="white", borderwidth=0,
                font=(FONT, 11, "bold"), padding=(20, 10))
    s.map("Accent.TButton", background=[("disabled", ACCENT_OFF), ("active", ACCENT_HOVER)],
          foreground=[("disabled", "white")])

    s.configure("TEntry", fieldbackground=BG, bordercolor=BORDER, padding=5)
    s.map("TEntry", fieldbackground=[("readonly", BG)])
    s.configure("TCombobox", fieldbackground=CARD, bordercolor=BORDER, padding=5)
    s.map("TCombobox", fieldbackground=[("readonly", CARD), ("disabled", BG)])

    s.configure("TProgressbar", troughcolor=BORDER, background=ACCENT, bordercolor=BORDER,
                lightcolor=ACCENT, darkcolor=ACCENT, thickness=6)