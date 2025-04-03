from flask import Flask, request, render_template
import re
import secrets
import math
import string

app = Flask(__name__)

def check_password_strength(password):
    length = len(password)
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"[0-9]", password))
    has_special = bool(re.search(r"[@#$%^&*!]", password))

    entropy = calculate_entropy(password)

    if length >= 12 and has_upper and has_lower and has_digit and has_special:
        strength = "Strong"
    elif length >= 8 and (has_upper or has_lower) and (has_digit or has_special):
        strength = "Medium"
    else:
        strength = "Weak"

    return strength, entropy

def calculate_entropy(password):
    charset = 0
    if any(c in string.ascii_lowercase for c in password):
        charset += 26
    if any(c in string.ascii_uppercase for c in password):
        charset += 26
    if any(c in string.digits for c in password):
        charset += 10
    if any(c in string.punctuation for c in password):
        charset += 32

    entropy = len(password) * math.log2(charset) if charset else 0
    return round(entropy, 2)

def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(16))

@app.route("/", methods=["GET", "POST"])
def index():
    strength, entropy, generated_password = "", "", ""
    if request.method == "POST":
        password = request.form.get("password")
        if password:
            strength, entropy = check_password_strength(password)
        if "generate" in request.form:
            generated_password = generate_password()
    return render_template("index.html", strength=strength, entropy=entropy, generated_password=generated_password)

if __name__ == "__main__":
    app.run(debug=True)
