# 🔐 Password Generator GUI

A secure and user-friendly Password Generator built using Python and Tkinter. This application generates strong, random passwords using Python's cryptographically secure `secrets` module.

## 🚀 Features

- **Custom Password Length:** Generate passwords ranging from 8 to 64 characters.
- **Character Selection:** Choose uppercase letters, lowercase letters, numbers, and symbols.
- **Password Strength Indicator:** Displays password strength as Weak, Medium, or Strong.
- **Exclude Ambiguous Characters:** Avoid confusing characters such as `0`, `O`, `1`, `l`, `I`, and `|`.
- **Clipboard Integration:** Automatically copies generated passwords to the clipboard.
- **Password History:** Maintains the last 5 generated passwords during the current session.
- **Secure Generation:** Uses Python's `secrets` module for cryptographically secure random password generation.
- **Graphical User Interface:** Simple and interactive interface built with Tkinter.

## 🛠️ Technologies Used

- Python
- Tkinter
- Secrets Module
- Pyperclip
- String Module

## 📋 Requirements

- Python 3.8 or above
- Pyperclip library

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Password-Generator.git
```

### 2. Navigate to the Project Directory

```bash
cd Password-Generator
```

### 3. Install Dependencies

```bash
python -m pip install pyperclip
```

### 4. Run the Application

```bash
python password_gui.py
```

## 📸 Application Features

The application provides an interactive GUI where users can:

- Adjust password length using a slider or spinbox.
- Select preferred character types.
- Generate secure passwords instantly.
- View password strength.
- Copy passwords to the clipboard.
- Access recently generated passwords.

## 🔒 Security

This application uses Python's `secrets` module, which is designed for generating cryptographically strong random values.

Passwords are generated locally and are not transmitted to any external server.

Password history is stored only in memory and is cleared when the application is closed.

## 🎯 Project Objective

The objective of this project is to develop a secure, efficient, and easy-to-use password generation tool that helps users create strong passwords and improve their password security practices.

## 👩‍💻 Author

**Palak Pandey**


---

⭐ If you find this project useful, consider
