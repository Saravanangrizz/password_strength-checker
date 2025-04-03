document.getElementById('password').addEventListener('input', function() {
    let password = this.value;
    let username = document.getElementById('username').value;
    let platform = document.getElementById('platform').value;
    
    fetch('/check-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password, username, platform })
    })
    .then(response => response.json())
    .then(data => {
        let strengthBar = document.getElementById('strength-bar');
        let strengthText = document.getElementById('strength-text');

        let strengthColors = ["bg-danger", "bg-warning", "bg-info", "bg-success"];
        
        strengthBar.style.width = (data.strength * 25) + "%";
        strengthBar.className = "progress-bar " + strengthColors[data.strength];
        strengthText.innerText = data.message;
    });
});
