# 🍽️ Restaurant Table Allocation System

A modern **web-based Restaurant Table Allocation and Reservation System** built with **Python Flask and SQLite**. The system allows customers to register, log in, check table availability, reserve tables, and view their booking history. An administrator can manage restaurant tables and monitor customer reservations through a dedicated admin dashboard.

<p align="center">

**🌐 Live Demo:**
https://restaurant-table-allocation.onrender.com

</p>

---

## 📸 Screenshots

> Add your project screenshots inside a `screenshots/` folder in the repository.

### 🏠 Home Page

![Home Page](screenshots/home.png)

### 🔐 Customer Login

![Customer Login](screenshots/login.png)

### 📝 Customer Registration

![Customer Registration](screenshots/register.png)

### 🍽️ Table Availability

![Available Tables](screenshots/available-tables.png)

### 📅 Table Booking

![Table Booking](screenshots/booking.png)

### 📋 Booking History

![Booking History](screenshots/booking-history.png)

### 👨‍💼 Admin Dashboard

![Admin Dashboard](screenshots/admin-dashboard.png)

### 🪑 Table Management

![Table Management](screenshots/table-management.png)

---

# ✨ Features

## 👤 Customer Features

* Customer registration
* Secure customer login
* Password hashing
* View available restaurant tables
* Book restaurant tables
* Booking date and time selection
* Booking validation
* View booking history
* View reservation details
* Customer logout

## 👨‍💼 Admin Features

* Secure admin login
* Admin dashboard
* View restaurant tables
* Add restaurant tables
* Manage table availability
* View customer reservations
* Manage bookings
* Delete tables
* Monitor restaurant operations

## 🔒 Security Features

* Password hashing using Werkzeug
* Separate customer and admin authentication
* Session-based authentication
* Protected admin routes
* Input validation
* Booking validation

---

# 🏗️ Project Architecture

```text
                    ┌─────────────────────────┐
                    │       User Browser      │
                    │   HTML / CSS / JS       │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       Flask App         │
                    │         app.py           │
                    └────────────┬────────────┘
                                 │
                  ┌──────────────┴──────────────┐
                  │                             │
                  ▼                             ▼
        ┌──────────────────┐          ┌──────────────────┐
        │ Authentication   │          │ Booking System   │
        │ Login/Register   │          │ Table Allocation │
        └──────────────────┘          └────────┬─────────┘
                                               │
                                               ▼
                                   ┌─────────────────────┐
                                   │     database.py     │
                                   │   Database Layer    │
                                   └──────────┬──────────┘
                                              │
                                              ▼
                                   ┌─────────────────────┐
                                   │     SQLite DB       │
                                   │   restaurant.db     │
                                   └─────────────────────┘
```

---

# 🔄 System Workflow

```text
                 START
                   │
                   ▼
             Open Website
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
      Customer           Admin
          │                 │
          ▼                 ▼
    Login/Register       Admin Login
          │                 │
          ▼                 ▼
    Customer Dashboard   Admin Dashboard
          │                 │
          ▼                 ▼
    Check Availability   Manage Tables
          │                 │
          ▼                 ▼
      Book Table        Manage Bookings
          │
          ▼
    Booking History
          │
          ▼
          END
```

---

# 🛠️ Technologies Used

| Technology    | Purpose                   |
| ------------- | ------------------------- |
| 🐍 Python     | Backend programming       |
| 🌐 Flask      | Web framework             |
| 🗄️ SQLite    | Database                  |
| 🎨 HTML5      | Web page structure        |
| 🎨 CSS3       | Styling                   |
| ⚡ JavaScript  | Client-side functionality |
| 🅱️ Bootstrap | Responsive UI             |
| 🔐 Werkzeug   | Password hashing          |
| ☁️ Render     | Cloud deployment          |
| 🐙 GitHub     | Source code management    |

---

# 📂 Project Structure

```text
Restaurant-Table-Allocation/
│
├── 📄 app.py
├── 📄 database.py
├── 📄 check_admin.py
├── 📄 requirements.txt
├── 📄 README.md
│
├── 🗄️ database.db
├── 🗄️ restaurant.db
│
├── 📁 static/
│   ├── 📄 style.css
│   └── 📁 images/
│
├── 📁 templates/
│   ├── 📄 index.html
│   ├── 📄 login.html
│   ├── 📄 register.html
│   ├── 📄 dashboard.html
│   ├── 📄 booking.html
│   ├── 📄 booking_history.html
│   ├── 📄 available_tables.html
│   ├── 📄 admin_login.html
│   ├── 📄 admin_dashboard.html
│   └── ...
│
└── 📁 screenshots/
    ├── 📄 home.png
    ├── 📄 login.png
    ├── 📄 register.png
    ├── 📄 booking.png
    ├── 📄 available-tables.png
    ├── 📄 booking-history.png
    ├── 📄 admin-dashboard.png
    └── 📄 table-management.png
```

