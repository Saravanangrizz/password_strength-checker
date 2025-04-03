from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# List of common weak passwords
COMMON_PASSWORDS = {"password", "123456789", "qwerty", "letmein", "password123","987654321"}

def check_password_strength(password, username, platform):
    strength = 0
    message = ""

    # Convert to lowercase for case-insensitive checks
    username = username.lower()
    password_lower = password.lower()

    # Check if password contains the username (Weak)
    if username and username in password_lower:
        return {"strength": 0, "message": "❌ Password should not contain your username!"}

    # Check against common weak passwords
    if password_lower in COMMON_PASSWORDS:
        return {"strength": 0, "message": "❌ This is a very common and weak password!"}

    # Basic password checks
    if len(password) > 8:
        strength += 1
    if any(c.islower() for c in password) and any(c.isupper() for c in password):
        strength += 1
    if any(c.isdigit() for c in password):
        strength += 1
    if any(c in "!@#$%^&*()-_+=" for c in password):  # Special character check
        strength += 1

    # Platform-based security requirements
    if platform == "banking":
        if len(password) >= 12 and any(c in "!@#$%^&*()-_+=" for c in password):
            strength += 1  # Extra strength for secure banking
        else:
            message = "⚠️ For banking, use at least 12 characters with special symbols!"
            strength -= 1

    # Strength labels
    strength_labels = ["Weak", "Moderate", "Strong", "Very Strong"]
    strength = max(0, min(strength, 3))  # Keep within range (0-3)

    return {"strength": strength, "message": message or strength_labels[strength]}

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
