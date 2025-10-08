
const animateVehicle = () => {
    const spots = document.querySelectorAll('.spot');
    spots.forEach((spot, index) => {
        if (spot.classList.contains('occupied')) {
            setTimeout(() => {
                spot.style.animation = 'gentlePulse 3s infinite';
            }, index * 100);
        }
    });
};

const ensureTwemojiLoaded = () => {
    return new Promise((resolve, reject) => {
        if (window.twemoji) {
            resolve(window.twemoji);
            return;
        }
        const existing = document.querySelector('script[data-lib="twemoji"]');
        if (existing) {
            existing.addEventListener('load', () => resolve(window.twemoji));
            existing.addEventListener('error', reject);
            return;
        }
        const script = document.createElement('script');
        script.src = 'https://twemoji.maxcdn.com/v/latest/twemoji.min.js';
        script.defer = true;
        script.async = true;
        script.setAttribute('data-lib', 'twemoji');
        script.addEventListener('load', () => resolve(window.twemoji));
        script.addEventListener('error', reject);
        document.head.appendChild(script);
    });
};

const updateOptimization = () => {
    const progressBar = document.querySelector('.progress-fill');
    if (progressBar) {
        const currentWidth = parseFloat(progressBar.style.width) || 0;
        const targetWidth = parseFloat(progressBar.dataset.targetWidth) || 0;
        
        if (currentWidth < targetWidth) {
            progressBar.style.width = Math.min(currentWidth + 2, targetWidth) + '%';
            setTimeout(updateOptimization, 100);
        }
    }
};

const createFloatingVehicles = () => {
    const vehicles = ['🚗', '🚙', '🚐', '🚚', '🚛', '🏎️', '🚜'];
    const container = document.querySelector('.floating-vehicles');
    
    for (let i = 0; i < 8; i++) {
        const vehicle = document.createElement('div');
        vehicle.className = 'floating-vehicle';
        vehicle.textContent = vehicles[Math.floor(Math.random() * vehicles.length)];
        vehicle.style.left = Math.random() * 100 + '%';
        vehicle.style.animationDelay = Math.random() * 6 + 's';
        vehicle.style.animationDuration = (Math.random() * 3 + 4) + 's';
        container.appendChild(vehicle);
    }
};

const addVisualFeedback = (element, type) => {
    if (type === 'success') {
        element.style.boxShadow = '0 0 20px rgba(39, 174, 96, 0.5)';
        setTimeout(() => {
            element.style.boxShadow = '';
        }, 1000);
    } else if (type === 'error') {
        element.style.boxShadow = '0 0 20px rgba(231, 76, 60, 0.5)';
        setTimeout(() => {
            element.style.boxShadow = '';
        }, 1000);
    }
};

// Initialize all animations and event listeners
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(animateVehicle, 300);
    
    // Button click handlers
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            button.style.opacity = '0.7';
            button.textContent = 'Đang thêm...';
            setTimeout(() => {
                button.closest('form').submit();
            }, 200);
        });
    });
    
    // Parking spot hover effects
    document.querySelectorAll('.spot').forEach(spot => {
        spot.addEventListener('mouseenter', () => {
            if (spot.classList.contains('occupied')) {
                spot.style.transform = 'scale(1.05)';
            }
        });
        
        spot.addEventListener('mouseleave', () => {
            spot.style.transform = 'scale(1)';
        });
    });
    
    setTimeout(updateOptimization, 500);
    createFloatingVehicles();

    // Ensure emoji icons render consistently via Twemoji CDN
    ensureTwemojiLoaded()
        .then((twemoji) => {
            if (!twemoji) return;
            const iconContainer = document.querySelector('.floating-vehicles');
            if (iconContainer) {
                twemoji.parse(iconContainer, { folder: 'svg', ext: '.svg' });
            }
        })
        .catch(() => {
            // Silently ignore if CDN fails; native emoji will render
        });
});