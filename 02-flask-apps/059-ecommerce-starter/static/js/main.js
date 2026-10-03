// Main JavaScript for E-commerce Template

document.addEventListener('DOMContentLoaded', () => {
    // Toast auto-hide
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    });

    // Add to cart buttons
    document.querySelectorAll('.add-to-cart, .add-to-cart-full').forEach(btn => {
        btn.addEventListener('click', async () => {
            const productId = btn.dataset.id;
            const qtyInput = document.getElementById('quantity');
            const quantity = qtyInput ? parseInt(qtyInput.value) : 1;

            try {
                const response = await fetch('/api/cart/add', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ product_id: productId, quantity: quantity })
                });
                const data = await response.json();

                if (data.success) {
                    document.getElementById('cart-count').textContent = data.cart_count;
                    showToast('Added to cart!', 'success');
                } else {
                    showToast(data.error || 'Failed to add to cart', 'error');
                }
            } catch (error) {
                showToast('An error occurred', 'error');
            }
        });
    });

    // Update cart quantity
    document.querySelectorAll('.update-qty').forEach(btn => {
        btn.addEventListener('click', async () => {
            const productId = btn.dataset.id;
            const action = btn.dataset.action;
            const cartItem = btn.closest('.cart-item');
            const qtySpan = cartItem.querySelector('.qty-value');
            let quantity = parseInt(qtySpan.textContent);

            if (action === 'plus') {
                quantity += 1;
            } else if (action === 'minus' && quantity > 1) {
                quantity -= 1;
            }

            try {
                const response = await fetch('/api/cart/update', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ product_id: productId, quantity: quantity })
                });
                const data = await response.json();

                if (data.success) {
                    qtySpan.textContent = quantity;
                    updateCartTotals(data);
                }
            } catch (error) {
                showToast('An error occurred', 'error');
            }
        });
    });

    // Remove from cart
    document.querySelectorAll('.remove-item').forEach(btn => {
        btn.addEventListener('click', async () => {
            const productId = btn.dataset.id;

            try {
                const response = await fetch('/api/cart/remove', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ product_id: productId })
                });
                const data = await response.json();

                if (data.success) {
                    document.getElementById('cart-count').textContent = data.cart_count;
                    btn.closest('.cart-item').remove();
                    updateCartTotals(data);
                    showToast('Item removed', 'success');
                }
            } catch (error) {
                showToast('An error occurred', 'error');
            }
        });
    });

    // Quantity selector on product page
    const qtyInput = document.getElementById('quantity');
    if (qtyInput) {
        document.getElementById('qty-minus')?.addEventListener('click', () => {
            const val = parseInt(qtyInput.value);
            if (val > 1) qtyInput.value = val - 1;
        });
        document.getElementById('qty-plus')?.addEventListener('click', () => {
            const val = parseInt(qtyInput.value);
            const max = parseInt(qtyInput.max);
            if (!max || val < max) qtyInput.value = val + 1;
        });
    }

    // Helper functions
    function updateCartTotals(data) {
        document.getElementById('subtotal').textContent = '$' + data.subtotal.toFixed(2);
        document.getElementById('shipping').textContent = data.shipping === 0 ? 'FREE' : '$' + data.shipping.toFixed(2);
        document.getElementById('tax').textContent = '$' + data.tax.toFixed(2);
        document.getElementById('total').textContent = '$' + data.total.toFixed(2);
    }

    function showToast(message, type = 'info') {
        const container = document.querySelector('.toast-container') || createToastContainer();
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    function createToastContainer() {
        const container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
        return container;
    }

    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideOut { to { transform: translateX(100%); opacity: 0; } }
    `;
    document.head.appendChild(style);
});
