import json
import os
import pwinput

# Files
PASSWORD_FILE = "vault.json"
MASTER_PASSWORD = "mypassword"        # Master password for program access
DECRYPT_PASSWORD = "decrypt123"       # Password required to decrypt credentials

# Caesar cipher (-12 offset)
def caesar_encrypt(text, shift=-12):
    result = ""
    for char in text:
        if char.isupper():  # A-Z
            result += chr((ord(char) - 65 + shift) % 26 + 65)
        elif char.islower():  # a-z
            result += chr((ord(char) - 97 + shift) % 26 + 97)
        elif char.isdigit():  # 0-9
            result += chr((ord(char) - 48 + shift) % 10 + 48)
        else:
            result += char
    return result

def caesar_decrypt(text, shift=-12):
    return caesar_encrypt(text, shift=-shift)

# Authentication
def authenticate():
    attempts = 3
    while attempts > 0:
        pwd = pwinput.pwinput("Enter master password: ", mask="*")
        if pwd == MASTER_PASSWORD:
            return True
        else:
            attempts -= 1
            print(f"Incorrect password! {attempts} attempts left.")
    print("Access denied!")
    return False

# Add password
def add_password():
    site = input("Enter site/app name: ").strip().upper()  # always uppercase
    username = pwinput.pwinput("Enter username/email: ", mask="*").strip()
    pwd = pwinput.pwinput("Enter password: ", mask="*").strip()
    
    # Load existing passwords (encrypted)
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as f:
            encrypted_list = json.load(f)
    else:
        encrypted_list = []
    
    # Encrypt the new entry
    encrypted_entry = {
        "site": caesar_encrypt(site),
        "username": caesar_encrypt(username),
        "password": caesar_encrypt(pwd)
    }
    
    encrypted_list.append(encrypted_entry)
    
    with open(PASSWORD_FILE, "w") as f:
        json.dump(encrypted_list, f, indent=4)
    
    print(f"Password for {site} saved successfully!")

# Check passwords
def view_passwords():
    if not os.path.exists(PASSWORD_FILE):
        print("No passwords stored.")
        return
    
    with open(PASSWORD_FILE, "r") as f:
        encrypted_list = json.load(f)
    
    # Decrypt entries for display
    passwords = []
    for entry in encrypted_list:
        passwords.append({
            "site": caesar_decrypt(entry["site"]),
            "username": caesar_decrypt(entry["username"]),
            "password": caesar_decrypt(entry["password"])
        })
    
    # Sort by site name
    passwords.sort(key=lambda x: x["site"])
    
    print("\nStored passwords (username/password hidden):")
    for i, entry in enumerate(passwords, start=1):
        print(f"{i}. {entry['site']} - [Encrypted credentials]")
    
    choice = input("\nDo you want to decrypt credentials? (y/n): ").strip().lower()
    if choice == "y":
        pwd = pwinput.pwinput("Enter decryption password: ", mask="*")
        if pwd == DECRYPT_PASSWORD:
            print("\nDecrypted credentials:")
            for i, entry in enumerate(passwords, start=1):
                print(f"{i}. {entry['site']} - {entry['username']} - {entry['password']}")
        else:
            print("Incorrect decryption password!")

# Delete password
def delete_password():
    if not os.path.exists(PASSWORD_FILE):
        print("No passwords stored.")
        return
    
    with open(PASSWORD_FILE, "r") as f:
        encrypted_list = json.load(f)
    
    # Decrypt entries for display
    passwords = []
    for entry in encrypted_list:
        passwords.append({
            "site": caesar_decrypt(entry["site"]),
            "username": caesar_decrypt(entry["username"]),
            "password": caesar_decrypt(entry["password"])
        })
    
    passwords.sort(key=lambda x: x["site"])
    
    print("Stored passwords:")
    for i, entry in enumerate(passwords, start=1):
        print(f"{i}. {entry['site']} - [Encrypted credentials]")
    
    choice = input("Enter the number of the password to delete: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(passwords):
        confirm = input("Type CONFIRM to delete this password: ").strip()
        if confirm.upper() == "CONFIRM":
            # Remove the selected entry
            passwords.pop(int(choice)-1)
            
            # Encrypt remaining passwords before saving
            encrypted_list = []
            for entry in passwords:
                encrypted_list.append({
                    "site": caesar_encrypt(entry["site"]),
                    "username": caesar_encrypt(entry["username"]),
                    "password": caesar_encrypt(entry["password"])
                })
            
            with open(PASSWORD_FILE, "w") as f:
                json.dump(encrypted_list, f, indent=4)
            
            print("Password deleted successfully.")
        else:
            print("Deletion cancelled.")
    else:
        print("Invalid choice!")

#CLI Menu
def menu():
    while True:
        print("\n=== CLI Password Manager ===")
        print("1. Add Password")
        print("2. View Passwords")
        print("3. Delete Password")
        print("4. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            add_password()
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            delete_password()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

# Main
if __name__ == "__main__":
    if authenticate():   # Authenticate first
        menu()           # show menu