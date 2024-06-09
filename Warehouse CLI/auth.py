import hashlib

users = {
    'admin': hashlib.sha256('password'.encode()).hexdigest()  # Mock user with username 'admin' and password 'password'
}

logged_in_user = None

def login(username, password):
    global logged_in_user
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if users.get(username) == hashed_password:
        logged_in_user = username
        return f"User {username} logged in successfully."
    else:
        return "Invalid username or password."

def logout():
    global logged_in_user
    if logged_in_user:
        user = logged_in_user
        logged_in_user = None
        return f"User {user} logged out successfully."
    else:
        return "No user is currently logged in."

def is_logged_in():
    return logged_in_user is not None
