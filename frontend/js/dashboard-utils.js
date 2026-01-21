// Dashboard Utilities - Shared functions for dashboard pages

// Loading States
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="loading-spinner"><div class="spinner"></div><p>Loading...</p></div>';
    }
}

function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '';
    }
}

// Error Handling
function showError(message, elementId = 'error-container') {
    const container = document.getElementById(elementId);
    if (container) {
        container.innerHTML = `
            <div class="error-message">
                <span class="error-icon">⚠️</span>
                <span>${message}</span>
                <button onclick="this.parentElement.remove()" class="close-btn">×</button>
            </div>
        `;
        container.style.display = 'block';
    } else {
        // Fallback to alert if container doesn't exist
        alert(message);
    }
}

function clearError(elementId = 'error-container') {
    const container = document.getElementById(elementId);
    if (container) {
        container.innerHTML = '';
        container.style.display = 'none';
    }
}

// Toast Notifications
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="close-btn">×</button>
    `;

    document.body.appendChild(toast);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Date Formatting
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDateTime(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Currency Formatting
function formatCurrency(amount) {
    if (amount === null || amount === undefined) return '$0.00';
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Status Badge
function getStatusBadge(status) {
    const statusClasses = {
        'pending': 'badge-warning',
        'confirmed': 'badge-success',
        'completed': 'badge-info',
        'cancelled': 'badge-danger',
        'active': 'badge-success',
        'inactive': 'badge-secondary'
    };

    const className = statusClasses[status?.toLowerCase()] || 'badge-secondary';
    return `<span class="badge ${className}">${status}</span>`;
}

// Check Authentication
function checkAuth() {
    if (!isAuthenticated()) {
        window.location.href = '/login.html';
        return false;
    }
    return true;
}

// Populate User Info
function populateUserInfo() {
    const user = getCurrentUser();
    if (user) {
        const userNameElement = document.getElementById('user-name');
        const userEmailElement = document.getElementById('user-email');
        const userRoleElement = document.getElementById('user-role');

        if (userNameElement) userNameElement.textContent = user.name || 'User';
        if (userEmailElement) userEmailElement.textContent = user.email || '';
        if (userRoleElement) userRoleElement.textContent = user.role || '';
    }
}

// Handle API Errors
function handleApiError(error) {
    console.error('API Error:', error);

    if (error.message.includes('401') || error.message.includes('Unauthorized')) {
        showToast('Session expired. Please login again.', 'error');
        setTimeout(() => {
            window.location.href = '/login.html';
        }, 2000);
    } else if (error.message.includes('403') || error.message.includes('Forbidden')) {
        showToast('You do not have permission to access this resource.', 'error');
    } else if (error.message.includes('404')) {
        showToast('Resource not found.', 'error');
    } else if (error.message.includes('500')) {
        showToast('Server error. Please try again later.', 'error');
    } else {
        showToast(error.message || 'An error occurred. Please try again.', 'error');
    }
}

// Initialize Dashboard
function initDashboard() {
    // Check authentication
    if (!checkAuth()) return;

    // Populate user info
    populateUserInfo();

    // Add logout handler
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            await api.logout();
        });
    }
}

// Call init on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDashboard);
} else {
    initDashboard();
}
