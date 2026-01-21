from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, StorageLocation
from utils.auth_helpers import role_required, get_current_user
from utils.validators import validate_coordinates
from utils.helpers import calculate_distance
import json

locations_bp = Blueprint('locations', __name__, url_prefix='/api/locations')

@locations_bp.route('', methods=['GET'])
def get_locations():
    """Get all storage locations with optional filters"""
    # Get query parameters
    city = request.args.get('city')
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radius = request.args.get('radius', 10, type=float)  # km
    verified_only = request.args.get('verified', 'false').lower() == 'true'
    
    query = StorageLocation.query.filter_by(active=True)
    
    if verified_only:
        query = query.filter_by(verified=True)
    
    locations = query.all()
    
    # Filter by distance if coordinates provided
    if lat and lng:
        locations_with_distance = []
        for loc in locations:
            distance = calculate_distance(lat, lng, loc.latitude, loc.longitude)
            if distance <= radius:
                loc_dict = loc.to_dict()
                loc_dict['distance'] = distance
                locations_with_distance.append(loc_dict)
        
        # Sort by distance
        locations_with_distance.sort(key=lambda x: x['distance'])
        return jsonify({'locations': locations_with_distance}), 200
    
    return jsonify({'locations': [loc.to_dict() for loc in locations]}), 200

@locations_bp.route('', methods=['POST'])
@jwt_required()
@role_required('provider')
def create_location():
    """Create a new storage location (providers only)"""
    data = request.get_json()
    current_user = get_current_user()
    
    # Validate required fields
    required_fields = ['business_name', 'address', 'latitude', 'longitude', 'capacity', 'price_per_hour']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate coordinates
    is_valid, error = validate_coordinates(data['latitude'], data['longitude'])
    if not is_valid:
        return jsonify({'error': error}), 400
    
    # Create location
    location = StorageLocation(
        provider_id=current_user.id,
        business_name=data['business_name'],
        address=data['address'],
        latitude=float(data['latitude']),
        longitude=float(data['longitude']),
        capacity=int(data['capacity']),
        price_per_hour=float(data['price_per_hour']),
        amenities=json.dumps(data.get('amenities', [])),
        photos=json.dumps(data.get('photos', [])),
        description=data.get('description', '')
    )
    
    try:
        db.session.add(location)
        db.session.commit()
        return jsonify({
            'message': 'Location created successfully',
            'location': location.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@locations_bp.route('/<int:location_id>', methods=['GET'])
def get_location(location_id):
    """Get a specific location by ID"""
    location = StorageLocation.query.get(location_id)
    
    if not location:
        return jsonify({'error': 'Location not found'}), 404
    
    return jsonify({'location': location.to_dict()}), 200

@locations_bp.route('/<int:location_id>', methods=['PUT'])
@jwt_required()
@role_required('provider')
def update_location(location_id):
    """Update a storage location"""
    current_user = get_current_user()
    location = StorageLocation.query.get(location_id)
    
    if not location:
        return jsonify({'error': 'Location not found'}), 404
    
    # Check if user owns this location
    if location.provider_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Update fields
    if 'business_name' in data:
        location.business_name = data['business_name']
    if 'address' in data:
        location.address = data['address']
    if 'capacity' in data:
        location.capacity = int(data['capacity'])
    if 'price_per_hour' in data:
        location.price_per_hour = float(data['price_per_hour'])
    if 'amenities' in data:
        location.amenities = json.dumps(data['amenities'])
    if 'photos' in data:
        location.photos = json.dumps(data['photos'])
    if 'description' in data:
        location.description = data['description']
    if 'active' in data:
        location.active = bool(data['active'])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Location updated successfully',
            'location': location.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@locations_bp.route('/<int:location_id>', methods=['DELETE'])
@jwt_required()
@role_required('provider')
def delete_location(location_id):
    """Delete a storage location"""
    current_user = get_current_user()
    location = StorageLocation.query.get(location_id)
    
    if not location:
        return jsonify({'error': 'Location not found'}), 404
    
    if location.provider_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Soft delete
        location.active = False
        db.session.commit()
        return jsonify({'message': 'Location deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@locations_bp.route('/nearby', methods=['GET'])
def get_nearby_locations():
    """Get storage locations near a specific coordinate"""
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radius = request.args.get('radius', 5, type=float)  # default 5km
    
    if not lat or not lng:
        return jsonify({'error': 'Latitude and longitude required'}), 400
    
    is_valid, error = validate_coordinates(lat, lng)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    locations = StorageLocation.query.filter_by(active=True, verified=True).all()
    
    nearby_locations = []
    for loc in locations:
        distance = calculate_distance(lat, lng, loc.latitude, loc.longitude)
        if distance <= radius:
            loc_dict = loc.to_dict()
            loc_dict['distance'] = distance
            nearby_locations.append(loc_dict)
    
    # Sort by distance
    nearby_locations.sort(key=lambda x: x['distance'])
    
    return jsonify({'locations': nearby_locations}), 200
