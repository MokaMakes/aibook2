import hashlib
import getpass

# In-memory database to store credentials: {username: (hashed_password, salt)}
user_db = {}

def hash_password(password: str, salt: bytes = None) -> tuple[str, bytes]:
    """Hashes a password with a salt using SHA-256."""
    import os
    if salt is None:
        salt = os.urandom(16)  # Generate a random 16-byte salt
    
    # Combine salt and password, then hash
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return hashed.hex(), salt

def register():
    print("\n--- User Registration ---")
    username = input("Enter a username: ").strip().lower()
    
    if not username:
        print("Username cannot be empty.")
        return
        
    if username in user_db:
        print("Username already exists! Please try logging in.")
        return
    
    password = getpass.getpass("Enter a password: ")
    confirm_password = getpass.getpass("Confirm password: ")
    
    if password != confirm_password:
        print("Passwords do not match!")
        return
        
    if len(password) < 6:
        print("Password must be at least 6 characters long.")
        return
    
    # Hash password and save to database
    hashed_pwd, salt = hash_password(password)
    user_db[username] = (hashed_pwd, salt)
    print(f"Account created successfully for '{username}'!")

def login():
    print("\n--- User Login ---")
    username = input("Enter username: ").strip().lower()
    password = getpass.getpass("Enter password: ")
    
    if username not in user_db:
        print("Invalid username or password.")
        return
    
    stored_hash, salt = user_db[username]
    input_hash, _ = hash_password(password, salt)
    
    if input_hash == stored_hash:
        print(f"\nWelcome back, {username}! Access granted.")
    else:
        print("Invalid username or password.")

def main():
    while True:
        print("\n=== Welcome Menu ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()
        
        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid selection. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