---

# 🚀 Installation

Follow these steps to run the project locally.

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/Veeraj-07/-Restaurant-Table-Allocation.git
```

Move into the project directory:

```bash
cd -Restaurant-Table-Allocation
```

---

## 2️⃣ Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

### PowerShell

```powershell
venv\Scripts\Activate.ps1
```

### Command Prompt

```cmd
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run the Application

```bash
python app.py
```

You should see Flask start the development server.

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

# 🔐 Demo Credentials

## 👨‍💼 Admin

```text
Username: admin
Password: admin123
```

## 👤 Customer

Create a customer account using the **Register** page.

> ⚠️ If your actual admin username/password is different, replace the credentials above with the credentials configured in your project.

---

# 🌐 Live Demo

The application is deployed on Render.

### 🔗 Live Website

https://restaurant-table-allocation.onrender.com

### 🔗 GitHub Repository

https://github.com/Veeraj-07/-Restaurant-Table-Allocation

---

# 🗄️ Database

The application uses **SQLite** for data storage.

The database manages information such as:

```text
Users
   │
   ├── Customer Accounts
   └── Admin Accounts

Tables
   │
   ├── Table Number
   ├── Capacity
   └── Availability

Bookings
   │
   ├── Customer
   ├── Table
   ├── Date
   ├── Time
   └── Booking Status
```

---

# 📋 Main Modules

### 1. Authentication Module

Handles:

* Registration
* Login
* Logout
* Password hashing
* Session management

### 2. Table Management Module

Handles:

* Adding tables
* Viewing tables
* Checking availability
* Removing tables
* Managing table capacity

### 3. Booking Module

Handles:

* Table reservations
* Booking date/time
* Availability checking
* Booking validation
* Reservation management

### 4. Admin Module

Handles:

* Admin authentication
* Dashboard
* Table management
* Reservation management

### 5. Customer Module

Handles:

* Customer dashboard
* Table search
* Reservations
* Booking history

---

# 🎯 Objectives

The main objectives of this project are:

* To digitize restaurant table reservations.
* To reduce manual table allocation.
* To prevent table booking conflicts.
* To provide customers with an easy reservation system.
* To provide administrators with centralized table management.
* To maintain reservation records digitally.
* To improve restaurant operational efficiency.

---

# 🌟 Advantages

✅ Easy to use
✅ Fast table reservation
✅ Reduces manual work
✅ Prevents double booking
✅ Centralized reservation management
✅ Secure authentication
✅ Responsive web interface
✅ Easy database management
✅ Cloud deployment support

---

# 🔮 Future Enhancements

Possible future improvements include:

* 💳 Online payment integration
* 📧 Email booking confirmation
* 📱 SMS notifications
* 📱 Mobile application
* 📊 Advanced admin analytics
* 📈 Revenue reports
* ⭐ Customer reviews and ratings
* 🪑 Visual restaurant floor plan
* 🔔 Real-time booking notifications
* 🤖 AI-based table allocation
* 🗄️ PostgreSQL database for production deployment

---

# ☁️ Deployment

The application is deployed using **Render**.

```text
GitHub Repository
       │
       ▼
    Render
       │
       ▼
Flask Application
       │
       ▼
Restaurant Website
```

### Production URL

https://restaurant-table-allocation.onrender.com

---

# 🧪 Testing

The following functionalities should be tested before deployment:

| Test Case             | Expected Result             |
| --------------------- | --------------------------- |
| Customer Registration | Account created             |
| Customer Login        | Customer dashboard opens    |
| Invalid Login         | Error message displayed     |
| Table Availability    | Available tables displayed  |
| Table Booking         | Reservation created         |
| Duplicate Booking     | Booking prevented           |
| Booking History       | Previous bookings displayed |
| Admin Login           | Admin dashboard opens       |
| Add Table             | New table created           |
| Delete Table          | Table removed               |
| Logout                | User session terminated     |

---

# 👨‍💻 Author

**Veeraj V Gowda**

### Project

🍽️ **Restaurant Table Allocation System**

### Technologies

`Python` `Flask` `SQLite` `HTML` `CSS` `JavaScript` `Bootstrap`

---

# 📜 License

This project is developed for **educational and academic purposes**.

---

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 🔗 Project Links

🌐 **Live Demo:**
https://restaurant-table-allocation.onrender.com

🐙 **GitHub:**
https://github.com/Veeraj-07/-Restaurant-Table-Allocation
