# Cybersecurity Incident Management System

This project is a web-based Cybersecurity Incident Management System developed using Python and Flask.  
It simulates security events, detects suspicious activity, and allows users to manage incidents through a web interface.

---

## Features

- Simulated event generation (failed logins, port scans, unknown IPs, file access)
- Rule-based incident detection
- Automatic incident creation
- Severity classification (Low, Medium, High)
- Role-Based Access Control (Administrator / Security Analyst)
- Incident management (status updates, comments, severity adjustment)
- Detection rules management (enable/disable rules)
- Web dashboard interface

---

## Technologies Used

- Python
- Flask
- SQLite
- HTML, CSS

---

## Project Structure

```
├── app.py
├── main.py
├── run_system.py
├── init_db.py
├── database.py
├── detection.py
├── event_generator.py
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── admin.html
│   ├── rules.html
│   └── incident_detail.html
├── static/
│   └── style.css
└── README.md
```

---

## How It Works

The system uses a simulated event generator to produce cybersecurity events such as:

- Failed login attempts  
- Port scanning  
- Unknown IP connections  
- Sensitive file access  

These events are processed by the detection module (detection.py), which applies predefined rules.  
If a rule is triggered, an incident is automatically created and stored in the database.

---

## Roles

### Administrator
- Manage users
- Configure detection rules

### Security Analyst
- Investigate incidents
- Update status
- Add comments
- Adjust severity

---

## How to Run

### 1. Install dependencies
```bash
pip install flask
```

### 2. Initialize the database
```bash
python init_db.py
```

### 3. Run the system
```bash
python run_system.py
```

---

### 4. Open in browser
http://127.0.0.1:5000

---

## Notes

- The system uses a simulated environment, not a real network
- Detection rules can be dynamically enabled or disabled
- The project is developed for educational purposes

---

## Author

Student project for Cybersecurity / Software Engineering coursework.
