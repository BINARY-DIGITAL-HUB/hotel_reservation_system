
from app import db, login_manager
from flask_login import UserMixin
import uuid
from datetime import datetime
from sqlalchemy import CheckConstraint, Numeric


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reservations = db.relationship('Reservation', back_populates='user', lazy=True)


class Room(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(20), unique=True, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(Numeric(10, 2), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    bed_type = db.Column(db.String(50))
    facilities = db.Column(db.Text)
    image = db.Column(db.String(255))
    status = db.Column(db.String(20), default='Available', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reservations = db.relationship('Reservation', back_populates='room', lazy=True)

    __table_args__ = (
        CheckConstraint('price >= 0', name='valid_room_price'),
        CheckConstraint('capacity > 0', name='valid_room_capacity')
    )


class Reservation(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    booking_reference = db.Column(db.String(30), unique=True, nullable=False, default=lambda: f"HTL-{uuid.uuid4().hex[:10].upper()}")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    number_of_guests = db.Column(db.Integer, nullable=False, default=1)
    total_amount = db.Column(Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    special_request = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='reservations')
    room = db.relationship('Room', back_populates='reservations')

    __table_args__ = (
        CheckConstraint('check_out > check_in', name='valid_reservation_dates'),
        CheckConstraint('number_of_guests > 0', name='valid_number_of_guests'),
        CheckConstraint('total_amount >= 0', name='valid_reservation_amount')
    )


class LogReservation(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False) # e.g., 'Created', 'Modified', 'Cancelled'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    reservation = db.relationship('Reservation', backref=db.backref('logs', lazy=True))
