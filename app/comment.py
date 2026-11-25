
# ============================================================
# HOTEL ROOM RESERVATION SYSTEM
# SAMPLE DATA AND DATA ENTRY OPTIONS
# ============================================================


# ============================================================
# 1. ROOM TABLE
# ============================================================

# room_number:
# Unique identification number assigned to each hotel room.
# Examples: 101, 102, 103, 201, 202, 301, 401
#
# Suggested numbering convention:
# Ground Floor: 001 - 099
# First Floor:   101 - 199
# Second Floor:  201 - 299
# Third Floor:   301 - 399
# Fourth Floor:  401 - 499


# room_type:
# Categories of rooms available in the hotel.
#
# Available options:
# 1. Standard
# 2. Deluxe
# 3. Superior
# 4. Executive
# 5. Suite
# 6. Family
# 7. Presidential


# description:
# Brief explanation of the room, its features and accommodation.
#
# Example:
# Spacious deluxe room with a king-size bed, air conditioning,
# television, private bathroom and complimentary Wi-Fi.


# price:
# Cost of occupying the room per night.
#
# Sample prices:
# Standard:       25000
# Deluxe:         45000
# Superior:       40000
# Executive:      75000
# Suite:         120000
# Family:         90000
# Presidential:  200000
#
# Note: These are illustrative prices in Nigerian Naira.


# capacity:
# Maximum number of people allowed in the room.
#
# Available options:
# 1, 2, 3, 4, 5, 6


# bed_type:
# Type of bed available in the room.
#
# Available options:
# 1. Single
# 2. Twin
# 3. Double
# 4. Queen
# 5. King
# 6. Bunk Bed


# facilities:
# Facilities and amenities available in the room.
#
# Available options:
# 1. Air Conditioning
# 2. Television
# 3. Free Wi-Fi
# 4. Refrigerator
# 5. Wardrobe
# 6. Private Bathroom
# 7. Hot Water
# 8. Balcony
# 9. Swimming Pool Access
# 10. Breakfast Included
# 11. Room Service
# 12. Work Desk
#
# Multiple facilities can be assigned to one room.


# image:
# Stores the filename or path of the uploaded room image.
#
# Examples:
# standard_101.jpg
# deluxe_201.jpg
# executive_301.jpg
# suite_401.jpg


# status:
# Operational status of the room.
#
# Available options:
# 1. Available
# 2. Maintenance
# 3. Inactive
#
# Available:
# Room is operational and can be considered for reservations.
#
# Maintenance:
# Room is undergoing repairs or maintenance.
#
# Inactive:
# Room has been temporarily or permanently removed from service.
#
# Note:
# Actual room availability must also be checked against reservation
# dates. Do not depend on room status alone.


# ============================================================
# 2. SAMPLE ROOM RECORDS
# ============================================================

# Room 101:
# Room Type: Standard
# Price: 25000
# Capacity: 2
# Bed Type: Double
# Facilities: Wi-Fi, TV, AC, Private Bathroom
# Status: Available

# Room 102:
# Room Type: Standard
# Price: 25000
# Capacity: 2
# Bed Type: Queen
# Facilities: Wi-Fi, TV, AC, Hot Water
# Status: Available

# Room 103:
# Room Type: Superior
# Price: 40000
# Capacity: 2
# Bed Type: Queen
# Facilities: Wi-Fi, TV, AC, Refrigerator
# Status: Maintenance

# Room 201:
# Room Type: Deluxe
# Price: 45000
# Capacity: 2
# Bed Type: King
# Facilities: Wi-Fi, TV, AC, Breakfast
# Status: Available

# Room 202:
# Room Type: Deluxe
# Price: 50000
# Capacity: 2
# Bed Type: King
# Facilities: Wi-Fi, TV, AC, Refrigerator, Balcony
# Status: Available

# Room 301:
# Room Type: Executive
# Price: 75000
# Capacity: 3
# Bed Type: King
# Facilities: Wi-Fi, TV, AC, Work Desk, Room Service
# Status: Available

# Room 401:
# Room Type: Suite
# Price: 120000
# Capacity: 4
# Bed Type: King
# Facilities: Wi-Fi, TV, AC, Refrigerator, Balcony, Breakfast
# Status: Available

# Room 501:
# Room Type: Family
# Price: 90000
# Capacity: 5
# Bed Type: Twin
# Facilities: Wi-Fi, TV, AC, Refrigerator, Room Service
# Status: Available


# ============================================================
# 3. RESERVATION TABLE
# ============================================================

# booking_reference:
# Unique reference automatically generated for every reservation.
#
# Example:
# HTL-A81B2C9D10
# HTL-2026-00125


# user_id:
# Foreign key referencing the registered User who made the reservation.
#
# Example:
# 1, 2, 3, 4, 5


# room_id:
# Foreign key referencing the selected room in the Room table.
#
# Example:
# 1, 2, 3, 4, 5


