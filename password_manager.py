import os
import json
from cryptography.fernet import Fernet

# Generate a key for encryption and decryption
# You must use this key every time you want to encrypt or decrypt data
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Load the previously generated key
def load_key():
    return open("secret.key", "rb").read()

# Encrypt a password
def encrypt_password(password, key):
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

# Decrypt a password
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

# Add a password
def add_password(service, password, key):
    encrypted_password = encrypt_password(password, key)
    passwords[service] = encrypted_password.decode()  # Decode to store as JSON serializable 
    save_passwords()

# Get a password
def get_password(service, key):
    if service in passwords:
        encrypted_password = passwords[service].encode()  # Encode to bytes for decryption
        return decrypt_password(encrypted_password, key)
    else:
        print("Service not found.")
        return None

# Delete a password
def delete_password(service):
    if service in passwords:
        del passwords[service]
        save_passwords()
    else:
        print("Service not found.")

# Save passwords to a file
def save_passwords():
    with open("passwords.json", "w") as file:
        json.dump(passwords, file)

# Load passwords from a file
def load_passwords():
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    else:
        return {}

# Main function
def main():
    global passwords
    passwords = load_passwords()
    key = load_key()

    while True:
        print("\nPassword Manager")
        print("1. Add password")
        print("2. Get password")
        print("3. Delete password")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            service = input("Enter the service name: ")
            password = input("Enter the password: ")
            add_password(service, password, key)
            print("Password added.")
        elif choice == '2':
            service = input("Enter the service name: ")
            password = get_password(service, key)
            if password:
                print(f"Password for {service}: {password}")
        elif choice == '3':
            service = input("Enter the service name: ")
            delete_password(service)
            print("Password deleted.")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    if not os.path.exists("secret.key"):
        generate_key()
    main()

