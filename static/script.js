async function checkPassword() {
    let username = document.getElementById("username").value.trim();
    let platform = document.getElementById("platform").value;
    let password = document.getElementById("password").value.trim();
    
    let strengthBar = document.getElementById("strength-bar");
    let strengthText = document.getElementById("strength-text");
    let suggestionsBox = document.getElementById("suggestions");

    let response = await fetch('/check-password', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ password, username, platform })
    });

    let result = await response.json();

    let strengthLevels = ["Very Weak", "Weak", "Fair", "Good", "Strong", "Very Strong"];
    let colors = ["darkred", "red", "orange", "yellow", "blue", "green"];

    let strengthIndex = strengthLevels.indexOf(result.strength);
    
    strengthBar.style.width = ((strengthIndex + 1) * 20) + "%";
    strengthBar.style.background = colors[strengthIndex] || "darkred";
    strengthText.textContent = "Strength: " + result.strength;
    
    suggestionsBox.innerHTML = result.suggestions.length ? "Suggestions: " + result.suggestions.join("<br>") : "";
}
