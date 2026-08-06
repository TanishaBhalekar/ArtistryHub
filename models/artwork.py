from datetime import datetime
from models import db

class Artwork(db.Model):
    __tablename__ = 'artworks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    medium = db.Column(db.String(50), nullable=True)  # e.g., Digital, Oil, Watercolor, 3D Model
    category = db.Column(db.String(50), nullable=True, index=True) # e.g., Portrait, Landscape, Concept Art
    tags = db.Column(db.String(255), nullable=True)     # Comma-separated tags
    visibility = db.Column(db.String(20), nullable=False, default='public') # public, private, unlisted
    image_url = db.Column(db.String(255), nullable=True)
    thumbnail_url = db.Column(db.String(255), nullable=True)
    
    # Foreign key relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Artwork {self.title}>'
