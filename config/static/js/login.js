document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('togglePasswordBtn');
    const passwordInput = document.getElementById('id_password');
    const toggleIcon = document.getElementById('toggleIcon');

    if (toggleBtn && passwordInput && toggleIcon) {
        toggleBtn.addEventListener('click', () => {
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                toggleIcon.classList.remove('bi-eye');
                toggleIcon.classList.add('bi-eye-slash');
            } else {
                passwordInput.type = 'password';
                toggleIcon.classList.remove('bi-eye-slash');
                toggleIcon.classList.add('bi-eye');
            }
        });
    }

    const demoButtons = document.querySelectorAll('[data-demo-user]');
    demoButtons.forEach((btn) => {
        btn.addEventListener('click', () => {
            const username = btn.getAttribute('data-demo-user');
            const password = btn.getAttribute('data-demo-pass');
            fillCredentials(username, password);
        });
    });
});

function fillCredentials(username, password) {
    const userInput = document.getElementById('id_username');
    const passInput = document.getElementById('id_password');
    if (userInput && passInput) {
        userInput.value = username;
        passInput.value = password;
        userInput.focus();
    }
}
