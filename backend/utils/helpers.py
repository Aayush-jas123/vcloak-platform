import math
from datetime import datetime

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in kilometers using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return round(distance, 2)

def calculate_price(check_in, check_out, price_per_hour):
    """Calculate total price based on duration and hourly rate"""
    if isinstance(check_in, str):
        check_in = datetime.fromisoformat(check_in.replace('Z', '+00:00'))
    if isinstance(check_out, str):
        check_out = datetime.fromisoformat(check_out.replace('Z', '+00:00'))
    
    duration = (check_out - check_in).total_seconds() / 3600  # hours
    total_price = duration * price_per_hour
    return round(total_price, 2)

def format_datetime(dt):
    """Format datetime for display"""
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-%d %H:%M:%S')
