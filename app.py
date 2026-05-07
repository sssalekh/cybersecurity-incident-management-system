from flask import Flask, render_template, request, redirect, session
import sqlite3
from database import get_incidents
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret"

def log_action(user, action):
    os.makedirs("logs", exist_ok=True)

    with open("logs/activity.log", "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {user} | {action}\n")


def check_user(username, password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    
    if user and check_password_hash(user[2], password):
        return user
    else:
        return None

    conn.close()
    return user

def is_admin():
    return session.get("role") == "Administrator"

def is_analyst():
    return session.get("role") == "Security Analyst"

@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = check_user(username, password)

        if user:
            session["user"] = user[1]
            session["role"] = user[3]

            log_action(username, "Logged in")

            return redirect("/dashboard")
        else:
            error = "Invalid credentials"

    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    severity = request.args.get("severity")
    query = request.args.get("q")

    incidents = get_incidents()

    if query:
        query = query.lower()
        incidents = [
            i for i in incidents
            if query in str(i[0]).lower()      # ID
            or query in i[1].lower()           # type
            or query in i[2].lower()           # description
            or (i[6] and query in i[6].lower())  # comments
        ]

    if severity:
        incidents = [i for i in incidents if i[3] == severity]

    high = sum(1 for i in incidents if i[3] == "High")
    medium = sum(1 for i in incidents if i[3] == "Medium")
    low = sum(1 for i in incidents if i[3] == "Low")

    return render_template(
        "dashboard.html",
        incidents=incidents,
        high=high,
        medium=medium,
        low=low
    )

@app.route("/logout")
def logout():
    log_action(session.get("user"), "Logged out")
    session.clear()
    return redirect("/")

@app.route("/admin")
def admin_panel():
    if not is_admin():
        return "Access denied"

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template("admin.html", users=users)

@app.route("/rules")
def rules():
    if not is_admin():
        return "Access denied"

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM rules")
    rules = cursor.fetchall()

    conn.close()

    return render_template("rules.html", rules=rules)

@app.route("/toggle_rule/<int:id>")
def toggle_rule(id):
    log_action(session["user"], f"Toggled rule {id}")
    if not is_admin():
        return "Access denied"

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE rules SET enabled = 1 - enabled WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/rules")

@app.route("/add_user", methods=["POST"])
def add_user():
    if not is_admin():
        return "Access denied"

    username = request.form["username"]
    password = generate_password_hash(request.form["password"])
    role = request.form["role"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (username, password, role)
    VALUES (?, ?, ?)
    """, (username, password, role))

    conn.commit()
    conn.close()

    return redirect("/admin")

@app.route("/close/<int:id>")
def close_incident(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE incidents SET status='Closed' WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/update_status/<int:id>/<status>")
def update_status(id, status):
    log_action(session["user"], f"Changed status of incident {id} to {status}")
    if "user" not in session:
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE incidents SET status=? WHERE id=?", (status, id))
    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/add_comment/<int:id>", methods=["POST"])
def add_comment(id):
    log_action(session["user"], f"Added comment to incident {id}")
    if not is_analyst():
        return "Access denied"

    comment = request.form["comment"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT comments FROM incidents WHERE id=?", (id,))
    old_comment = cursor.fetchone()[0] or ""

    new_comment = old_comment + "\n" + comment

    cursor.execute("UPDATE incidents SET comments=? WHERE id=?", (new_comment, id))

    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/update_severity/<int:id>")
def update_severity(id):
    if not is_analyst():
        return "Access denied"

    severity = request.args.get("severity")

    log_action(session["user"], f"Changed severity of incident {id} to {severity}")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE incidents SET severity=? WHERE id=?", (severity, id))
    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/incident/<int:id>")
def incident_detail(id):
    if "user" not in session:
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM incidents WHERE id=?", (id,))
    incident = cursor.fetchone()

    conn.close()

    if not incident:
        return "Incident not found"

    return render_template("incident_detail.html", incident=incident)

if __name__ == "__main__":
    app.run(debug=True)
