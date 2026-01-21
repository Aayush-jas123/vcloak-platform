# vcloak - Secure Luggage Storage Platform

A full-stack web application connecting travelers with local storage providers for secure, temporary luggage storage.

## Features

- **For Travelers**: Search and book secure luggage storage locations
- **For Providers**: List storage spaces and manage bookings
- **For Admins**: Verify providers and oversee platform operations

## Tech Stack

### Backend
- Python Flask
- SQLAlchemy ORM
- SQLite (development) / PostgreSQL (production)
- Flask-JWT-Extended for authentication
- Flask-CORS for cross-origin requests

### Frontend
- HTML5, CSS3, JavaScript (ES6+)
- Modern design system with CSS variables
- Responsive design
- RESTful API integration

## Project Structure

```
vcloak/
├── backend/
│   ├── models/          # Database models
│   ├── routes/          # API routes
│   ├── utils/           # Helper functions
│   ├── app.py           # Main Flask application
│   ├── config.py        # Configuration
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   ├── traveler/        # Traveler interface
│   ├── provider/        # Provider interface
│   ├── admin/           # Admin interface
│   └── index.html       # Landing page
└── README.md
```

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and update values:
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

5. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Open `frontend/index.html` in a web browser, or use a local server:
```bash
# Using Python
cd frontend
python -m http.server 5500

# Using Node.js (if you have http-server installed)
npx http-server frontend -p 5500
```

The frontend will be available at `http://localhost:5500`

## Default Admin Credentials

- Email: `admin@vcloak.com`
- Password: `admin123`

**Important**: Change these credentials in production!

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info

### Locations
- `GET /api/locations` - Get all locations
- `POST /api/locations` - Create location (providers only)
- `GET /api/locations/:id` - Get location details
- `PUT /api/locations/:id` - Update location
- `DELETE /api/locations/:id` - Delete location
- `GET /api/locations/nearby` - Get nearby locations

### Bookings
- `GET /api/bookings` - Get user's bookings
- `POST /api/bookings` - Create booking
- `GET /api/bookings/:id` - Get booking details
- `PUT /api/bookings/:id` - Update booking
- `GET /api/bookings/provider` - Get provider's bookings

### Reviews
- `POST /api/reviews` - Submit review
- `GET /api/reviews/location/:id` - Get location reviews

### Admin
- `GET /api/admin/stats` - Platform statistics
- `GET /api/admin/providers` - Get providers
- `PUT /api/admin/providers/:id/verify` - Verify provider
- `GET /api/admin/users` - Get all users
- `PUT /api/admin/users/:id` - Update user
- `GET /api/admin/bookings` - Get all bookings

## Development

### Database Models

- **User**: Travelers, providers, and admins
- **StorageLocation**: Storage facilities with geolocation
- **Booking**: Luggage storage bookings
- **Review**: User reviews for locations

### Authentication

JWT-based authentication with access and refresh tokens. Tokens are stored in localStorage on the frontend.

## License

MIT License

## Contact

For questions or support, please contact the development team.
