from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.user import User
from models.artwork import Artwork
from models.commission import Commission, CommissionStatus, PaymentStatus

__all__ = ['db', 'User', 'Artwork', 'Commission', 'CommissionStatus', 'PaymentStatus']
