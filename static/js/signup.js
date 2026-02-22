document.querySelector('.submit-btn').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default anchor behavior

    // Retrieve input values
    const username = document.querySelector('input[type="text"]').value;
    const email = document.querySelector('input[type="email"]').value;
    const password = document.querySelector('input[type="password"]').value;

    // Save data to localStorage
    localStorage.setItem('userUsername', username);
    localStorage.setItem('userEmail', email);
    localStorage.setItem('userPassword', password);

    // Optionally, show a message or redirect
    alert('Signup successful! You can now log in.');
    window.location.href = '/login'; // Redirect to login page
});