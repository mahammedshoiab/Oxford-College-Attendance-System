
import sqlite3

connection = sqlite3.connect("attendance.db")
cursor = connection.cursor()

# Student and teacher accounts
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# Attendance records
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    attended INTEGER DEFAULT 0,
    total INTEGER DEFAULT 0,
    FOREIGN KEY (student_id) REFERENCES users(id)
)
""")

# Sample student accounts
sample_users = [
    ("Sameed", "sameed", "student123", "student"),
    ("Rahul", "rahul", "student123", "student"),
    ("Priya", "priya", "student123", "student"),
    ("Teacher", "teacher", "teacher123", "teacher")
]

for user in sample_users:
    cursor.execute("""
    INSERT OR IGNORE INTO users (name, username, password, role)
    VALUES (?, ?, ?, ?)
    """, user)

# Sample attendance records
sample_attendance = [
    ("sameed", "Python", 41, 50),
    ("rahul", "Python", 35, 50),
    ("priya", "Python", 45, 50)
]

for username, subject, attended, total in sample_attendance:
    cursor.execute("""
    SELECT id FROM users WHERE username = ?
    """, (username,))

    student_id = cursor.fetchone()[0]

    cursor.execute("""
    INSERT INTO attendance (student_id, subject, attended, total)
    SELECT ?, ?, ?, ?
    WHERE NOT EXISTS (
        SELECT 1 FROM attendance
        WHERE student_id = ? AND subject = ?
    )
    """, (student_id, subject, attended, total, student_id, subject))

connection.commit()
connection.close()

print("Database created successfully!")
