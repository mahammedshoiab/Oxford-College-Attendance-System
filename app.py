
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash
import sqlite3
import math

app = Flask(__name__)

MIN_ATTENDANCE = 75


# DATABASE CONNECTION
def get_db_connection():
    connection = sqlite3.connect("attendance.db")
    connection.row_factory = sqlite3.Row
    return connection


# HOME - TEACHER DASHBOARD
@app.route("/")
def home():
    return redirect(url_for("teacher"))


# CHATBOT PAGE
@app.route("/chatbot")
def chatbot():
    return render_template("index.html")


# TEACHER DASHBOARD
@app.route("/teacher")
def teacher():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            users.id,
            users.name,
            users.username,
            COALESCE(SUM(attendance.attended), 0) AS attended,
            COALESCE(SUM(attendance.total), 0) AS total
        FROM users
        LEFT JOIN attendance
        ON users.id = attendance.student_id
        WHERE users.role = 'student'
        GROUP BY users.id
        ORDER BY users.name
    """)

    students = cursor.fetchall()
    connection.close()

    student_list = []

    for student in students:
        attended = student["attended"]
        total = student["total"]

        percentage = (attended / total * 100) if total > 0 else 0

        student_list.append({
            "id": student["id"],
            "name": student["name"],
            "username": student["username"],
            "attended": attended,
            "total": total,
            "percentage": round(percentage, 1),
            "status": "Eligible" if percentage >= MIN_ATTENDANCE else "Below 75%"
        })

    return render_template(
        "teacher.html",
        students=student_list
    )


# ADD NEW STUDENT
@app.route("/teacher/add_student", methods=["POST"])
def add_student():

    name = request.form.get("name", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not name or not username or not password:
        return "Please fill in all student details.", 400

    if len(password) < 6:
        return "Password must contain at least 6 characters.", 400

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        connection.close()
        return "Username already exists. Please choose another.", 400

    password_hash = generate_password_hash(password)

    cursor.execute("""
        INSERT INTO users (name, username, password, role)
        VALUES (?, ?, ?, 'student')
    """, (name, username, password_hash))

    connection.commit()
    connection.close()

    return redirect(url_for("teacher"))


# UPDATE STUDENT ATTENDANCE
@app.route("/teacher/update", methods=["POST"])
def update_attendance():

    student_id = request.form.get("student_id")
    subject = request.form.get("subject", "").strip()

    try:
        student_id = int(student_id)
        attended = int(request.form.get("attended", 0))
        total = int(request.form.get("total", 0))
    except (ValueError, TypeError):
        return "Please enter valid numbers.", 400

    if not subject or attended < 0 or total < 0 or attended > total:
        return "Invalid attendance details.", 400

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id FROM users
        WHERE id = ? AND role = 'student'
    """, (student_id,))

    student = cursor.fetchone()

    if student is None:
        connection.close()
        return "Student not found.", 404

    cursor.execute("""
        SELECT id FROM attendance
        WHERE student_id = ? AND subject = ?
    """, (student_id, subject))

    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE attendance
            SET attended = ?, total = ?
            WHERE student_id = ? AND subject = ?
        """, (attended, total, student_id, subject))

    else:
        cursor.execute("""
            INSERT INTO attendance
            (student_id, subject, attended, total)
            VALUES (?, ?, ?, ?)
        """, (student_id, subject, attended, total))

    connection.commit()
    connection.close()

    return redirect(url_for("teacher"))


# CHATBOT API
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}
    message = data.get("message", "").lower()

    connection = get_db_connection()
    cursor = connection.cursor()

    search_name = (
        message.replace("what is", "")
        .replace("attendance", "")
        .replace("show", "")
        .replace("my", "")
        .strip()
    )

    cursor.execute("""
        SELECT
            users.name,
            SUM(attendance.attended) AS attended,
            SUM(attendance.total) AS total
        FROM users
        JOIN attendance
        ON users.id = attendance.student_id
        WHERE LOWER(users.name) LIKE ?
        GROUP BY users.id
    """, ("%" + search_name + "%",))

    student = cursor.fetchone()
    connection.close()

    if student is None:
        return jsonify({
            "reply": "I couldn't find that student. Try Sameed, Rahul or Priya."
        })

    attended = student["attended"]
    total = student["total"]

    if not total:
        return jsonify({
            "reply": "No attendance records are available for this student."
        })

    percentage = (attended / total) * 100

    max_misses = max(
        0,
        math.floor(attended / 0.75 - total)
    )

    if percentage < MIN_ATTENDANCE:
        classes_needed = math.ceil(
            (0.75 * total - attended) / 0.25
        )
    else:
        classes_needed = 0

    reply = (
        f"{student['name']}, your attendance is {percentage:.1f}%. "
        f"You attended {attended} out of {total} classes. "
        f"Minimum required attendance is 75%. "
        f"You can miss {max_misses} consecutive upcoming classes "
        f"without falling below 75%. "
        f"Classes to attend consecutively to reach 75%: "
        f"{classes_needed}."
    )

    return jsonify({"reply": reply})


# LOGOUT LINK
@app.route("/logout")
def logout():
    return redirect(url_for("home"))


# RUN APPLICATION
if __name__ == "__main__":
    app.run(debug=True)
