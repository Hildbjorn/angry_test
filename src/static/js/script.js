document.addEventListener("DOMContentLoaded", function () {
    const checkAuthUrl = "{% url 'check_auth' %}";  // Этот тег будет правильно обработан сервером Django

    function checkAuth() {
        fetch(checkAuthUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка сети');
                }
                return response.json();
            })
            .then(data => {
                if (data.is_authenticated) {
                    window.location.reload();  // Обновить страницу, если пользователь аутентифицирован
                }
            })
            .catch(error => {
                console.error("Ошибка при проверке авторизации:", error);
            });
    }

    setInterval(checkAuth, 3000);  // Проверка каждые 3 секунды
});