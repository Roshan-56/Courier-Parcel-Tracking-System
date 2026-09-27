"""Database models for the Courier & Parcel Tracking System."""
from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

# Canonical, ordered list of shipment statuses (the delivery lifecycle).
STATUS_FLOW = ["Booked", "In Transit", "Out for Delivery", "Delivered"]


class Staff(UserMixin, db.Model):
    """A staff member who can log in to manage shipments."""

    __tablename__ = "staff"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Shipment(db.Model):
    """A parcel being tracked from origin to destination."""

    __tablename__ = "shipment"

    id = db.Column(db.Integer, primary_key=True)
    tracking_no = db.Column(db.String(20), unique=True, nullable=False, index=True)
    sender = db.Column(db.String(120), nullable=False)
    receiver = db.Column(db.String(120), nullable=False)
    origin = db.Column(db.String(120), nullable=False)
    destination = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(40), nullable=False, default="Booked")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    events = db.relationship(
        "TrackingEvent",
        backref="shipment",
        cascade="all, delete-orphan",
        order_by="TrackingEvent.timestamp",
    )

    @property
    def timeline(self):
        """Events ordered oldest -> newest for display."""
        return sorted(self.events, key=lambda e: e.timestamp)


class TrackingEvent(db.Model):
    """A single scan/update in a shipment's journey."""

    __tablename__ = "tracking_event"

    id = db.Column(db.Integer, primary_key=True)
    shipment_id = db.Column(
        db.Integer, db.ForeignKey("shipment.id"), nullable=False, index=True
    )
    status = db.Column(db.String(40), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    note = db.Column(db.String(255), nullable=True)
