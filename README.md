# vcloak - Secure Luggage Storage Platform 🧳

A full-stack web application connecting travelers with local storage providers for secure, temporary luggage storage.

**Live Platform**: https://vcloak-platform.onrender.com

## ✨ Features

### For Travelers
- 🔍 Search and browse storage locations with filters
- 📍 View location details with interactive Google Maps
- 📅 Book storage with real-time price calculation
- ⭐ Submit reviews and ratings
- 📊 Track booking history and spending analytics
- 👤 Manage profile and change password

### For Providers
- 📦 List and manage storage locations
- ✏️ Add amenities, capacity, and pricing
- 📋 Manage bookings with status updates
- 💰 Track earnings and performance
- 📈 View business analytics dashboard
- ⭐ Monitor customer ratings and reviews

### For Admins
- 👥 Manage users and verify providers
- 📊 Platform-wide analytics and insights
- 🔍 Oversee all bookings and locations
- 📈 Monitor revenue and growth metrics
- ✅ Verify and approve providers

## 🚀 Tech Stack

### Backend
- **Python 3.11.9** with Flask web framework
- **PostgreSQL** (NeonDB) for production database
- **SQLAlchemy** ORM for database operations
- **Flask-JWT-Extended** for authentication
- **Flask-CORS** for cross-origin requests
- **psycopg3** for PostgreSQL connectivity

### Frontend
- **HTML5, CSS3, JavaScript** (Vanilla)
- **Chart.js** for analytics visualizations
- **Google Maps API** for location mapping
- **Responsive Design** with CSS Grid and Flexbox
- **Modern UI/UX** with custom design system

### Deployment
- **Render.com** for hosting (auto-deploy from GitHub)
- **NeonDB** for PostgreSQL database
- **HTTPS** enabled by default
- **Environment Variables** for configuration

## 📦 Project Structure

```
vcloak/
├── backend/
│   ├── models/              # Database models (User, Location, Booking, Review)
│   ├── routes/              # API routes (auth, locations, bookings, reviews, admin)
│   ├── utils/               # Helper functions and decorators
│   ├── app.py               # Main Flask application
│   ├── config.py            # Configuration and environment variables
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── css/                 # Stylesheets (style.css, components.css)
│   ├── js/                  # JavaScript (api.js, dashboard-utils.js)
│   ├── traveler/            # Traveler interface (dashboard, search, booking, reviews)
│   ├── provider/            # Provider interface (dashboard, locations, bookings, analytics)
│   ├── admin/               # Admin interface (dashboard, users, providers, analytics)
│   ├── index.html           # Landing page
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── profile.html         # User profile
│   ├── location-details.html # Location details with map
│   └── ...                  # Other pages (404, error, password reset, etc.)
└── README.md
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL (or use NeonDB)
- Git

### Backend Setup

1. **Clone the repository**:
```bash
git clone https://github.com/Aayush-jas123/vcloak-platform.git
cd vcloak-platform
```

2. **Create virtual environment**:
```bash
cd backend
python -m venv venv
```

3. **Activate virtual environment**:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

5. **Set up environment variables**:
Create a `.env` file in the `backend/` directory:
```env
DATABASE_URL=postgresql://user:password@host/database
JWT_SECRET_KEY=your-secret-key-change-this
FRONTEND_URL=http://localhost:5500
```

6. **Run the Flask server**:
```bash
python app.py
```

Backend will run on `http://localhost:5000`

### Frontend Setup

1. **Update API URL** (for local development):
In `frontend/js/api.js`, change:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

2. **Serve frontend**:
```bash
# Using Python
cd frontend
python -m http.server 5500

# Or use any static file server
```

Frontend will be available at `http://localhost:5500`

## 🔐 Default Credentials

**Admin Account**:
- Email: `admin@vcloak.com`
- Password: `admin123`

**⚠️ Important**: Change admin password immediately in production!

## 📡 API Endpoints

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
- `PUT /api/bookings/:id` - Update booking status
- `GET /api/bookings/provider` - Get provider's bookings

### Reviews
- `POST /api/reviews` - Submit review
- `GET /api/reviews/location/:id` - Get location reviews

### Admin
- `GET /api/admin/stats` - Platform statistics
- `GET /api/admin/providers` - Get all providers
- `PUT /api/admin/providers/:id/verify` - Verify provider
- `GET /api/admin/users` - Get all users
- `PUT /api/admin/users/:id` - Update user
- `GET /api/admin/bookings` - Get all bookings

## 🗄️ Database Models

### User
- Email, password (hashed), name, role (admin/provider/traveler)
- Verification status, created date

### StorageLocation
- Business name, address, latitude, longitude
- Description, capacity, price per hour
- Amenities (JSON), active status, verified status
- Provider relationship

### Booking
- Check-in/check-out dates, number of bags
- Total price, status (pending/confirmed/active/completed/cancelled)
- Special instructions
- Traveler and location relationships

### Review
- Rating (1-5 stars), comment
- Traveler, location, and booking relationships
- Created date

## 🎨 Features Implemented

### Phase 1: Foundation
- ✅ JWT authentication and authorization
- ✅ Role-based access control
- ✅ Error handling and loading states
- ✅ Toast notifications

### Phase 2: Core Pages
- ✅ Admin management pages
- ✅ Traveler search functionality
- ✅ All role dashboards

### Phase 3: Provider Features
- ✅ Location management system
- ✅ Location creation and editing
- ✅ Amenities and capacity management

### Phase 4: Booking Flow
- ✅ Complete booking workflow
- ✅ Real-time price calculation
- ✅ Review and rating system
- ✅ Provider booking management

### Phase 5: Security & Polish
- ✅ Profile management
- ✅ Password change functionality
- ✅ Error pages (404, generic)
- ✅ UI/UX polish

### Phase 6: Advanced Features
- ✅ Google Maps integration
- ✅ Email verification flow (frontend)
- ✅ Password reset system (frontend)
- ✅ Advanced analytics dashboards with Chart.js

## 📊 Analytics Dashboards

All roles have comprehensive analytics with interactive charts:

- **Admin**: Revenue trends, user growth, booking patterns, top locations
- **Provider**: Earnings, location performance, ratings, peak hours
- **Traveler**: Spending tracking, booking history, favorite locations

## 🔒 Security Features

- JWT-based authentication with access tokens
- Password hashing with Werkzeug
- Role-based access control (@role_required decorator)
- HTTPS enabled on production
- Input validation and sanitization
- CORS configuration

## 🚀 Deployment

The platform is deployed on **Render.com** with auto-deployment from GitHub.

**Live URL**: https://vcloak-platform.onrender.com

### Deploy Your Own

1. Fork this repository
2. Create account on [Render.com](https://render.com)
3. Create new Web Service
4. Connect your GitHub repository
5. Set environment variables:
   - `DATABASE_URL` (from NeonDB or your PostgreSQL)
   - `JWT_SECRET_KEY`
6. Deploy!

## 🧪 Testing

### Manual Testing
1. Register as traveler and provider
2. Create storage locations as provider
3. Search and book as traveler
4. Manage bookings as provider
5. Verify providers as admin

### Test Accounts
Create test accounts for each role to test all features.

## 📝 License

MIT License - feel free to use this project for learning or commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Contact

For questions or support:
- GitHub: [Aayush-jas123](https://github.com/Aayush-jas123)
- Platform: https://vcloak-platform.onrender.com

## 🎉 Acknowledgments

Built with ❤️ using Flask, PostgreSQL, and modern web technologies.

---

**Status**: ✅ Production-Ready | **Version**: 1.0.0 | **Last Updated**: January 2026
