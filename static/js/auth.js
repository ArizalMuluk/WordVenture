document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const toggleFormBtn = document.getElementById('toggle-form');
    const toggleText = document.getElementById('toggle-text');
    const welcomeText = document.getElementById('welcome-text');
    const welcomeDescription = document.getElementById('welcome-description');
    const togglePasswordBtn = document.getElementById('toggle-password');
    const toggleRegisterPasswordBtn = document.getElementById('toggle-register-password');
    const loginPassword = document.getElementById('login-password');
    const registerPassword = document.getElementById('register-password');
    const flashMessages = document.querySelectorAll('.flash-message');
    const closeFlashBtns = document.querySelectorAll('.close-flash');

    // Toggle between login and register forms
    let isLoginForm = true;
    toggleFormBtn.addEventListener('click', function() {
        if (isLoginForm) {
            // Switch to Register form
            loginForm.classList.add('slide-out');
            setTimeout(() => {
                loginForm.classList.add('hidden');
                registerForm.classList.remove('hidden');
                registerForm.classList.add('slide-in');
                welcomeText.textContent = 'Halo, Teman Baru!';
                welcomeDescription.textContent = 'Silahkan isi data diri Anda untuk memulai perjalanan bersama kami.';
                toggleText.textContent = 'Masuk';
            }, 300);
        } else {
            // Switch to Login form
            registerForm.classList.add('slide-out');
            setTimeout(() => {
                registerForm.classList.add('hidden');
                loginForm.classList.remove('hidden');
                loginForm.classList.add('slide-in');
                welcomeText.textContent = 'Selamat Datang Kembali!';
                welcomeDescription.textContent = 'Silahkan masuk untuk melanjutkan perjalanan Anda bersama kami.';
                toggleText.textContent = 'Buat Akun';
            }, 300);
        }
        isLoginForm = !isLoginForm;
    });

    // Toggle password visibility
    togglePasswordBtn.addEventListener('click', function() {
        togglePasswordVisibility(loginPassword, this);
    });

    toggleRegisterPasswordBtn.addEventListener('click', function() {
        togglePasswordVisibility(registerPassword, this);
    });

    function togglePasswordVisibility(passwordField, button) {
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
        
        // Toggle eye icon
        const icon = button.querySelector('i');
        if (type === 'text') {
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    }

    // Close flash messages
    closeFlashBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const flashMessage = this.closest('.flash-message');
            flashMessage.classList.add('opacity-0');
            setTimeout(() => {
                flashMessage.remove();
            }, 300);
        });
    });

    // Auto close flash messages after 5 seconds
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(message => {
                message.classList.add('opacity-0');
                setTimeout(() => {
                    message.remove();
                }, 300);
            });
        }, 5000);
    }

    // Form validation
    const registerFormElement = document.querySelector('#register-form form');
    if (registerFormElement) {
        registerFormElement.addEventListener('submit', function(e) {
            const password = document.getElementById('register-password').value;
            const confirmPassword = document.getElementById('confirm-password').value;
            
            if (password !== confirmPassword) {
                e.preventDefault();
                // Create a flash message for password mismatch
                const flashContainer = document.getElementById('flash-messages') || createFlashContainer();
                const flashMessage = document.createElement('div');
                flashMessage.className = 'flash-message bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-2 rounded shadow-md';
                flashMessage.innerHTML = `
                    <div class="flex items-center">
                        <div class="py-1">
                            <i class="fas fa-exclamation-circle mr-2"></i>
                        </div>
                        <div>Password dan konfirmasi password tidak cocok!</div>
                        <button type="button" class="ml-auto close-flash">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                `;
                flashContainer.appendChild(flashMessage);
                
                // Add event listener to close button
                const closeBtn = flashMessage.querySelector('.close-flash');
                closeBtn.addEventListener('click', function() {
                    flashMessage.classList.add('opacity-0');
                    setTimeout(() => {
                        flashMessage.remove();
                    }, 300);
                });
                
                // Auto close after 5 seconds
                setTimeout(() => {
                    flashMessage.classList.add('opacity-0');
                    setTimeout(() => {
                        flashMessage.remove();
                    }, 300);
                }, 5000);
            }
        });
    }

    function createFlashContainer() {
        const container = document.createElement('div');
        container.id = 'flash-messages';
        container.className = 'fixed top-4 right-4 z-50';
        document.body.appendChild(container);
        return container;
    }

    // Add floating animation to decorative elements
    const decorativeElements = document.querySelectorAll('.gradient-bg > div.absolute');
    decorativeElements.forEach((element, index) => {
        element.style.animation = `float ${3 + index * 0.5}s ease-in-out infinite alternate`;
    });

    // Add keyframes for floating animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float {
            0% { transform: translateY(0) rotate(0deg); }
            100% { transform: translateY(-10px) rotate(5deg); }
        }
    `;
    document.head.appendChild(style);

    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('button[type="submit"], #toggle-form');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            ripple.style.position = 'absolute';
            ripple.style.width = '1px';
            ripple.style.height = '1px';
            ripple.style.borderRadius = '50%';
            ripple.style.backgroundColor = 'rgba(255, 255, 255, 0.7)';
            ripple.style.transform = 'scale(0)';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.style.animation = 'ripple 0.6s linear';
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Add keyframes for ripple animation
    const rippleStyle = document.createElement('style');
    rippleStyle.textContent = `
        @keyframes ripple {
            to {
                transform: scale(100);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(rippleStyle);

    // Add input focus animation
    const inputs = document.querySelectorAll('.input-effect');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focus');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focus');
        });
    });

    // Add additional style for input focus
    const inputStyle = document.createElement('style');
    inputStyle.textContent = `
        .relative.focus::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            width: 0;
            height: 2px;
            background: #4f46e5;
            transition: all 0.3s ease;
            transform: translateX(-50%);
            animation: expandWidth 0.3s forwards;
        }
        
        @keyframes expandWidth {
            to { width: 100%; }
        }
    `;
    document.head.appendChild(inputStyle);
});