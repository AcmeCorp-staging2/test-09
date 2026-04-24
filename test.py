import os
import sqlite3
import pickle
import hashlib
import requests

# Hardcoded secret (SAST should flag this)
API_KEY = "12345-SECRET-KEY"
DB_PASSWORD = "admin123"


# SQL Injection vulnerability
def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)  # vulnerable

    return cursor.fetchall()


# Command Injection vulnerability
def ping_host(host):
    os.system(f"ping -c 1 {host}")  # vulnerable


# Insecure deserialization
def load_user_data(data):
    return pickle.loads(data)  # vulnerable


# Weak hashing (MD5)
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


# Path Traversal vulnerability
def read_file(filename):
    with open(f"/var/data/{filename}", "r") as f:
        return f.read()


# SSRF vulnerability
def fetch_url(url):
    response = requests.get(url)  # no validation
    return response.text


# Debug mode enabled (Flask example)
from flask import Flask, request

app = Flask(__name__)
app.debug = True  # should not be enabled in production


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # insecure comparison
    if username == "admin" and password == "admin":
        return "Welcome admin"
    return "Invalid credentials"


# Use of eval (Remote Code Execution risk)
def run_code(user_input):
    return eval(user_input)


if __name__ == "__main__":
    print(get_user("admin"))
    ping_host("127.0.0.1")
