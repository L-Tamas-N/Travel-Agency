document.addEventListener('DOMContentLoaded', function () {
    const emailInput = document.getElementById('email');
    const emailErrorDiv = document.getElementById('email-error');
    const buttonSubmitDisabled = document.getElementById('submit');

    const passwordInput = document.getElementById('password');
    const passwordErrorDiv = document.getElementById('password-error');

    const consentInput = document.querySelector('input[name="consent"]');
    const consentErrorDiv = document.querySelector('.checkbox-holder .error');

    // Function to check if both email, password, and consent are valid
    function checkFormValidity() {
        const email = emailInput.value;
        const password = passwordInput.value;

        const emailPattern = /^[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com|hotmail\.com|testing\.com)$/;
        const isEmailValid = emailPattern.test(email);
        const isPasswordValid = password.length >= 6 && password.length <= 16 && /[a-z]/.test(password) && /[A-Z]/.test(password) && /\d/.test(password);
        const isConsentChecked = consentInput.checked;

        // Enable/Disable the submit button based on validation
        if (isEmailValid && isPasswordValid && isConsentChecked) {
            buttonSubmitDisabled.classList.remove('disabled');
        } else {
            buttonSubmitDisabled.classList.add('disabled');
        }

        // Show/hide consent error message
        if (!isConsentChecked) {
            consentErrorDiv.innerHTML = 'You must agree to the terms and conditions.';
            consentErrorDiv.style.display = 'block';
        } else {
            consentErrorDiv.innerHTML = '';
            consentErrorDiv.style.display = 'none';
        }
    }

    emailInput.addEventListener('input', function () {
        const email = emailInput.value;

        const emailPattern = /^[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com|hotmail\.com|testing\.com)$/;
        if (email && !emailPattern.test(email)) {
            emailErrorDiv.innerHTML = 'Please enter a valid email address';
            emailErrorDiv.style.display = 'block';
            emailInput.classList.add('invalid');
        } else {
            emailErrorDiv.innerHTML = '';
            emailErrorDiv.style.display = 'none';
            emailInput.classList.remove('invalid');
        }

        // Check form validity after every email input change
        checkFormValidity();
    });

    passwordInput.addEventListener('input', function () {
        const password = passwordInput.value;

        if (password.length < 6 || password.length > 16 || !/[a-z]/.test(password) || !/[A-Z]/.test(password) || !/\d/.test(password)) {
            passwordErrorDiv.innerHTML = 'Password must be between 6 and 16 characters, contain at least one uppercase letter, one lowercase letter, and one number.';
            passwordErrorDiv.style.display = 'block';
            passwordInput.classList.add('invalid');
        } else {
            passwordErrorDiv.innerHTML = '';
            passwordErrorDiv.style.display = 'none';
            passwordInput.classList.remove('invalid');
        }

        // Check form validity after every password input change
        checkFormValidity();
    });

    consentInput.addEventListener('change', function () {
        // Check form validity after the consent checkbox is changed
        checkFormValidity();
    });

    // Initial form validity check (in case there's already some input when the page loads)
    checkFormValidity();
});
