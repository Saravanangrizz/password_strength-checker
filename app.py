from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # Enable CORS

def check_strength(password, username, platform):
    strength = 0
    suggestions = []

    # Basic strength checks
    if len(password) >= 8:
        strength += 1
    else:
        suggestions.append("Make it at least 8 characters long.")
    
    if re.search(r'[A-Z]', password):
        strength += 1
    else:
        suggestions.append("Add an uppercase letter.")
    
    if re.search(r'[a-z]', password):
        strength += 1
    else:
        suggestions.append("Add a lowercase letter.")
    
    if re.search(r'[0-9]', password):
        strength += 1
    else:
        suggestions.append("Include a number.")
    
    if re.search(r'[@$!%*?&]', password):
        strength += 1
    else:
        suggestions.append("Use special characters like @, !, or &.")

    # Check if password contains the username
    if username.lower() in password.lower():
        strength -= 1
        suggestions.append("Avoid using your username in the password.")

    # Platform-specific recommendations
    if platform.lower() in ["banking", "work", "government"]:
        if strength < 4:
            suggestions.append("For secure platforms, use at least 12 characters and mix symbols, numbers, and letters.")

    levels = ["Very Weak", "Weak", "Fair", "Good", "Strong", "Very Strong"]
    strength = max(0, min(strength, len(levels) - 1))  # Keep strength in valid range
    
    return {"strength": levels[strength], "suggestions": suggestions}

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/check-password', methods=['POST'])
def check_password():
    data = request.json
    password = data.get("password", "")
    username = data.get("username", "")
    platform = data.get("platform", "")

    result = check_strength(password, username, platform)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
