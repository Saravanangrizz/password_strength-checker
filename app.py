from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for security

def check_strength(password):
    strength = 0
    suggestions = []

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

    levels = ["Weak", "Fair", "Good", "Strong", "Very Strong"]
    return {"strength": levels[strength-1] if strength > 0 else "Very Weak", "suggestions": suggestions}

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/check-password', methods=['POST'])
def check_password():
    data = request.json
    password = data.get("password", "")
    
    result = check_strength(password)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
