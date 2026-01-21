from datetime import datetime
from . import db

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    traveler_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('storage_locations.id'), nullable=False)
    check_in = db.Column(db.DateTime, nullable=False)
    check_out = db.Column(db.DateTime, nullable=False)
    num_bags = db.Column(db.Integer, nullable=False, default=1)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, confirmed, active, completed, cancelled
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, refunded
    special_instructions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    review = db.relationship('Review', backref='booking', uselist=False, lazy=True)
    
    def to_dict(self):
        """Convert booking to dictionary"""
        return {
            'id': self.id,
            'traveler_id': self.traveler_id,
            'location_id': self.location_id,
            'check_in': self.check_in.isoformat(),
            'check_out': self.check_out.isoformat(),
            'num_bags': self.num_bags,
            'total_price': self.total_price,
            'status': self.status,
            'payment_status': self.payment_status,
            'special_instructions': self.special_instructions,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Booking {self.id} - {self.status}>'
