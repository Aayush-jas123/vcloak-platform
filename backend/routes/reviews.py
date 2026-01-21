from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Review, Booking, StorageLocation
from utils.auth_helpers import get_current_user
from utils.validators import validate_rating

reviews_bp = Blueprint('reviews', __name__, url_prefix='/api/reviews')

@reviews_bp.route('', methods=['POST'])
@jwt_required()
def create_review():
    """Submit a review for a completed booking"""
    data = request.get_json()
    current_user = get_current_user()
    
    # Validate required fields
    if 'booking_id' not in data or 'rating' not in data:
        return jsonify({'error': 'Booking ID and rating required'}), 400
    
    # Validate rating
    is_valid, error = validate_rating(data['rating'])
    if not is_valid:
        return jsonify({'error': error}), 400
    
    # Get booking
    booking = Booking.query.get(data['booking_id'])
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    # Check if user is the traveler
    if booking.traveler_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Check if booking is completed
    if booking.status != 'completed':
        return jsonify({'error': 'Can only review completed bookings'}), 400
    
    # Check if review already exists
    if Review.query.filter_by(booking_id=booking.id).first():
        return jsonify({'error': 'Review already submitted for this booking'}), 409
    
    # Create review
    review = Review(
        booking_id=booking.id,
        traveler_id=current_user.id,
        location_id=booking.location_id,
        rating=int(data['rating']),
        comment=data.get('comment', '')
    )
    
    try:
        db.session.add(review)
        
        # Update location rating
        location = StorageLocation.query.get(booking.location_id)
        all_reviews = Review.query.filter_by(location_id=location.id).all()
        total_rating = sum(r.rating for r in all_reviews) + review.rating
        location.rating = total_rating / (len(all_reviews) + 1)
        location.total_reviews = len(all_reviews) + 1
        
        db.session.commit()
        
        return jsonify({
            'message': 'Review submitted successfully',
            'review': review.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/location/<int:location_id>', methods=['GET'])
def get_location_reviews(location_id):
    """Get all reviews for a location"""
    location = StorageLocation.query.get(location_id)
    if not location:
        return jsonify({'error': 'Location not found'}), 404
    
    reviews = Review.query.filter_by(location_id=location_id).order_by(Review.created_at.desc()).all()
    
    return jsonify({
        'reviews': [review.to_dict() for review in reviews],
        'average_rating': location.rating,
        'total_reviews': location.total_reviews
    }), 200
