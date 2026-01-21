// Main JavaScript for landing page

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar scroll effect
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
        navbar.style.boxShadow = 'var(--shadow-md)';
    } else {
        navbar.style.boxShadow = 'none';
    }

    lastScroll = currentScroll;
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all feature cards and steps
document.querySelectorAll('.feature-card, .step').forEach(el => {
    observer.observe(el);
});

// Check if user is logged in and update navbar
if (isAuthenticated()) {
    const user = getCurrentUser();
    const navLinks = document.querySelector('.nav-links');

    if (user && navLinks) {
        let dashboardLink = '';

        switch (user.role) {
            case 'traveler':
                dashboardLink = 'traveler/dashboard.html';
                break;
            case 'provider':
                dashboardLink = 'provider/dashboard.html';
                break;
            case 'admin':
                dashboardLink = 'admin/dashboard.html';
                break;
        }

        navLinks.innerHTML = `
            <a href="${dashboardLink}">Dashboard</a>
            <a href="#" onclick="handleLogout(event)" class="btn btn-outline btn-sm">Logout</a>
        `;
    }
}

function handleLogout(e) {
    e.preventDefault();
    api.logout();
}
