// API Configuration
const API_BASE_URL = window.location.origin + '/api';

// Get auth token from localStorage
function getAuthToken() {
    return localStorage.getItem('access_token');
}

// Set auth token
function setAuthToken(token) {
    localStorage.setItem('access_token', token);
}

// Remove auth token
function removeAuthToken() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
}

// Get current user
function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

// Set current user
function setCurrentUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

// API Client
const api = {
    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const token = getAuthToken();

        const config = {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
        };

        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    // Auth endpoints
    async register(userData) {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData),
        });
    },

    async login(credentials) {
        const data = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify(credentials),
        });

        if (data.access_token) {
            setAuthToken(data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
            setCurrentUser(data.user);
        }

        return data;
    },

    async logout() {
        removeAuthToken();
        window.location.href = '/frontend/index.html';
    },

    async getCurrentUser() {
        return this.request('/auth/me');
    },

    // Location endpoints
    async getLocations(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/locations?${queryString}`);
    },

    async getLocation(id) {
        return this.request(`/locations/${id}`);
    },

    async createLocation(locationData) {
        return this.request('/locations', {
            method: 'POST',
            body: JSON.stringify(locationData),
        });
    },

    async updateLocation(id, locationData) {
        return this.request(`/locations/${id}`, {
            method: 'PUT',
            body: JSON.stringify(locationData),
        });
    },

    async deleteLocation(id) {
        return this.request(`/locations/${id}`, {
            method: 'DELETE',
        });
    },

    async getNearbyLocations(lat, lng, radius = 5) {
        return this.request(`/locations/nearby?lat=${lat}&lng=${lng}&radius=${radius}`);
    },

    // Booking endpoints
    async getBookings(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/bookings?${queryString}`);
    },

    async getBooking(id) {
        return this.request(`/bookings/${id}`);
    },

    async createBooking(bookingData) {
        return this.request('/bookings', {
            method: 'POST',
            body: JSON.stringify(bookingData),
        });
    },

    async updateBooking(id, bookingData) {
        return this.request(`/bookings/${id}`, {
            method: 'PUT',
            body: JSON.stringify(bookingData),
        });
    },

    async getProviderBookings() {
        return this.request('/bookings/provider');
    },

    // Review endpoints
    async createReview(reviewData) {
        return this.request('/reviews', {
            method: 'POST',
            body: JSON.stringify(reviewData),
        });
    },

    async getLocationReviews(locationId) {
        return this.request(`/reviews/location/${locationId}`);
    },

    // Admin endpoints
    async getAdminStats() {
        return this.request('/admin/stats');
    },

    async getProviders(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/admin/providers?${queryString}`);
    },

    async verifyProvider(providerId, verifyLocations = false) {
        return this.request(`/admin/providers/${providerId}/verify`, {
            method: 'PUT',
            body: JSON.stringify({ verify_locations: verifyLocations }),
        });
    },

    async verifyLocation(locationId) {
        return this.request(`/admin/locations/${locationId}/verify`, {
            method: 'PUT',
        });
    },

    async getAllUsers(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/admin/users?${queryString}`);
    },

    async updateUser(userId, userData) {
        return this.request(`/admin/users/${userId}`, {
            method: 'PUT',
            body: JSON.stringify(userData),
        });
    },

    async getAllBookings(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/admin/bookings?${queryString}`);
    },
};

// Check if user is authenticated
function isAuthenticated() {
    return !!getAuthToken();
}

// Redirect if not authenticated
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = '/frontend/login.html';
        return false;
    }
    return true;
}

// Redirect if not correct role
function requireRole(role) {
    const user = getCurrentUser();
    if (!user || user.role !== role) {
        window.location.href = '/frontend/index.html';
        return false;
    }
    return true;
}
