"""
Password Strength Analyzer (GUI)
Vortex Tech Cybersecurity Internship - Week 2

A simple Tkinter desktop app that rates password strength based on
length, character variety, and a common-password check, and shows
live feedback plus a visual strength meter.
"""

import tkinter as tk
from tkinter import ttk

COMMON_PASSWORDS = {
    "123456", "123456789", "password", "12345678", "qwerty",
    "111111", "123123", "abc123", "password1", "letmein",
    "welcome", "admin", "iloveyou", "monkey", "dragon",
}

RATING_COLORS = {
    "Very Weak": "#ff5c5c",
    "Weak": "#ffa64d",
    "Medium": "#ffd93d",
    "Strong": "#2ee6a6",
}

RATING_SCORE = {
    "Very Weak": 15,
    "Weak": 35,
    "Medium": 65,
    "Strong": 100,
}


def analyze_password(password: str) -> dict:
    """Core scoring logic — same rules as the CLI checker."""
    if password.lower() in COMMON_PASSWORDS:
        return {
            "rating": "Very Weak",
            "notes": ["This is one of the most common leaked passwords — "
                      "crackable in seconds. Avoid it completely."],
        }

    length_ok = len(password) >= 8
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    checks_passed = sum([length_ok, has_upper, has_lower, has_digit, has_special])

    notes = []
    if not length_ok:
        notes.append("Use at least 8 characters.")
    if not has_upper:
        notes.append("Add an uppercase letter.")
    if not has_lower:
        notes.append("Add a lowercase letter.")
    if not has_digit:
        notes.append("Add a number.")
    if not has_special:
        notes.append("Add a special character (e.g. !, @, #, $).")

    if checks_passed <= 2:
        rating = "Weak"
    elif checks_passed in (3, 4):
        rating = "Medium"
    else:
        rating = "Strong"

    if not notes:
        notes.append("Great job — this password meets all the basic strength checks.")

    return {"rating": rating, "notes": notes}


class PasswordAnalyzerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Password Strength Analyzer")
        self.root.geometry("420x480")
        self.root.configure(bg="#0d1f1f")
        self.root.resizable(False, False)

        self._build_header()
        self._build_input()
        self._build_meter()
        self._build_feedback()
        self._build_footer()

    def _build_header(self):
        tk.Label(
            self.root, text="🔐 Password Strength Analyzer",
            font=("Segoe UI", 15, "bold"), bg="#0d1f1f", fg="#ffffff",
        ).pack(pady=(20, 4))
        tk.Label(
            self.root, text="Vortex Tech Cybersecurity Internship — Week 2",
            font=("Segoe UI", 9), bg="#0d1f1f", fg="#7fd9c4",
        ).pack(pady=(0, 16))

    def _build_input(self):
        frame = tk.Frame(self.root, bg="#0d1f1f")
        frame.pack(pady=4)

        self.show_var = tk.BooleanVar(value=False)
        self.password_entry = tk.Entry(
            frame, width=28, font=("Segoe UI", 12), show="*",
            relief="flat", justify="center",
        )
        self.password_entry.grid(row=0, column=0, ipady=6, padx=(0, 6))
        self.password_entry.bind("<KeyRelease>", lambda e: self.analyze())

        tk.Checkbutton(
            frame, text="show", variable=self.show_var, bg="#0d1f1f",
            fg="#7fd9c4", activebackground="#0d1f1f", selectcolor="#0d1f1f",
            command=self._toggle_visibility,
        ).grid(row=0, column=1)

        tk.Button(
            self.root, text="Analyze Password", font=("Segoe UI", 10, "bold"),
            bg="#17a589", fg="white", relief="flat", padx=12, pady=6,
            activebackground="#128f77", command=self.analyze,
        ).pack(pady=14)

    def _toggle_visibility(self):
        self.password_entry.config(show="" if self.show_var.get() else "*")

    def _build_meter(self):
        self.rating_label = tk.Label(
            self.root, text="Rating: —", font=("Segoe UI", 11, "bold"),
            bg="#0d1f1f", fg="#ffffff",
        )
        self.rating_label.pack(pady=(0, 6))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Strength.Horizontal.TProgressbar",
                         troughcolor="#123030", background="#2ee6a6", thickness=14)

        self.meter = ttk.Progressbar(
            self.root, length=320, mode="determinate",
            style="Strength.Horizontal.TProgressbar",
        )
        self.meter.pack(pady=(0, 16))

    def _build_feedback(self):
        tk.Label(
            self.root, text="Security Feedback", font=("Segoe UI", 10, "bold"),
            bg="#0d1f1f", fg="#ffffff",
        ).pack()
        self.feedback_box = tk.Text(
            self.root, height=8, width=42, font=("Segoe UI", 9),
            bg="#123030", fg="#d6f5ec", relief="flat", wrap="word", padx=8, pady=8,
        )
        self.feedback_box.pack(pady=(6, 10))
        self.feedback_box.config(state="disabled")

    def _build_footer(self):
        tk.Label(
            self.root, text="VortexTech Cybersecurity Internship 2026",
            font=("Segoe UI", 8), bg="#0d1f1f", fg="#3d7a6b",
        ).pack(side="bottom", pady=10)

    def analyze(self):
        password = self.password_entry.get()

        if not password:
            self.rating_label.config(text="Rating: —")
            self.meter["value"] = 0
            self._set_feedback(["Start typing a password to see live feedback."])
            return

        result = analyze_password(password)
        rating = result["rating"]
        color = RATING_COLORS[rating]

        self.rating_label.config(text=f"Rating: {rating}", fg=color)
        self.meter["value"] = RATING_SCORE[rating]

        style = ttk.Style()
        style.configure("Strength.Horizontal.TProgressbar", background=color)

        self._set_feedback(result["notes"])

    def _set_feedback(self, notes):
        self.feedback_box.config(state="normal")
        self.feedback_box.delete("1.0", tk.END)
        for note in notes:
            self.feedback_box.insert(tk.END, f"• {note}\n")
        self.feedback_box.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordAnalyzerApp(root)
    root.mainloop()