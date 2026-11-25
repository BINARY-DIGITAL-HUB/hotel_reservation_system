from app import app
from flask import render_template, request, redirect, url_for, flash
from app.database import db, User, Room, Reservation, LogReservation
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, date
from secrets import token_hex




@app.route('/')
def index():
    return render_template("index.html")



@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        print(f"User: {user}, Password: {password}")  # Debugging line

        if user and check_password_hash(user.password, password):

            login_user(user)

            flash('Welcome back!', 'success')

            return redirect(url_for('dashboard'))

        flash('Invalid email or password.', 'danger')

    return render_template('login.html')





@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()

        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not all([first_name, last_name, email, phone, password]):
            flash('Please complete all required fields.', 'danger')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        new_guest = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            password=hashed_password
        )

        db.session.add(new_guest)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')

        return redirect(url_for('login'))

    return render_template('register.html')




@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))



@app.route('/reservation/<int:room_id>', methods=['GET', 'POST'])
@login_required
def make_reservation(room_id):

    room = Room.query.get_or_404(room_id)

    # Check room operational status
    if room.status != 'Available':
        flash('Sorry, this room is currently unavailable.', 'warning')
        return redirect(url_for('available_rooms'))

    if request.method == 'POST':

        try:
            # Retrieve form data
            check_in = date.fromisoformat(
                request.form.get('check_in', '')
            )

            check_out = date.fromisoformat(
                request.form.get('check_out', '')
            )

            number_of_guests = int(
                request.form.get('number_of_guests', 0)
            )

            special_request = request.form.get(
                'special_request', ''
            ).strip()

            # Validate check-in date
            if check_in < date.today():
                flash('Check-in date cannot be in the past.', 'danger')
                return redirect(url_for('reservation', room_id=room.id))

            # Validate check-out date
            if check_out <= check_in:
                flash('Check-out date must be after check-in date.', 'danger')
                return redirect(url_for('reservation', room_id=room.id))

            # Validate number of guests
            if number_of_guests < 1 or number_of_guests > room.capacity:
                flash(
                    f'This room accommodates between 1 and {room.capacity} guests.',
                    'danger'
                )
                return redirect(url_for('reservation', room_id=room.id))

            # Check room availability for selected dates
            existing_reservation = Reservation.query.filter(
                Reservation.room_id == room.id,
                Reservation.status.in_(['Pending', 'Confirmed']),
                Reservation.check_in < check_out,
                Reservation.check_out > check_in
            ).first()

            if existing_reservation:
                flash(
                    'Sorry, this room is already reserved for the selected dates.',
                    'danger'
                )
                return redirect(url_for('reservation', room_id=room.id))

            # Calculate total amount
            number_of_nights = (check_out - check_in).days

            total_amount = number_of_nights * room.price

            # Generate unique booking reference
            booking_reference = f"BK-{token_hex(5).upper()}"

            # Create reservation
            new_reservation = Reservation(
                booking_reference=booking_reference,
                user_id=current_user.id,
                room_id=room.id,
                check_in=check_in,
                check_out=check_out,
                number_of_guests=number_of_guests,
                total_amount=total_amount,
                status='Pending',
                special_request=special_request
            )

            # Save reservation
            db.session.add(new_reservation)
            db.session.commit()

            flash(
                f'Reservation submitted successfully! Your booking reference is {booking_reference}.',
                'success'
            )

            return redirect(url_for('manage_bookings'))

        except (ValueError, TypeError):
            db.session.rollback()
            flash('Please provide valid reservation information.', 'danger')

        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")  # Debugging line
            flash('An error occurred while processing your reservation.', 'danger')

    # Display reservation form
    return render_template(
        'make_reservation.html',
        room=room,
        user=current_user,
        today=date.today().isoformat()
    )








@app.route('/dashboard')
@login_required
def dashboard():

    today = date.today()

    # Retrieve reservations belonging to the logged-in user
    reservations_query = Reservation.query.filter_by(
        user_id=current_user.id
    )

    # Total reservations
    total_bookings = reservations_query.count()

    # Upcoming reservations
    upcoming_bookings = Reservation.query.filter(
        Reservation.user_id == current_user.id,
        Reservation.check_in >= today,
        Reservation.status.in_(['Pending', 'Confirmed'])
    ).count()

    # Cancelled reservations
    cancelled_bookings = Reservation.query.filter_by(
        user_id=current_user.id,
        status='Cancelled'
    ).count()

    # Retrieve recent reservations
    reservations = reservations_query.order_by(
        Reservation.created_at.desc()
    ).limit(5).all()


    # fect log total created, modified, cancelled reservations
    log_total_created = LogReservation.query.filter_by(action='Created').count()
    log_total_modified = LogReservation.query.filter_by(action='Modified').count()
    log_total_cancelled = LogReservation.query.filter_by(action='Cancelled').count()

    return render_template(
        'dashboard.html',
        user=current_user,
        total_bookings=total_bookings,
        upcoming_bookings=upcoming_bookings,
        cancelled_bookings=cancelled_bookings,
        reservations=reservations,
        log_total_created=log_total_created,
        log_total_modified=log_total_modified,
        log_total_cancelled=log_total_cancelled
    )





