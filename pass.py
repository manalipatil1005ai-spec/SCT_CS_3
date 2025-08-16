import tkinter as tk
from tkinter import messagebox
import string
import pyperclip
import math

# Function to calculate password strength
def check_strength(password):
    length = len(password)
    lower = any(c.islower() for c in password)
    upper = any(c.isupper() for c in password)
    digits = any(c.isdigit() for c in password)
    special = any(c in string.punctuation for c in password)

    score = 0
    suggestions = []

    if length >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters")

    if lower:
        score += 1
    else:
        suggestions.append("Add lowercase letters")

    if upper:
        score += 1
    else:
        suggestions.append("Add uppercase letters")

    if digits:
        score += 1
    else:
        suggestions.append("Include numbers")

    if special:
        score += 1
    else:
        suggestions.append("Use special characters")

    # Estimated time to crack (very simplified)
    charset = 0
    if lower: charset += 26
    if upper: charset += 26
    if digits: charset += 10
    if special: charset += len(string.punctuation)

    guesses = charset ** length
    crack_time = guesses / 1e6  # assuming 1M guesses/sec

    if score <= 2:
        strength = "Weak"
        color = "red"
    elif score == 3:
        strength = "Moderate"
        color = "orange"
    elif score == 4:
        strength = "Strong"
        color = "green"
    else:
        strength = "Very Strong"
        color = "darkgreen"

    return strength, color, suggestions, crack_time


def update_strength(*args):
    password = entry.get()
    if not password:
        strength_label.config(text="Enter a password", fg="black")
        suggestions_label.config(text="")
        crack_time_label.config(text="")
        return

    strength, color, suggestions, crack_time = check_strength(password)
    strength_label.config(text=f"Strength: {strength}", fg=color)

    if suggestions:
        suggestions_label.config(text="Suggestions: " + ", ".join(suggestions))
    else:
        suggestions_label.config(text="Looks good!")

    if crack_time < 60:
        time_text = f"Crack Time: {crack_time:.2f} sec"
    elif crack_time < 3600:
        time_text = f"Crack Time: {crack_time/60:.2f} min"
    elif crack_time < 86400:
        time_text = f"Crack Time: {crack_time/3600:.2f} hr"
    else:
        time_text = f"Crack Time: {crack_time/86400:.2f} days"

    crack_time_label.config(text=time_text)


def copy_password():
    password = entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard")


# GUI Setup
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("500x300")
root.configure(bg="#f4f4f9")

title = tk.Label(root, text="🔐 Password Strength Checker", font=("Arial", 16, "bold"), bg="#f4f4f9")
title.pack(pady=10)

entry = tk.Entry(root, width=40, font=("Arial", 14), show="*")
entry.pack(pady=10)
entry.bind("<KeyRelease>", update_strength)

strength_label = tk.Label(root, text="Enter a password", font=("Arial", 12), bg="#f4f4f9")
strength_label.pack(pady=5)

suggestions_label = tk.Label(root, text="", font=("Arial", 10), fg="gray", wraplength=400, bg="#f4f4f9")
suggestions_label.pack(pady=5)

crack_time_label = tk.Label(root, text="", font=("Arial", 10), fg="blue", bg="#f4f4f9")
crack_time_label.pack(pady=5)

copy_btn = tk.Button(root, text="Copy Password", command=copy_password, bg="#007acc", fg="white", font=("Arial", 12), relief="raised")
copy_btn.pack(pady=10)

root.mainloop()