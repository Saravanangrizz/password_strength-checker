from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='static')

# List of common weak passwords
COMMON_PASSWORDS = {"password", "123456789", "qwerty", "letmein", "password123","987654321"}

def check_password_strength(password, username, platform):
    strength = 0
    message = "Weak"

    username = username.lower()
    password_lower = password.lower()

    # Username check
    if username and username in password_lower:
        return {"strength": 0, "message": "❌ Password should not contain your username!"}

    # Common weak passwords
    if password_lower in COMMON_PASSWORDS:
        return {"strength": 0, "message": "❌ This password is too common!"}

    # Strength logic
    if len(password) > 8:
        strength += 1
    if any(c.islower() for c in password) and any(c.isupper() for c in password):
        strength += 1
    if any(c.isdigit() for c in password):
        strength += 1
    if any(c in "!@#$%^&*()-_+=" for c in password):
        strength += 1

    # Platform-specific rules
    if platform == "banking":
        if len(password) >= 12 and any(c in "!@#$%^&*()-_+=" for c in password):
            strength += 1
        else:
            message = "⚠️ For banking, use at least 12 characters and special symbols!"
            strength -= 1

    # Strength labels
    strength_labels = ["Weak", "Moderate", "Strong", "Very Strong"]
    strength = max(0, min(strength, 3))  

    return {"strength": strength, "message": message if message != "Weak" else strength_labels[strength]}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check-password', methods=['POST'])
def check_password():
    data = request.json
    password = data.get("password", "")
    username = data.get("username", "")
    platform = data.get("platform", "general")

    result = check_password_strength(password, username, platform)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
