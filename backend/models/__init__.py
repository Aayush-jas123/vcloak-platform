from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .storage_location import StorageLocation
from .booking import Booking
from .review import Review

__all__ = ['db', 'User', 'StorageLocation', 'Booking', 'Review']
