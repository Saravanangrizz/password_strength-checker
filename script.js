document.addEventListener("DOMContentLoaded", function() {
    let passwordField = document.getElementById('password');
    let usernameField = document.getElementById('username');
    let platformField = document.getElementById('platform');
    let strengthBar = document.getElementById('strength-bar');
    let strengthText = document.getElementById('strength-text');

    function checkPasswordStrength() {
        let password = passwordField.value;
        let username = usernameField.value;
        let platform = platformField.value;
        
        fetch('/check-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password, username, platform })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                let strengthColors = ["bg-danger", "bg-warning", "bg-info", "bg-success"];
                
                strengthBar.style.width = (data.strength * 25) + "%";
                strengthBar.className = "progress-bar " + strengthColors[data.strength];
                strengthText.innerText = data.message;
            } else {
                strengthText.innerText = "⚠️ Error: No response from server!";
            }
        })
        .catch(error => {
            console.error("Error fetching strength:", error);
            strengthText.innerText = "⚠️ Error checking password!";
        });
    }

    passwordField.addEventListener('input', checkPasswordStrength);
    usernameField.addEventListener('input', checkPasswordStrength);
    platformField.addEventListener('change', checkPasswordStrength);
});
