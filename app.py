from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


# ==========================================
# APP CONFIGURATION
# ==========================================

app = Flask(__name__)

app.secret_key = "restaurant_secret_key"

DATABASE = "restaurant.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# ==========================================
# DATABASE SETUP / UPGRADE
# ==========================================

def upgrade_database():

    conn = get_db_connection()

    # ==========================================
    # USERS TABLE
    # ==========================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT NOT NULL UNIQUE,

            password TEXT NOT NULL,

            role TEXT NOT NULL DEFAULT 'customer'
        )
    """)


    # ==========================================
    # RESTAURANT TABLES
    # ==========================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS restaurant_tables (

            table_id INTEGER PRIMARY KEY AUTOINCREMENT,

            table_number TEXT NOT NULL UNIQUE,

            capacity INTEGER NOT NULL,

            status TEXT DEFAULT 'Available'
        )
    """)


    # ==========================================
    # RESERVATIONS
    # ==========================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reservations (

            reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,

            customer_id INTEGER,

            customer_name TEXT NOT NULL,

            phone TEXT NOT NULL,

            table_id INTEGER NOT NULL,

            booking_date TEXT NOT NULL,

            booking_time TEXT NOT NULL,

            guests INTEGER NOT NULL,

            status TEXT DEFAULT 'Reserved'
        )
    """)


    # ==========================================
    # CHECK RESERVATIONS COLUMNS
    # ==========================================

    reservation_columns = conn.execute(
        "PRAGMA table_info(reservations)"
    ).fetchall()


    reservation_column_names = [

        column["name"]

        for column in reservation_columns

    ]


    # Add customer_id if missing

    if "customer_id" not in reservation_column_names:

        conn.execute("""
            ALTER TABLE reservations
            ADD COLUMN customer_id INTEGER
        """)


    # Add status if missing

    if "status" not in reservation_column_names:

        conn.execute("""
            ALTER TABLE reservations
            ADD COLUMN status TEXT DEFAULT 'Reserved'
        """)


    # ==========================================
    # CHECK RESTAURANT TABLE COLUMNS
    # ==========================================

    table_columns = conn.execute(
        "PRAGMA table_info(restaurant_tables)"
    ).fetchall()


    table_column_names = [

        column["name"]

        for column in table_columns

    ]


    # Add status if missing

    if "status" not in table_column_names:

        conn.execute("""
            ALTER TABLE restaurant_tables
            ADD COLUMN status TEXT DEFAULT 'Available'
        """)


    conn.commit()

    conn.close()


# ==========================================
# HOME PAGE
# ==========================================

@app.route('/')
def home():

    return render_template(
        'index.html'
    )


# ==========================================
# CUSTOMER REGISTER
# ==========================================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form.get(
            'name',
            ''
        ).strip()


        email = request.form.get(
            'email',
            ''
        ).strip().lower()


        password = request.form.get(
            'password',
            ''
        )


        # VALIDATION

        if not name or not email or not password:

            return render_template(
                'register.html',
                error="All fields are required!"
            )


        if len(name) < 2:

            return render_template(
                'register.html',
                error="Please enter a valid name."
            )


        if len(password) < 6:

            return render_template(
                'register.html',
                error="Password must contain at least 6 characters!"
            )


        password_hash = generate_password_hash(
            password
        )


        conn = get_db_connection()


        try:

            conn.execute("""
                INSERT INTO users
                (
                    name,
                    email,
                    password,
                    role
                )

                VALUES (?, ?, ?, ?)
            """, (
                name,
                email,
                password_hash,
                'customer'
            ))


            conn.commit()

            conn.close()


            return redirect(
                url_for('customer_login')
            )


        except sqlite3.IntegrityError:

            conn.close()


            return render_template(
                'register.html',
                error="Email already registered!"
            )


    # IMPORTANT: GET REQUEST RETURN

    return render_template(
        'register.html'
    )


# ==========================================
# CUSTOMER LOGIN
# ==========================================

@app.route('/login', methods=['GET', 'POST'])
def customer_login():

    if request.method == 'POST':

        email = request.form.get(
            'email',
            ''
        ).strip().lower()


        password = request.form.get(
            'password',
            ''
        )


        if not email or not password:

            return render_template(
                'login.html',
                error="Please enter email and password."
            )


        conn = get_db_connection()


        customer = conn.execute("""
            SELECT *
            FROM users

            WHERE email = ?

            AND role = 'customer'
        """, (
            email,
        )).fetchone()


        if customer:

            stored_password = customer['password']

            password_valid = False


            try:

                password_valid = check_password_hash(
                    stored_password,
                    password
                )

            except Exception:

                password_valid = False


            # OLD PLAIN TEXT PASSWORD SUPPORT

            if (

                not password_valid

                and

                stored_password == password

            ):

                new_hash = generate_password_hash(
                    password
                )


                conn.execute("""
                    UPDATE users

                    SET password = ?

                    WHERE id = ?
                """, (
                    new_hash,
                    customer['id']
                ))


                conn.commit()

                password_valid = True


            if password_valid:

                session['customer_id'] = customer['id']

                session['customer_name'] = customer['name']


                conn.close()


                return redirect(
                    url_for('booking')
                )


        conn.close()


        return render_template(
            'login.html',
            error="Invalid email or password!"
        )


    return render_template(
        'login.html'
    )


# ==========================================
# CUSTOMER LOGOUT
# ==========================================

@app.route('/logout')
def customer_logout():

    session.pop(
        'customer_id',
        None
    )


    session.pop(
        'customer_name',
        None
    )


    return redirect(
        url_for('home')
    )


# ==========================================
# CUSTOMER BOOKING HISTORY
# ==========================================

@app.route('/booking-history')
def booking_history():

    if 'customer_id' not in session:

        return redirect(
            url_for('customer_login')
        )


    customer_id = session['customer_id']


    conn = get_db_connection()


    bookings = conn.execute("""
        SELECT

            reservations.*,

            restaurant_tables.table_number,

            restaurant_tables.capacity

        FROM reservations

        LEFT JOIN restaurant_tables

        ON reservations.table_id =
           restaurant_tables.table_id

        WHERE reservations.customer_id = ?

        ORDER BY

            reservations.booking_date DESC,

            reservations.booking_time DESC,

            reservations.reservation_id DESC

    """, (
        customer_id,
    )).fetchall()


    conn.close()


    return render_template(
        'booking_history.html',
        bookings=bookings
    )


# ==========================================
# CUSTOMER CANCEL BOOKING
# ==========================================

@app.route('/cancel-booking/<int:reservation_id>')
def customer_cancel_booking(reservation_id):

    if 'customer_id' not in session:

        return redirect(
            url_for('customer_login')
        )


    customer_id = session['customer_id']


    conn = get_db_connection()


    reservation = conn.execute("""
        SELECT *

        FROM reservations

        WHERE reservation_id = ?

        AND customer_id = ?
    """, (
        reservation_id,
        customer_id
    )).fetchone()


    if reservation:

        conn.execute("""
            DELETE FROM reservations

            WHERE reservation_id = ?

            AND customer_id = ?
        """, (
            reservation_id,
            customer_id
        ))


        conn.commit()


    conn.close()


    return redirect(
        url_for('booking_history')
    )


# ==========================================
# AVAILABLE TABLES
# ==========================================

@app.route('/available-tables')
def available_tables():

    conn = get_db_connection()


    tables = conn.execute("""
        SELECT *

        FROM restaurant_tables

        WHERE status = 'Available'

        ORDER BY

            capacity ASC,

            table_number ASC
    """).fetchall()


    conn.close()


    return render_template(
        'available_tables.html',
        tables=tables
    )


# ==========================================
# TABLE BOOKING
# ==========================================

@app.route('/booking', methods=['GET', 'POST'])
def booking():

    if 'customer_id' not in session:

        return redirect(
            url_for('customer_login')
        )


    if request.method == 'POST':

        customer_id = session['customer_id']

        customer_name = session['customer_name']


        # ==========================================
        # FORM DATA
        # ==========================================

        phone = request.form.get(
            'phone',
            ''
        ).strip()


        booking_date = request.form.get(
            'booking_date',
            ''
        ).strip()


        booking_time = request.form.get(
            'booking_time',
            ''
        ).strip()


        # ==========================================
        # PHONE VALIDATION
        # ==========================================

        if not phone:

            return render_template(
                'booking.html',
                error="Please enter your phone number."
            )


        if len(phone) < 10:

            return render_template(
                'booking.html',
                error="Please enter a valid phone number."
            )


        # ==========================================
        # GUEST VALIDATION
        # ==========================================

        try:

            guests = int(
                request.form.get(
                    'guests',
                    0
                )
            )


        except ValueError:

            return render_template(
                'booking.html',
                error="Please enter a valid number of guests."
            )


        if guests <= 0:

            return render_template(
                'booking.html',
                error="Number of guests must be greater than zero."
            )


        if guests > 20:

            return render_template(
                'booking.html',
                error="Maximum 20 guests can be booked at once."
            )


        # ==========================================
        # DATE AND TIME
        # ==========================================

        try:

            requested_start = datetime.strptime(
                booking_date + " " + booking_time,
                "%Y-%m-%d %H:%M"
            )


        except ValueError:

            return render_template(
                'booking.html',
                error="Invalid booking date or time."
            )


        # ==========================================
        # PREVENT PAST BOOKINGS
        # ==========================================

        if requested_start < datetime.now():

            return render_template(
                'booking.html',
                error="You cannot book a table in the past."
            )


        # ==========================================
        # RESTAURANT HOURS
        # ==========================================

        opening_time = 10 * 60

        closing_time = 22 * 60


        requested_minutes = (

            requested_start.hour * 60

            +

            requested_start.minute

        )


        booking_duration = 120


        requested_end_minutes = (

            requested_minutes

            +

            booking_duration

        )


        if (

            requested_minutes < opening_time

            or

            requested_end_minutes > closing_time

        ):

            return render_template(
                'booking.html',
                error=(
                    "Bookings are available "
                    "between 10:00 AM and 8:00 PM."
                )
            )


        # ==========================================
        # DATABASE
        # ==========================================

        conn = get_db_connection()


        # ==========================================
        # FIND SUITABLE TABLE
        # ==========================================

        tables = conn.execute("""
            SELECT *

            FROM restaurant_tables

            WHERE capacity >= ?

            AND status != 'Occupied'

            ORDER BY

                capacity ASC,

                table_number ASC

        """, (
            guests,
        )).fetchall()


        selected_table = None


        # ==========================================
        # CHECK FOR TIME CONFLICTS
        # ==========================================

        for table in tables:

            existing_bookings = conn.execute("""
                SELECT booking_time

                FROM reservations

                WHERE table_id = ?

                AND booking_date = ?

                AND status = 'Reserved'

            """, (
                table['table_id'],
                booking_date
            )).fetchall()


            conflict = False


            for existing in existing_bookings:

                try:

                    existing_start = datetime.strptime(
                        booking_date
                        + " "
                        + existing['booking_time'],
                        "%Y-%m-%d %H:%M"
                    )


                except ValueError:

                    continue


                existing_end = (

                    existing_start

                    +

                    timedelta(hours=2)

                )


                requested_end = (

                    requested_start

                    +

                    timedelta(hours=2)

                )


                # TIME OVERLAP

                if (

                    requested_start < existing_end

                    and

                    requested_end > existing_start

                ):

                    conflict = True

                    break


            if not conflict:

                selected_table = table

                break


        # ==========================================
        # BOOKING SUCCESS
        # ==========================================

        if selected_table:

            # 8 COLUMNS = 8 VALUES

            conn.execute("""
                INSERT INTO reservations
                (
                    customer_id,
                    customer_name,
                    phone,
                    table_id,
                    booking_date,
                    booking_time,
                    guests,
                    status
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?)

            """, (
                customer_id,
                customer_name,
                phone,
                selected_table['table_id'],
                booking_date,
                booking_time,
                guests,
                'Reserved'
            ))


            conn.commit()

            conn.close()


            return render_template(
                'booking_success.html',
                table_number=selected_table['table_number'],
                customer_name=customer_name
            )


        # ==========================================
        # NO TABLE AVAILABLE
        # ==========================================

        conn.close()


        return render_template(
            'booking.html',
            error=(
                "Sorry! No suitable table is available "
                "for the selected date and time. "
                "Please choose another time."
            )
        )


    return render_template(
        'booking.html'
    )


# ==========================================
# ADMIN LOGIN
# ==========================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        email = request.form.get(
            'email',
            ''
        ).strip().lower()


        password = request.form.get(
            'password',
            ''
        )


        if not email or not password:

            return render_template(
                'admin_login.html',
                error="Please enter email and password."
            )


        conn = get_db_connection()


        admin = conn.execute("""
            SELECT *

            FROM users

            WHERE email = ?

            AND role = 'admin'

        """, (
            email,
        )).fetchone()


        if admin:

            stored_password = admin['password']

            password_valid = False


            try:

                password_valid = check_password_hash(
                    stored_password,
                    password
                )


            except Exception:

                password_valid = False


            # OLD PLAIN PASSWORD SUPPORT

            if (

                not password_valid

                and

                stored_password == password

            ):

                new_hash = generate_password_hash(
                    password
                )


                conn.execute("""
                    UPDATE users

                    SET password = ?

                    WHERE id = ?
                """, (
                    new_hash,
                    admin['id']
                ))


                conn.commit()

                password_valid = True


            if password_valid:

                session['admin_id'] = admin['id']

                session['admin_name'] = admin['name']


                conn.close()


                return redirect(
                    url_for('admin_dashboard')
                )


        conn.close()


        return render_template(
            'admin_login.html',
            error="Invalid email or password!"
        )


    return render_template(
        'admin_login.html'
    )


# ==========================================
# ADMIN DASHBOARD
# ==========================================

@app.route('/admin/dashboard')
def admin_dashboard():

    if 'admin_id' not in session:

        return redirect(
            url_for('admin_login')
        )


    search = request.args.get(
        'search',
        ''
    ).strip()


    conn = get_db_connection()


    # ==========================================
    # STATISTICS
    # ==========================================

    total_tables = conn.execute("""
        SELECT COUNT(*)

        FROM restaurant_tables
    """).fetchone()[0]


    available_tables_count = conn.execute("""
        SELECT COUNT(*)

        FROM restaurant_tables

        WHERE status = 'Available'
    """).fetchone()[0]


    reserved_tables_count = conn.execute("""
        SELECT COUNT(*)

        FROM restaurant_tables

        WHERE status = 'Reserved'
    """).fetchone()[0]


    occupied_tables_count = conn.execute("""
        SELECT COUNT(*)

        FROM restaurant_tables

        WHERE status = 'Occupied'
    """).fetchone()[0]


    total_reservations = conn.execute("""
        SELECT COUNT(*)

        FROM reservations
    """).fetchone()[0]


    # ==========================================
    # ALL TABLES
    # ==========================================

    tables = conn.execute("""
        SELECT *

        FROM restaurant_tables

        ORDER BY table_number ASC
    """).fetchall()


    # ==========================================
    # SEARCH RESERVATIONS
    # ==========================================

    if search:

        reservations = conn.execute("""
            SELECT

                reservations.*,

                restaurant_tables.table_number,

                restaurant_tables.capacity

            FROM reservations

            LEFT JOIN restaurant_tables

            ON reservations.table_id =
               restaurant_tables.table_id

            WHERE

                reservations.customer_name LIKE ?

                OR reservations.phone LIKE ?

                OR CAST(
                    restaurant_tables.table_number
                    AS TEXT
                ) LIKE ?

                OR reservations.booking_date LIKE ?

            ORDER BY
                reservations.reservation_id DESC

        """, (
            '%' + search + '%',
            '%' + search + '%',
            '%' + search + '%',
            '%' + search + '%'
        )).fetchall()


    else:

        reservations = conn.execute("""
            SELECT

                reservations.*,

                restaurant_tables.table_number,

                restaurant_tables.capacity

            FROM reservations

            LEFT JOIN restaurant_tables

            ON reservations.table_id =
               restaurant_tables.table_id

            ORDER BY
                reservations.reservation_id DESC

        """).fetchall()


    conn.close()


    return render_template(
        'dashboard.html',

        tables=tables,

        reservations=reservations,

        search=search,

        total_tables=total_tables,

        available_tables_count=available_tables_count,

        reserved_tables_count=reserved_tables_count,

        occupied_tables_count=occupied_tables_count,

        total_reservations=total_reservations
    )


# ==========================================
# ADD TABLE
# ==========================================

@app.route(
    '/admin/add-table',
    methods=['POST']
)
def add_table():

    if 'admin_id' not in session:

        return redirect(
            url_for('admin_login')
        )


    table_number = request.form.get(
        'table_number',
        ''
    ).strip()


    capacity = request.form.get(
        'capacity',
        ''
    ).strip()


    if not table_number or not capacity:

        return redirect(
            url_for('admin_dashboard')
        )


    try:

        capacity = int(capacity)


    except ValueError:

        return redirect(
            url_for('admin_dashboard')
        )


    if capacity <= 0:

        return redirect(
            url_for('admin_dashboard')
        )


    conn = get_db_connection()


    try:

        conn.execute("""
            INSERT INTO restaurant_tables
            (
                table_number,
                capacity,
                status
            )

            VALUES (?, ?, ?)

        """, (
            table_number,
            capacity,
            'Available'
        ))


        conn.commit()


    except sqlite3.IntegrityError:

        pass


    conn.close()


    return redirect(
        url_for('admin_dashboard')
    )


# ==========================================
# EDIT RESERVATION
# ==========================================

@app.route(
    '/admin/edit-reservation/<int:reservation_id>',
    methods=['GET', 'POST']
)
def edit_reservation(reservation_id):

    if 'admin_id' not in session:

        return redirect(
            url_for('admin_login')
        )


    conn = get_db_connection()


    if request.method == 'POST':

        customer_name = request.form.get(
            'customer_name',
            ''
        ).strip()


        phone = request.form.get(
            'phone',
            ''
        ).strip()


        booking_date = request.form.get(
            'booking_date',
            ''
        ).strip()


        booking_time = request.form.get(
            'booking_time',
            ''
        ).strip()


        guests = request.form.get(
            'guests',
            ''
        ).strip()


        if (

            not customer_name

            or not phone

            or not booking_date

            or not booking_time

            or not guests

        ):

            conn.close()

            return redirect(
                url_for('admin_dashboard')
            )


        try:

            guests = int(guests)


        except ValueError:

            conn.close()

            return redirect(
                url_for('admin_dashboard')
            )


        try:

            datetime.strptime(
                booking_date + " " + booking_time,
                "%Y-%m-%d %H:%M"
            )


        except ValueError:

            conn.close()

            return redirect(
                url_for('admin_dashboard')
            )


        conn.execute("""
            UPDATE reservations

            SET

                customer_name = ?,

                phone = ?,

                booking_date = ?,

                booking_time = ?,

                guests = ?

            WHERE reservation_id = ?

        """, (
            customer_name,
            phone,
            booking_date,
            booking_time,
            guests,
            reservation_id
        ))


        conn.commit()

        conn.close()


        return redirect(
            url_for('admin_dashboard')
        )


    reservation = conn.execute("""
        SELECT *

        FROM reservations

        WHERE reservation_id = ?
    """, (
        reservation_id,
    )).fetchone()


    conn.close()


    if reservation is None:

        return redirect(
            url_for('admin_dashboard')
        )


    return render_template(
        'edit_reservation.html',
        reservation=reservation
    )


# ==========================================
# ADMIN DELETE RESERVATION
# ==========================================

@app.route(
    '/admin/cancel-reservation/<int:reservation_id>'
)
def cancel_reservation(reservation_id):

    if 'admin_id' not in session:

        return redirect(
            url_for('admin_login')
        )


    conn = get_db_connection()


    reservation = conn.execute("""
        SELECT *

        FROM reservations

        WHERE reservation_id = ?
    """, (
        reservation_id,
    )).fetchone()


    if reservation:

        conn.execute("""
            DELETE FROM reservations

            WHERE reservation_id = ?
        """, (
            reservation_id,
        ))


        conn.commit()


    conn.close()


    return redirect(
        url_for('admin_dashboard')
    )


# ==========================================
# UPDATE TABLE STATUS
# ==========================================

@app.route(
    '/admin/update-table-status/<int:table_id>',
    methods=['POST']
)
def update_table_status(table_id):

    if 'admin_id' not in session:

        return redirect(
            url_for('admin_login')
        )


    status = request.form.get(
        'status',
        ''
    )


    allowed_status = [

        'Available',

        'Reserved',

        'Occupied'

    ]


    if status in allowed_status:

        conn = get_db_connection()


        conn.execute("""
            UPDATE restaurant_tables

            SET status = ?

            WHERE table_id = ?

        """, (
            status,
            table_id
        ))


        conn.commit()

        conn.close()


    return redirect(
        url_for('admin_dashboard')
    )


# ==========================================
# ADMIN LOGOUT
# ==========================================

@app.route('/admin/logout')
def admin_logout():

    session.pop(
        'admin_id',
        None
    )


    session.pop(
        'admin_name',
        None
    )


    return redirect(
        url_for('home')
    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == '__main__':

    upgrade_database()

    app.run(
        debug=True
    )