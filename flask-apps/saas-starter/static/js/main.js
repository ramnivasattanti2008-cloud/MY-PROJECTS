// Main JavaScript for SaaS Starter

document.addEventListener('DOMContentLoaded', () => {
    // Toast auto-hide
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    });

    // Settings tabs
    const tabs = document.querySelectorAll('.settings-tab');
    const panels = document.querySelectorAll('.settings-panel');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetId = tab.dataset.tab + '-panel';

            tabs.forEach(t => t.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));

            tab.classList.add('active');
            document.getElementById(targetId)?.classList.add('active');
        });
    });

    // Copy API key
    document.querySelectorAll('.btn-icon').forEach(btn => {
        if (btn.title === 'Copy') {
            btn.addEventListener('click', async () => {
                const keyValue = btn.closest('.key-item').querySelector('.key-value').textContent;
                await navigator.clipboard.writeText(keyValue);
                btn.style.color = 'var(--success)';
                setTimeout(() => btn.style.color = '', 2000);
            });
        }
    });

    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideOut { to { transform: translateX(100%); opacity: 0; } }
    `;
    document.head.appendChild(style);
});
