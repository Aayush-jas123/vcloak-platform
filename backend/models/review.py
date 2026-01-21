from datetime import datetime
from . import db

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False, unique=True)
    traveler_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('storage_locations.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert review to dictionary"""
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'traveler_id': self.traveler_id,
            'location_id': self.location_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat(),
            'traveler_name': self.reviewer.name if self.reviewer else None
        }
    
    def __repr__(self):
        return f'<Review {self.id} - Rating: {self.rating}>'
