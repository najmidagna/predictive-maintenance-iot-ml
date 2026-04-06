import json
import os

USER_FILE = "users.json"

def load_users():
    # If file does not exist → create default admin
    if not os.path.exists(USER_FILE):
        default_users = {
            "admin": {"password": "1234", "role": "admin"}
        }
        with open(USER_FILE, "w") as f:
            json.dump(default_users, f, indent=4)
        return default_users

    # If the file is empty → restore admin
    if os.path.getsize(USER_FILE) == 0:
        default_users = {
            "admin": {"password": "1234", "role": "admin"}
        }
        with open(USER_FILE, "w") as f:
            json.dump(default_users, f, indent=4)
        return default_users

    # Load users
    with open(USER_FILE, "r") as f:
        data = json.load(f)

    # ⭐ Convert old string format to dict automatically
    for name, value in list(data.items()):
        if isinstance(value, str):
            data[name] = {"password": value, "role": "user"}

    return data


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)


def login_user(username, password):
    users = load_users()
    if username in users and users[username]["password"] == password:
        return users[username]["role"]   # admin or user
    return None
