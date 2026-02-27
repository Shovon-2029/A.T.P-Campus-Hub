import json
import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Enable CORS so your frontend HTML can communicate with this backend
CORS(app) 

# The name of the JSON file where data will be stored
USERS_FILE = 'users.json'

# --- Helper Functions ---

def read_users():
    """Reads users from the JSON file. Returns an empty list if file doesn't exist."""
    if not os.path.exists(USERS_FILE):
        return []
    
    with open(USERS_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def write_users(users):
    """Writes the user list back to the JSON file formatted nicely."""
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# --- API Routes ---

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not email or not password or not role:
        return jsonify({'error': 'Missing required fields'}), 400

    users = read_users()

    # Check if the email is already registered
    for user in users:
        if user['email'] == email:
            return jsonify({'error': 'Email is already registered'}), 409

    # Hash the password for security
    hashed_password = generate_password_hash(password)
    
    # Create the new user dictionary
    new_user = {
        'email': email,
        'password_hash': hashed_password,
        'role': role
    }
    
    # Append and save
    users.append(new_user)
    write_users(users)

    return jsonify({'message': 'Account created successfully!'}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not email or not password or not role:
        return jsonify({'error': 'Missing required fields'}), 400

    users = read_users()

    # Search for the user in our JSON data
    for user in users:
        if user['email'] == email:
            # Verify the hashed password matches
            if check_password_hash(user['password_hash'], password):
                # Ensure they selected the correct role
                if user['role'] != role:
                    return jsonify({'error': f'Account exists, but not as a {role}. Please check your role selection.'}), 403
                
                return jsonify({'message': 'Login successful!', 'role': user['role']}), 200
            else:
                return jsonify({'error': 'Invalid email or password'}), 401

    # If no email was found
    return jsonify({'error': 'Invalid email or password'}), 401


@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    users = read_users()

    # Search for the user by email
    for user in users:
        if user['email'] == email:
            # Generate a simple temporary password (e.g., Campus4829!)
            temp_password = f"Campus@{random.randint(1000, 9999)}"
            
            # Hash the new temporary password and overwrite the old one
            user['password_hash'] = generate_password_hash(temp_password)
            write_users(users)
            
            return jsonify({
                'message': 'Password reset successful', 
                'temp_password': temp_password
            }), 200

    # If no email was found
    return jsonify({'error': 'No account found with this email.'}), 404


if __name__ == '__main__':
    # Running on port 5002 to match your frontend fetch requests
    app.run(debug=True, port=5002)