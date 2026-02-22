document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    // Retrieve input values
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Retrieve stored data
    const storedEmail = localStorage.getItem('userEmail');
    const storedPassword = localStorage.getItem('userPassword');

    // Check if the user has signed up and credentials match
    if (email === storedEmail && password === storedPassword) {
        alert('Login successful!');
        window.location.href = "/ams_panel";
    } else {
        alert('Please Sign up First or Check your Credentials.');
    }
});