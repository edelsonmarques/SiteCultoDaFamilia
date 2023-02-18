const form = {
    email: () => document.getElementById("email"),
    username: () => document.getElementById("username"),
    password: () => document.getElementById("password"),
    registerButton: () => document.getElementById("register_button"),
    usernameRequiredError: () => document.getElementById("username-required-error"),
    emailRequiredError: () => document.getElementById("email-required-error"),
    emailInvalidError: () => document.getElementById("email-invalid-error"),
    passwordRequiredError: () => document.getElementById("password-required-error"),
    recoveryButton: () => document.getElementById("recovery_button"),
    loginButton: () => document.getElementById("login_button"),
    usernameName: () => document.getElementById("username"),
}