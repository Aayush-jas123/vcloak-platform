from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from models import db, Booking, StorageLocation
from utils.auth_helpers import role_required, get_current_user
from utils.helpers import calculate_price

bookings_bp = Blueprint('bookings', __name__, url_prefix='/api/bookings')

@bookings_bp.route('', methods=['GET'])
@jwt_required()
def get_bookings():
    """Get user's bookings"""
    current_user = get_current_user()
    
    # Get query parameters
    status = request.args.get('status')
    
    query = Booking.query.filter_by(traveler_id=current_user.id)
    
    if status:
        query = query.filter_by(status=status)
    
    bookings = query.order_by(Booking.created_at.desc()).all()
    
    # Include location details
    bookings_data = []
    for booking in bookings:
        booking_dict = booking.to_dict()
        booking_dict['location'] = booking.location.to_dict() if booking.location else None
        bookings_data.append(booking_dict)
    
    return jsonify({'bookings': bookings_data}), 200

@bookings_bp.route('', methods=['POST'])
@jwt_required()
@role_required('traveler')
def create_booking():
    """Create a new booking"""
    data = request.get_json()
    current_user = get_current_user()
    
    # Validate required fields
    required_fields = ['location_id', 'check_in', 'check_out', 'num_bags']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Get location
    location = StorageLocation.query.get(data['location_id'])
    if not location:
        return jsonify({'error': 'Location not found'}), 404
    
    if not location.active or not location.verified:
        return jsonify({'error': 'Location not available'}), 400
    
    # Parse dates
    try:
        check_in = datetime.fromisoformat(data['check_in'].replace('Z', '+00:00'))
        check_out = datetime.fromisoformat(data['check_out'].replace('Z', '+00:00'))
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    
    if check_out <= check_in:
        return jsonify({'error': 'Check-out must be after check-in'}), 400
    
    # Calculate price
    total_price = calculate_price(check_in, check_out, location.price_per_hour)
    
    # Create booking
    booking = Booking(
        traveler_id=current_user.id,
        location_id=location.id,
        check_in=check_in,
        check_out=check_out,
        num_bags=int(data['num_bags']),
        total_price=total_price,
        special_instructions=data.get('special_instructions'),
        status='confirmed'
    )
    
    try:
        db.session.add(booking)
        db.session.commit()
        
        booking_dict = booking.to_dict()
        booking_dict['location'] = location.to_dict()
        
        return jsonify({
            'message': 'Booking created successfully',
            'booking': booking_dict
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bookings_bp.route('/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
    """Get a specific booking"""
    current_user = get_current_user()
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    # Check authorization
    if booking.traveler_id != current_user.id and booking.location.provider_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    booking_dict = booking.to_dict()
    booking_dict['location'] = booking.location.to_dict()
    booking_dict['traveler'] = booking.traveler.to_dict()
    
    return jsonify({'booking': booking_dict}), 200

@bookings_bp.route('/<int:booking_id>', methods=['PUT'])
@jwt_required()
def update_booking(booking_id):
    """Update booking status"""
    current_user = get_current_user()
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    data = request.get_json()
    
    # Travelers can cancel, providers can update status
    if booking.traveler_id == current_user.id:
        if 'status' in data and data['status'] == 'cancelled':
            booking.status = 'cancelled'
    elif booking.location.provider_id == current_user.id:
        if 'status' in data:
            booking.status = data['status']
    else:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Booking updated successfully',
            'booking': booking.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bookings_bp.route('/provider', methods=['GET'])
@jwt_required()
@role_required('provider')
def get_provider_bookings():
    """Get bookings for provider's locations"""
    current_user = get_current_user()
    
    # Get all locations owned by provider
    locations = StorageLocation.query.filter_by(provider_id=current_user.id).all()
    location_ids = [loc.id for loc in locations]
    
    # Get bookings for these locations
    bookings = Booking.query.filter(Booking.location_id.in_(location_ids)).order_by(Booking.check_in.desc()).all()
    
    bookings_data = []
    for booking in bookings:
        booking_dict = booking.to_dict()
        booking_dict['location'] = booking.location.to_dict()
        booking_dict['traveler'] = booking.traveler.to_dict()
        bookings_data.append(booking_dict)
    
    return jsonify({'bookings': bookings_data}), 200
