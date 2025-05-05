document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    
    // Функция для применения темы
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        if (theme === 'dark') {
            document.body.classList.add('dark-theme');
            document.body.classList.remove('light-theme');
        } else {
            document.body.classList.add('light-theme');
            document.body.classList.remove('dark-theme');
        }
    }
    
    // Проверяем сохраненную тему или системные настройки
    function getPreferredTheme() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) return savedTheme;
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    
    // Инициализация темы
    const currentTheme = getPreferredTheme();
    applyTheme(currentTheme);
    themeToggle.checked = currentTheme === 'dark';
    
    // Обработчик переключения
    themeToggle.addEventListener('change', function() {
        const newTheme = this.checked ? 'dark' : 'light';
        localStorage.setItem('theme', newTheme);
        document.cookie = `theme=${newTheme}; path=/; max-age=31536000`;
        applyTheme(newTheme);
    });
    
    // Следим за изменением системных предпочтений
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!localStorage.getItem('theme')) {
            applyTheme(e.matches ? 'dark' : 'light');
        }
    });
});