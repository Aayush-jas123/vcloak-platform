from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, User, StorageLocation, Booking
from utils.auth_helpers import role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_stats():
    """Get platform statistics"""
    total_users = User.query.count()
    total_travelers = User.query.filter_by(role='traveler').count()
    total_providers = User.query.filter_by(role='provider').count()
    total_locations = StorageLocation.query.count()
    verified_locations = StorageLocation.query.filter_by(verified=True).count()
    total_bookings = Booking.query.count()
    active_bookings = Booking.query.filter_by(status='active').count()
    completed_bookings = Booking.query.filter_by(status='completed').count()
    
    return jsonify({
        'stats': {
            'total_users': total_users,
            'total_travelers': total_travelers,
            'total_providers': total_providers,
            'total_locations': total_locations,
            'verified_locations': verified_locations,
            'pending_verification': total_locations - verified_locations,
            'total_bookings': total_bookings,
            'active_bookings': active_bookings,
            'completed_bookings': completed_bookings
        }
    }), 200

@admin_bp.route('/providers', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_providers():
    """Get all providers with their locations"""
    verified = request.args.get('verified')
    
    query = User.query.filter_by(role='provider')
    
    providers = query.all()
    
    providers_data = []
    for provider in providers:
        provider_dict = provider.to_dict()
        locations = StorageLocation.query.filter_by(provider_id=provider.id).all()
        
        if verified == 'false':
            locations = [loc for loc in locations if not loc.verified]
        elif verified == 'true':
            locations = [loc for loc in locations if loc.verified]
        
        provider_dict['locations'] = [loc.to_dict() for loc in locations]
        providers_data.append(provider_dict)
    
    return jsonify({'providers': providers_data}), 200

@admin_bp.route('/providers/<int:provider_id>/verify', methods=['PUT'])
@jwt_required()
@role_required('admin')
def verify_provider(provider_id):
    """Verify a provider and their locations"""
    provider = User.query.get(provider_id)
    
    if not provider:
        return jsonify({'error': 'Provider not found'}), 404
    
    if provider.role != 'provider':
        return jsonify({'error': 'User is not a provider'}), 400
    
    # Verify provider
    provider.verified = True
    
    # Optionally verify all their locations
    data = request.get_json() or {}
    if data.get('verify_locations', False):
        locations = StorageLocation.query.filter_by(provider_id=provider_id).all()
        for location in locations:
            location.verified = True
    
    try:
        db.session.commit()
        return jsonify({'message': 'Provider verified successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/locations/<int:location_id>/verify', methods=['PUT'])
@jwt_required()
@role_required('admin')
def verify_location(location_id):
    """Verify a specific location"""
    location = StorageLocation.query.get(location_id)
    
    if not location:
        return jsonify({'error': 'Location not found'}), 404
    
    location.verified = True
    
    try:
        db.session.commit()
        return jsonify({'message': 'Location verified successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_users():
    """Get all users"""
    role = request.args.get('role')
    
    query = User.query
    
    if role:
        query = query.filter_by(role=role)
    
    users = query.all()
    
    return jsonify({'users': [user.to_dict() for user in users]}), 200

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_user(user_id):
    """Update user status (suspend/activate)"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'verified' in data:
        user.verified = bool(data['verified'])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/bookings', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_bookings():
    """Get all bookings for oversight"""
    status = request.args.get('status')
    
    query = Booking.query
    
    if status:
        query = query.filter_by(status=status)
    
    bookings = query.order_by(Booking.created_at.desc()).limit(100).all()
    
    bookings_data = []
    for booking in bookings:
        booking_dict = booking.to_dict()
        booking_dict['location'] = booking.location.to_dict()
        booking_dict['traveler'] = booking.traveler.to_dict()
        bookings_data.append(booking_dict)
    
    return jsonify({'bookings': bookings_data}), 200