# check_in:
# Date the User intends to arrive at the hotel.
#
# Example:
# 2026-11-25


# check_out:
# Date the User intends to leave the hotel.
#
# Example:
# 2026-11-27
#
# Validation:
# Check-out date must be later than check-in date.


# number_of_guests:
# Number of people occupying the reserved room.
#
# Available options:
# 1, 2, 3, 4, 5, 6
#
# Validation:
# Number of guests must not exceed room capacity.


# total_amount:
# Total reservation cost.
#
# Calculation:
# Total Amount = Room Price Per Night * Number of Nights
#
# Example:
# Room Price = 65000
# Check-in = 25 November
# Check-out = 27 November
# Number of Nights = 2
# Total Amount = 130000


# status:
# Current state of the reservation.
#
# Available options:
# 1. Pending
# 2. Confirmed
# 3. Cancelled
# 4. Completed
#
# Pending:
# Reservation has been submitted but is awaiting confirmation.
#
# Confirmed:
# Reservation has been approved and accepted.
#
# Cancelled:
# Reservation has been cancelled by the User or hotel.
#
# Completed:
# User has completed the stay and checked out.


# special_request:
# Optional instructions or preferences submitted by the User.
#
# Examples:
# 1. Late arrival
# 2. Early check-in request
# 3. Extra pillow
# 4. Airport pickup
# 5. Room decoration
# 6. Non-smoking room
# 7. Birthday arrangement
# 8. Near elevator
# 9. None


# created_at:
# Automatically records the date and time the reservation was created.


# ============================================================
# 4. SAMPLE RESERVATION RECORDS
# ============================================================

# Reservation 1:
# Booking Reference: HTL-001
# User ID: 1
# Room ID: 2
# Check-in: 2026-11-25
# Check-out: 2026-11-27
# Number of Guests: 2
# Total Amount: 130000
# Status: Confirmed
# Special Request: Late arrival

# Reservation 2:
# Booking Reference: HTL-002
# User ID: 2
# Room ID: 1
# Check-in: 2026-11-26
# Check-out: 2026-11-28
# Number of Guests: 1
# Total Amount: 50000
# Status: Pending
# Special Request: Extra pillow

# Reservation 3:
# Booking Reference: HTL-003
# User ID: 3
# Room ID: 3
# Check-in: 2026-11-20
# Check-out: 2026-11-22
# Number of Guests: 2
# Total Amount: 80000
# Status: Completed
# Special Request: None

# Reservation 4:
# Booking Reference: HTL-004
# User ID: 1
# Room ID: 4
# Check-in: 2026-11-29
# Check-out: 2026-11-30
# Number of Guests: 2
# Total Amount: 45000
# Status: Cancelled
# Special Request: None


# ============================================================
# 5. PAYMENT OPTIONS
# ============================================================

# payment_method:
# 1. Pay at Hotel
# 2. Online Payment

# payment_status:
# 1. Unpaid
# 2. Pending
# 3. Paid
# 4. Failed
# 5. Refunded
# 6. Partially Refunded
#
# Note:
# Reservation status and payment status are different.
# A confirmed reservation does not necessarily mean payment
# has already been completed.


# ============================================================
# 6. CANCELLATION REASONS
# ============================================================

# cancellation_reason:
# 1. Change of Plans
# 2. Found Another Hotel
# 3. Travel Cancelled
# 4. Incorrect Booking Details
# 5. Financial Reasons
# 6. Emergency
# 7. Other


# ============================================================
# 7. DASHBOARD INFORMATION
# ============================================================

# Total Reservations:
# Total number of reservations made by the logged-in User.

# Upcoming Reservations:
# Number of confirmed reservations with future check-in dates.

# Cancelled Reservations:
# Total number of reservations with Cancelled status.

# Recent Reservations:
# Display the latest reservation records.
#
# Suggested columns:
# 1. Booking Reference
# 2. Room Type
# 3. Check-in Date
# 4. Check-out Date
# 5. Reservation Status
# 6. Action


# ============================================================
# 8. SUGGESTED DEVELOPMENT MODULES
# ============================================================

# 1. User Management
#    - User Registration
#    - User Login
#    - User Logout
#    - User Profile

# 2. Room Management
#    - Add Room
#    - View Rooms
#    - Update Room
#    - Delete/Deactivate Room
#    - Manage Room Status

# 3. Room Availability
#    - Search by Check-in Date
#    - Search by Check-out Date
#    - Filter by Room Type
#    - Filter by Number of Guests
#    - Check Reservation Date Conflicts

# 4. Reservation Management
#    - Make Reservation
#    - View Reservation
#    - Update Reservation
#    - Cancel Reservation
#    - Generate Booking Reference

# 5. Payment Management
#    - Select Payment Method
#    - Record Payment
#    - Update Payment Status
#    - Generate Payment Receipt

# 6. Dashboard Management
#    - Total Reservations
#    - Upcoming Reservations
#    - Cancelled Reservations
#    - Recent Reservations
#    - User Account Information
