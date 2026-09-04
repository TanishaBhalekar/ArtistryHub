import enum
from datetime import datetime
from models import db

class CommissionStatus(str, enum.Enum):
    REQUESTED = 'Requested'
    ACCEPTED = 'Accepted'
    SKETCH = 'Sketch'
    COLORING = 'Coloring'
    REVISION = 'Revision'
    DELIVERED = 'Delivered'

class PaymentStatus(str, enum.Enum):
    UNPAID = 'unpaid'
    DEPOSIT_PAID = 'deposit_paid'
    PAID_IN_FULL = 'paid_in_full'
    REFUNDED = 'refunded'

class Commission(db.Model):
    __tablename__ = 'commissions'

    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key mapping artist (User)
    artist_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Client Details
    client_name = db.Column(db.String(100), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    client_notes = db.Column(db.Text, nullable=True)
    
    # Commission Details
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    medium = db.Column(db.String(50), nullable=True, default='Digital 2D')
    priority = db.Column(db.String(20), nullable=True, default='Normal')  # High, Normal, Urgent
    deadline = db.Column(db.DateTime, nullable=True)
    
    # Status Enums
    status = db.Column(db.Enum(CommissionStatus), default=CommissionStatus.REQUESTED, nullable=False, index=True)
    payment_status = db.Column(db.Enum(PaymentStatus), default=PaymentStatus.UNPAID, nullable=False)
    
    # Milestone Checkbox States
    accepted_done = db.Column(db.Boolean, default=True)
    sketch_done = db.Column(db.Boolean, default=False)
    render_done = db.Column(db.Boolean, default=False)
    delivered_done = db.Column(db.Boolean, default=False)

    # Accounting & Revisions
    revision_count = db.Column(db.Integer, default=0, nullable=False)
    cost = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    deliverables = db.relationship('CommissionDeliverable', backref='commission', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Commission {self.title} - Status: {self.status.value}>'


class CommissionDeliverable(db.Model):
    __tablename__ = 'commission_deliverables'

    id = db.Column(db.Integer, primary_key=True)
    commission_id = db.Column(db.Integer, db.ForeignKey('commissions.id', ondelete='CASCADE'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    version_tag = db.Column(db.String(20), default='v1')  # v1, v2, v3, final
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
