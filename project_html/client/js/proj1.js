document.addEventListener("DOMContentLoaded", function () {
    // Login Form Handling
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault(); 
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('http://localhost:5000/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                const data = await response.json();

                if (response.ok) {
                    localStorage.setItem('token', data.token);
                    localStorage.setItem('user', JSON.stringify(data.user));
                    window.location.href = 'home.html'; // Redirect to home page
                } else {
                    alert(data.error || 'Login failed');
                }
            } catch (error) {
                alert('Network error');
            }
        });
    }

    // Product Display and Cart Functionality
    if (document.querySelector('.container')) {
        async function loadProducts() {
            try {
                const response = await fetch('http://localhost:5000/api/products');
                const products = await response.json();

                const container = document.querySelector('.container');
                container.innerHTML = products.map(product => `
                    <div class="product">
                        <img src="${product.image}" alt="${product.name}">
                        <h3>${product.name}</h3>
                        <p>$${product.price.toFixed(2)}</p>
                        <button class="add-to-cart" data-id="${product._id}">BUY</button>
                    </div>
                `).join('');

                document.querySelectorAll('.add-to-cart').forEach(button => {
                    button.addEventListener('click', async (e) => {
                        const productId = e.target.dataset.id;
                        const token = localStorage.getItem('token');

                        if (!token) {
                            window.location.href = 'login.html';
                            return;
                        }

                        try {
                            const response = await fetch('http://localhost:5000/api/cart', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'Authorization': `Bearer ${token}`
                                },
                                body: JSON.stringify({ productId, quantity: 1 })
                            });
                            const data = await response.json();

                            if (response.ok) {
                                alert('Product added to cart!');
                            } else {
                                alert(data.error || 'Failed to add to cart');
                            }
                        } catch (error) {
                            alert('Network error');
                        }
                    });
                });
            } catch (error) {
                console.error('Error loading products:', error);
            }
        }

        loadProducts();
    }
});
