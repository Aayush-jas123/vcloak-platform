import re
from email_validator import validate_email, EmailNotValidError

def validate_email_address(email):
    """Validate email format"""
    try:
        validate_email(email)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)

def validate_phone(phone):
    """Validate phone number format"""
    if not phone:
        return True, None
    
    # Basic phone validation (10-15 digits with optional + and spaces)
    pattern = r'^\+?[\d\s-]{10,15}$'
    if re.match(pattern, phone):
        return True, None
    return False, "Invalid phone number format"

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, None

def validate_rating(rating):
    """Validate rating value"""
    try:
        rating = int(rating)
        if 1 <= rating <= 5:
            return True, None
        return False, "Rating must be between 1 and 5"
    except (ValueError, TypeError):
        return False, "Invalid rating value"

def validate_coordinates(lat, lng):
    """Validate latitude and longitude"""
    try:
        lat = float(lat)
        lng = float(lng)
        if -90 <= lat <= 90 and -180 <= lng <= 180:
            return True, None
        return False, "Invalid coordinates range"
    except (ValueError, TypeError):
        return False, "Invalid coordinate values"