@app.route('/available-rooms', methods=['GET'])
@login_required
def available_rooms():

    check_in = request.args.get('check_in', '')
    check_out = request.args.get('check_out', '')
    number_of_guests = request.args.get('number_of_guests', '')
    room_type = request.args.get('room_type', '')

    rooms = Room.query.filter_by(status='Available')

    if number_of_guests:
        try:
            guests = int(number_of_guests)
            if guests < 1:
                raise ValueError
            rooms = rooms.filter(Room.capacity >= guests)
        except ValueError:
            flash('Please enter a valid number of guests.', 'danger')
            number_of_guests = ''

    if room_type:
        rooms = rooms.filter(Room.room_type == room_type)

    if check_in and check_out:
        try:
            check_in_date = date.fromisoformat(check_in)
            check_out_date = date.fromisoformat(check_out)

            if check_in_date < date.today():
                flash('Check-in date cannot be in the past.', 'danger')
                check_in = ''
                check_out = ''
            elif check_out_date <= check_in_date:
                flash('Check-out date must be after check-in date.', 'danger')
                check_in = ''
                check_out = ''
            else:
                rooms = rooms.filter(
                    ~Room.reservations.any(
                        db.and_(
                            Reservation.status.in_(['Pending', 'Confirmed']),
                            Reservation.check_in < check_out_date,
                            Reservation.check_out > check_in_date
                        )
                    )
                )

        except ValueError:
            flash('Please enter valid reservation dates.', 'danger')
            check_in = ''
            check_out = ''

    elif check_in or check_out:
        flash('Please select both check-in and check-out dates.', 'warning')
        check_in = ''
        check_out = ''

    rooms = rooms.order_by(Room.price.asc()).all()

    return render_template('available_rooms.html', rooms=rooms, check_in=check_in, check_out=check_out, number_of_guests=number_of_guests, room_type=room_type, today=date.today().isoformat())




    # management of reservation


from datetime import date, datetime
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user


# ============================================================
# MANAGE BOOKINGS
# ============================================================

@app.route('/manage-bookings')
@login_required
def manage_bookings():

    reservations = Reservation.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Reservation.created_at.desc()
    ).all()

    return render_template(
        'manage_bookings.html',
        user=current_user,
        reservations=reservations
    )


# ============================================================
# EDIT RESERVATION
# ============================================================

@app.route('/edit-reservation/<int:reservation_id>', methods=['GET', 'POST'])
@login_required
def edit_reservation(reservation_id):

    reservation = Reservation.query.filter_by(
        id=reservation_id,
        user_id=current_user.id
    ).first_or_404()

    if reservation.status == 'Cancelled':
        flash('Cancelled reservations cannot be edited.', 'warning')
        return redirect(url_for('manage_bookings'))

    if request.method == 'POST':

        try:
            check_in = datetime.strptime(
                request.form.get('check_in'), '%Y-%m-%d'
            ).date()

            check_out = datetime.strptime(
                request.form.get('check_out'), '%Y-%m-%d'
            ).date()

            number_of_guests = int(
                request.form.get('number_of_guests')
            )

            special_request = request.form.get(
                'special_request', ''
            ).strip()

            # Validate dates
            if check_in < date.today():
                flash('Check-in date cannot be in the past.', 'danger')
                return redirect(url_for(
                    'edit_reservation',
                    reservation_id=reservation.id
                ))

            if check_out <= check_in:
                flash('Check-out date must be after check-in date.', 'danger')
                return redirect(url_for(
                    'edit_reservation',
                    reservation_id=reservation.id
                ))

            # Validate room capacity
            if number_of_guests < 1 or number_of_guests > reservation.room.capacity:
                flash(
                    f'Number of guests must be between 1 and {reservation.room.capacity}.',
                    'danger'
                )
                return redirect(url_for(
                    'edit_reservation',
                    reservation_id=reservation.id
                ))

            # Check whether the room is still operational
            if reservation.room.status != 'Available':
                flash('This room is currently unavailable.', 'danger')
                return redirect(url_for('manage_bookings'))

            # Check for overlapping reservations
            conflicting_reservation = Reservation.query.filter(
                Reservation.room_id == reservation.room_id,
                Reservation.id != reservation.id,
                Reservation.status.in_(['Pending', 'Confirmed']),
                Reservation.check_in < check_out,
                Reservation.check_out > check_in
            ).first()

            if conflicting_reservation:
                flash(
                    'This room is already reserved for the selected dates.',
                    'danger'
                )
                return redirect(url_for(
                    'edit_reservation',
                    reservation_id=reservation.id
                ))

            # Calculate reservation amount
            number_of_nights = (check_out - check_in).days

            total_amount = number_of_nights * reservation.room.price

            # Update reservation
            reservation.check_in = check_in
            reservation.check_out = check_out
            reservation.number_of_guests = number_of_guests
            reservation.total_amount = total_amount
            reservation.special_request = special_request

            db.session.commit()

            flash('Reservation updated successfully.', 'success')

            return redirect(url_for('manage_bookings'))

        except (ValueError, TypeError):
            db.session.rollback()
            flash('Please provide valid reservation information.', 'danger')

        except Exception:
            db.session.rollback()
            flash('Unable to update reservation. Please try again.', 'danger')

    return render_template(
        'edit_reservation.html',
        user=current_user,
        reservation=reservation,
        today=date.today().isoformat()
    )


# ============================================================
# DELETE / CANCEL RESERVATION
# ============================================================

@app.route('/delete-reservation/<int:reservation_id>', methods=['POST'])
@login_required
def delete_reservation(reservation_id):

    reservation = Reservation.query.filter_by(
        id=reservation_id,
        user_id=current_user.id
    ).first_or_404()

    try:
        db.session.delete(reservation)
        db.session.commit()

        # log the cancellation action
        log_entry = LogReservation(
            reservation_id=reservation.id,
            action='Cancelled'
        )
        db.session.add(log_entry)
        db.session.commit()

        flash('Reservation cancelled and deleted successfully.', 'success')

    except Exception:
        db.session.rollback()
        flash('Unable to cancel reservation. Please try again.', 'danger')

    return redirect(url_for('manage_bookings'))
