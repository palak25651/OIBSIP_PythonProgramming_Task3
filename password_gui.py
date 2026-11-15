"""Advanced tier: tkinter password generator using the secrets module.

Features: length slider + spinbox, character-type checkboxes, guaranteed one
character per selected type, strength indicator, exclude ambiguous characters,
auto-copy to clipboard (pyperclip), in-memory history of the last 5 passwords.
"""
import math
import secrets
import string
import tkinter as tk
from collections import deque
from tkinter import ttk

try:
    import pyperclip
except ImportError:  # fall back to tkinter's own clipboard if pyperclip is missing
    pyperclip = None

MIN_LENGTH, MAX_LENGTH = 8, 64
AMBIGUOUS = set("0O1lI|")
HISTORY_SIZE = 5


def build_pools(upper, lower, digits, symbols, exclude_ambiguous):
    """Return a list of character pools, one per selected type."""
    raw = []
    if upper:
        raw.append(string.ascii_uppercase)
    if lower:
        raw.append(string.ascii_lowercase)
    if digits:
        raw.append(string.digits)
    if symbols:
        raw.append(string.punctuation)
    if exclude_ambiguous:
        raw = ["".join(c for c in pool if c not in AMBIGUOUS) for pool in raw]
    return raw


def generate_password(length, pools):
    """Cryptographically secure password with >=1 char from every pool."""
    if length < MIN_LENGTH:
        raise ValueError(f"Length must be at least {MIN_LENGTH}.")
    if len(pools) < 2:
        raise ValueError("Select at least 2 character types.")
    chars = [secrets.choice(pool) for pool in pools]
    everything = "".join(pools)
    chars += [secrets.choice(everything) for _ in range(length - len(chars))]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def strength(password):
    """Return (label, fraction 0-1) from estimated entropy and diversity."""
    pool_size = 0
    if any(c.islower() for c in password):
        pool_size += 26
    if any(c.isupper() for c in password):
        pool_size += 26
    if any(c.isdigit() for c in password):
        pool_size += 10
    if any(c in string.punctuation for c in password):
        pool_size += 32
    bits = len(password) * math.log2(pool_size) if pool_size else 0
    if bits < 50:
        label = "Weak"
    elif bits < 80:
        label = "Medium"
    else:
        label = "Strong"
    return label, min(bits / 110, 1.0)


class App(tk.Tk):
    COLORS = {"Weak": "#d9534f", "Medium": "#f0ad4e", "Strong": "#5cb85c"}

    def __init__(self):
        super().__init__()
        self.title("Password Generator")
        self.resizable(False, False)
        self.history = deque(maxlen=HISTORY_SIZE)

        self.length = tk.IntVar(value=16)
        self.upper = tk.BooleanVar(value=True)
        self.lower = tk.BooleanVar(value=True)
        self.digits = tk.BooleanVar(value=True)
        self.symbols = tk.BooleanVar(value=True)
        self.no_ambiguous = tk.BooleanVar(value=False)
        self.password = tk.StringVar()
        self.status = tk.StringVar()

        self._build_ui()
        self.generate()

    def _build_ui(self):
        pad = {"padx": 12, "pady": 6}
        frm = ttk.Frame(self, padding=8)
        frm.grid()

        # Length controls (slider + spinbox share one variable)
        ttk.Label(frm, text="Length").grid(row=0, column=0, sticky="w", **pad)
        ttk.Scale(frm, from_=MIN_LENGTH, to=MAX_LENGTH, orient="horizontal", length=200,
                  command=lambda v: self.length.set(round(float(v)))).grid(row=0, column=1, **pad)
        ttk.Spinbox(frm, from_=MIN_LENGTH, to=MAX_LENGTH, width=5,
                    textvariable=self.length).grid(row=0, column=2, **pad)

        # Character types
        box = ttk.LabelFrame(frm, text="Character types (pick at least 2)")
        box.grid(row=1, column=0, columnspan=3, sticky="ew", **pad)
        for text, var in [("Uppercase (A-Z)", self.upper), ("Lowercase (a-z)", self.lower),
                          ("Numbers (0-9)", self.digits), ("Symbols (!@#...)", self.symbols)]:
            ttk.Checkbutton(box, text=text, variable=var).pack(anchor="w", padx=8, pady=2)
        ttk.Checkbutton(frm, text="Exclude ambiguous characters (0 O l 1 I |)",
                        variable=self.no_ambiguous).grid(row=2, column=0, columnspan=3,
                                                        sticky="w", **pad)

        # Output
        ttk.Entry(frm, textvariable=self.password, font=("Courier", 13), width=34,
                  state="readonly").grid(row=3, column=0, columnspan=3, **pad)

        self.bar = ttk.Progressbar(frm, length=300, maximum=100)
        self.bar.grid(row=4, column=0, columnspan=2, sticky="w", **pad)
        self.strength_label = tk.Label(frm, text="", width=8, fg="white")
        self.strength_label.grid(row=4, column=2, **pad)

        buttons = ttk.Frame(frm)
        buttons.grid(row=5, column=0, columnspan=3, **pad)
        ttk.Button(buttons, text="Generate", command=self.generate).pack(side="left", padx=4)
        ttk.Button(buttons, text="Copy to Clipboard", command=self.copy).pack(side="left", padx=4)

        ttk.Label(frm, textvariable=self.status, foreground="#555").grid(
            row=6, column=0, columnspan=3, **pad)

        hist = ttk.LabelFrame(frm, text=f"Last {HISTORY_SIZE} passwords (this session only)")
        hist.grid(row=7, column=0, columnspan=3, sticky="ew", **pad)
        self.history_box = tk.Listbox(hist, height=HISTORY_SIZE, font=("Courier", 11), width=42)
        self.history_box.pack(padx=6, pady=6)

    def copy(self):
        pw = self.password.get()
        if not pw:
            return
        if pyperclip:
            try:
                pyperclip.copy(pw)
                return True
            except pyperclip.PyperclipException:
                pass
        self.clipboard_clear()  # fallback
        self.clipboard_append(pw)
        return True

    def generate(self):
        try:
            length = int(self.length.get())
        except (tk.TclError, ValueError):
            self.status.set("Length must be a whole number.")
            return
        if not MIN_LENGTH <= length <= MAX_LENGTH:
            self.status.set(f"Length must be between {MIN_LENGTH} and {MAX_LENGTH}.")
            return
        pools = build_pools(self.upper.get(), self.lower.get(), self.digits.get(),
                            self.symbols.get(), self.no_ambiguous.get())
        if len(pools) < 2:
            self.status.set("Select at least 2 character types.")
            return

        pw = generate_password(length, pools)
        self.password.set(pw)
        self.history.appendleft(pw)
        self.history_box.delete(0, "end")
        for item in self.history:
            self.history_box.insert("end", item)

        label, frac = strength(pw)
        self.bar["value"] = frac * 100
        self.strength_label.config(text=label, bg=self.COLORS[label])
        self.copy()
        self.status.set("Generated and copied to clipboard.")


if __name__ == "__main__":
    App().mainloop()
