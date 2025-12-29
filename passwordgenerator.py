import customtkinter as ctk
import secrets
import string
import math
import tkinter as tk
from tkinter import messagebox

# ================= LOGIC =================

def generate_password(length, u, l, d, s):
    pools = []
    password = []

    if u:
        pools.append(string.ascii_uppercase)
        password.append(secrets.choice(string.ascii_uppercase))
    if l:
        pools.append(string.ascii_lowercase)
        password.append(secrets.choice(string.ascii_lowercase))
    if d:
        pools.append(string.digits)
        password.append(secrets.choice(string.digits))
    if s:
        pools.append(string.punctuation)
        password.append(secrets.choice(string.punctuation))

    if not pools:
        raise ValueError("Select at least one character type.")

    if length < len(password):
        raise ValueError(f"Length must be at least {len(password)}")

    all_chars = "".join(pools)

    for _ in range(length - len(password)):
        password.append(secrets.choice(all_chars))

    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def estimate_strength(length, u, l, d, s):
    charset = 0
    if u: charset += 26
    if l: charset += 26
    if d: charset += 10
    if s: charset += len(string.punctuation)

    entropy = length * math.log2(charset) if charset else 0

    if entropy < 40: return 1, "Very Weak"
    elif entropy < 60: return 2, "Weak"
    elif entropy < 80: return 3, "Medium"
    elif entropy < 100: return 4, "Strong"
    else: return 5, "Very Strong"


# ================= UI =================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class PasswordApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Secure Password Generator")
        self.geometry("500x700")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="🔒", font=("Arial", 60)).pack(pady=(20, 0))
        ctk.CTkLabel(self, text="Secure Password Generator",
                     font=("Arial", 24, "bold")).pack(pady=10)

        # ===== Length =====
        self.length = ctk.IntVar(value=16)
        self.length.trace_add("write", self.update_strength)

        card1 = ctk.CTkFrame(self, corner_radius=15)
        card1.pack(fill="x", padx=30, pady=15)

        ctk.CTkLabel(card1, text="Password Length",
                     font=("Arial", 16, "bold")).pack(pady=10)

        ctk.CTkSlider(card1, from_=8, to=64,
                      variable=self.length).pack(fill="x", padx=20)

        ctk.CTkLabel(card1, textvariable=self.length,
                     font=("Arial", 20)).pack(pady=10)

        # ===== Options =====
        self.upper = ctk.BooleanVar(value=True)
        self.lower = ctk.BooleanVar(value=True)
        self.digit = ctk.BooleanVar(value=True)
        self.special = ctk.BooleanVar(value=True)

        card2 = ctk.CTkFrame(self, corner_radius=15)
        card2.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(card2, text="Character Types",
                     font=("Arial", 16, "bold")).pack(pady=10)

        for text, var in [
            ("Uppercase (A-Z)", self.upper),
            ("Lowercase (a-z)", self.lower),
            ("Digits (0-9)", self.digit),
            ("Special (!@#$)", self.special)
        ]:
            ctk.CTkCheckBox(card2, text=text,
                            variable=var,
                           command=self.update_strength).pack(anchor="w", padx=20, pady=5)
        # ===== Generate =====
        ctk.CTkButton(self, text="Generate Password",
                      height=45,
                      font=("Arial", 16, "bold"),
                      command=self.generate).pack(fill="x", padx=40, pady=20)

        # ===== Output =====
        self.password = tk.StringVar(value="Generate a secure password")
        ctk.CTkEntry(self, textvariable=self.password,
                     font=("Courier", 18, "bold"),
                     justify="center",
                     state="readonly",
                     height=50).pack(fill="x", padx=30, pady=10)

        # ===== Strength =====
        self.strength_bar = ctk.CTkProgressBar(self)
        self.strength_bar.pack(fill="x", padx=40, pady=10)
        self.strength_bar.set(0)

        self.strength_label = ctk.CTkLabel(self, text="",
                                           font=("Arial", 16, "bold"))
        self.strength_label.pack()

        # ===== Copy =====
        ctk.CTkButton(self, text="📋 Copy to Clipboard",
                      command=self.copy).pack(pady=15)

        self.update_strength()

    def update_strength(self, *args):
        level, text = estimate_strength(
            self.length.get(),
            self.upper.get(),
            self.lower.get(),
            self.digit.get(),
            self.special.get()
        )

        self.strength_bar.set(level / 5)

        colors = ["#ff4d4d", "#ff944d", "#ffff66", "#99ff66", "#33ff99"]
        self.strength_label.configure(text=text, text_color=colors[level - 1])

    def generate(self):
        try:
            pwd = generate_password(
                self.length.get(),
                self.upper.get(),
                self.lower.get(),
                self.digit.get(),
                self.special.get()
            )
            self.password.set(pwd)
            self.update_strength()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.password.get())
        self.strength_label.configure(text="Copied ✔", text_color="#33ff99")

if __name__ == "__main__":

    PasswordApp().mainloop()
