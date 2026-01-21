from datetime import datetime
from . import db

class StorageLocation(db.Model):
    __tablename__ = 'storage_locations'
    
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    business_name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=10)
    price_per_hour = db.Column(db.Float, nullable=False)
    amenities = db.Column(db.Text)  # JSON string: ["secure", "cctv", "24/7", "indoor"]
    photos = db.Column(db.Text)  # JSON string: ["url1", "url2"]
    description = db.Column(db.Text)
    rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)
    verified = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='location', lazy=True)
    reviews = db.relationship('Review', backref='location', lazy=True)
    
    def to_dict(self):
        """Convert location to dictionary"""
        import json
        return {
            'id': self.id,
            'provider_id': self.provider_id,
            'business_name': self.business_name,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'capacity': self.capacity,
            'price_per_hour': self.price_per_hour,
            'amenities': json.loads(self.amenities) if self.amenities else [],
            'photos': json.loads(self.photos) if self.photos else [],
            'description': self.description,
            'rating': round(self.rating, 1),
            'total_reviews': self.total_reviews,
            'verified': self.verified,
            'active': self.active,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<StorageLocation {self.business_name}>'
