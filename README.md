# Cipher-Vault

**Cipher Vault** is a secure command-line interface (CLI) password manager written in Python.  
It stores your passwords encrypted using a **Caesar cipher**, so your credentials remain safe even if someone accesses your file.

---

## Features

- **Master password protection** – Only authorized users can access the vault.  
- **Caesar cipher encryption** – All site names, usernames, and passwords are encrypted before saving.  
- **Add passwords** – Store new site credentials securely.  
- **View passwords** – Optionally decrypt and view stored credentials with a separate decryption password.  
- **Delete passwords** – Safely remove passwords with a confirmation step.  
- **CLI interface** – Simple and easy-to-use command-line interface.  
- **Auto-uppercase site names** and **alphabetical sorting** for organization.

---

## Installation

1. Make sure you have **Python 3** installed.  
2. Install the required library for masked input:

```bash
pip install pwinput
```
## Usage
1. Open a terminal (Command Prompt, PowerShell, or VS Code terminal).
2. Go to your program directory
3. Run the program:
python cipher_vault.py
4. Enter your master password to unlock the vault.
5. Use the menu to add, view, or delete passwords.

## Security Notes
- Your passwords are stored in vault.json encrypted using a Caesar cipher.
- To reveal the credentials, you need a separate decryption password.
