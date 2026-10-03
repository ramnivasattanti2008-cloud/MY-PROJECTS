// Main JavaScript for Blog Template

document.addEventListener('DOMContentLoaded', () => {
    // Toast auto-hide
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    });

    // Auto-slug from title
    const titleInput = document.querySelector('input[name="title"]');
    const slugInput = document.querySelector('input[name="slug"]');

    if (titleInput && slugInput) {
        titleInput.addEventListener('input', () => {
            if (!slugInput.dataset.manual) {
                slugInput.value = titleInput.value
                    .toLowerCase()
                    .replace(/[^a-z0-9]+/g, '-')
                    .replace(/^-|-$/g, '');
            }
        });

        slugInput.addEventListener('input', () => {
            slugInput.dataset.manual = 'true';
        });
    }

    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideOut { to { transform: translateX(100%); opacity: 0; } }
    `;
    document.head.appendChild(style);
});
