#!/usr/bin/env bash

# File to store user credentials in format: username:hash:salt
DB_FILE="users.db"

# Ensure database file exists with restricted permissions
if [ ! -f "$DB_FILE" ]; then
    touch "$DB_FILE"
    chmod 600 "$DB_FILE"
fi

hash_password() {
    local pass="$1"
    local salt="$2"
    # PBKDF2 with SHA256 and 10,000 iterations
    openssl kdf -keylen 32 -kdfopt digest:SHA256 -kdfopt pass:"$pass" -kdfopt salt:"$salt" -kdfopt iter:10000 PBKDF2 2>/dev/null | xxd -p | tr -d '\n'
}

register_user() {
    echo -e "\n=== User Registration ==="
    read -rp "Enter username: " username

    if [ -z "$username" ]; then
        echo "Username cannot be empty."
        return
    fi

    # Check if username exists
    if grep -q "^${username}:" "$DB_FILE"; then
        echo "Error: Username already exists."
        return
    fi

    read -rsp "Enter password: " password
    echo
    read -rsp "Confirm password: " password_confirm
    echo

    if [ "$password" != "$password_confirm" ]; then
        echo "Error: Passwords do not match."
        return
    fi

    if [ ${#password} -lt 6 ]; then
        echo "Error: Password must be at least 6 characters long."
        return
    fi

    # Generate a random 16-byte hex salt
    salt=$(openssl rand -hex 16)
    hashed_pass=$(hash_password "$password" "$salt")

    # Store credentials
    echo "${username}:${hashed_pass}:${salt}" >> "$DB_FILE"
    echo "Account created successfully for '$username'!"
}

login_user() {
    echo -e "\n=== User Login ==="
    read -rp "Enter username: " username
    read -rsp "Enter password: " password
    echo

    # Find user record
    user_row=$(grep "^${username}:" "$DB_FILE")

    if [ -z "$user_row" ]; then
        echo "Error: Invalid username or password."
        return
    fi

    # Extract stored hash and salt
    stored_hash=$(echo "$user_row" | cut -d':' -f2)
    stored_salt=$(echo "$user_row" | cut -d':' -f3)

    # Hash the provided password with the stored salt
    input_hash=$(hash_password "$password" "$stored_salt")

    if [ "$input_hash" = "$stored_hash" ]; then
        echo "Welcome back, $username! Access granted."
    else
        echo "Error: Invalid username or password."
    fi
}

main() {
    while true; do
        echo -e "\n===================="
        echo "1) Register"
        echo "2) Login"
        echo "3) Exit"
        read -rp "Choose an option (1-3): " choice

        case "$choice" in
            1) register_user ;;
            2) login_user ;;
            3) echo "Goodbye!"; exit 0 ;;
            *) echo "Invalid option. Please try again." ;;
        esac
    done
}

main
