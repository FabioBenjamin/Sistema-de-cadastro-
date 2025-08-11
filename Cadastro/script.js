document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registrationForm');

    form.addEventListener('submit', function (event) {
        const username = form.username.value.trim();
        const email = form.email.value.trim();
        const password = form.password.value.trim();

        if (!username || !email || !password) {
            alert('Por favor, preencha todos os campos.');
            event.preventDefault();
            return;
        }

        const emailValido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailValido.test(email)) {
            alert('Por favor, insira um gmail válido.');
            event.preventDefault();
            return;
        }
    });
});