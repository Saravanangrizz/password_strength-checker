function checkPassword() {
    let password = document.getElementById("password").value;
    let strengthBar = document.getElementById("strength-bar");
    let strengthText = document.getElementById("strength-text");
    let suggestionsBox = document.getElementById("suggestions");
    
    let strength = 0;
    
    if (password.length >= 8) strength++;  
    if (/[A-Z]/.test(password)) strength++;  
    if (/[a-z]/.test(password)) strength++;  
    if (/[0-9]/.test(password)) strength++;  
    if (/[@$!%*?&]/.test(password)) strength++;  

    let strengthLevels = ["Weak", "Fair", "Good", "Strong", "Very Strong"];
    let colors = ["red", "orange", "yellow", "blue", "green"];

    strengthBar.style.width = (strength * 20) + "%";
    strengthBar.style.background = colors[strength - 1] || "red";
    strengthText.textContent = "Strength: " + (strengthLevels[strength - 1] || "Weak");

    suggestImprovements(password);
}

function suggestImprovements(password) {
    let suggestions = [];
    
    if (password.length < 8) suggestions.push("Make it at least 8 characters long.");
    if (!/[A-Z]/.test(password)) suggestions.push("Add an uppercase letter.");
    if (!/[a-z]/.test(password)) suggestions.push("Add a lowercase letter.");
    if (!/[0-9]/.test(password)) suggestions.push("Include a number.");
    if (!/[@$!%*?&]/.test(password)) suggestions.push("Use special characters like @, !, or &.");

    document.getElementById("suggestions").innerHTML = suggestions.length ? "Suggestions: " + suggestions.join(" ") : "";
}
