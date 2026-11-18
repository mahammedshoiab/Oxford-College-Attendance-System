
# The Oxford College of Engineering
## College Attendance Management System

A web-based college attendance management project developed using Python, Flask, SQLite, HTML, CSS, and JavaScript.

The application provides a teacher dashboard to manage students, update attendance, monitor attendance percentages, and interact with an attendance chatbot.

---

## 1. Project Objectives

- Manage student attendance records.
- Display student attendance details.
- Calculate attendance percentages automatically.
- Identify students below 75% attendance.
- Register new students.
- Update subject-wise attendance.
- Provide an AI-style chatbot interface for attendance queries.

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| SQLite | Database management |
| HTML | Frontend structure |
| CSS | Website design and styling |
| JavaScript | Chatbot functionality |
| Git | Version control |
| GitHub | Source code hosting |

## 3. Project Features

### Teacher Dashboard
- Total registered students.
- Average attendance percentage.
- Eligible students count.
- Low attendance alerts.
- Student attendance table.

### Student Management
- Add new students.
- Create student usernames.
- Create student passwords.
- Store student details in SQLite.

### Attendance Management
- Select students.
- Enter subject names.
- Update classes attended.
- Update total classes.
- Calculate attendance percentage.
- Check the minimum 75% attendance requirement.

### Attendance Chatbot
- Ask questions about student attendance.
- Search student attendance by name.
- Display attendance percentages.
- Calculate how many classes a student needs to attend to reach 75%.

## 4. Project Folder Structure

```text
CollegeAttendanceChatbot/
│
├── app.py
├── init_db.py
├── attendance.db
│
├── templates/
│   ├── index.html
│   └── teacher.html
│
├── static/
│   └── style.css
│
└── README.md
```

The database file is created locally and should not be published if it contains personal student information.

## 5. Database Structure

The application uses SQLite with two main tables.

### Users Table

| Column | Description |
|---|---|
| id | Unique user ID |
| name | Student name |
| username | Student username |
| password | Student password |
| role | Student or teacher |

### Attendance Table

| Column | Description |
|---|---|
| id | Attendance record ID |
| student_id | Student reference ID |
| subject | Subject name |
| attended | Classes attended |
| total | Total classes |

## 6. Attendance Calculation

The application calculates attendance using:

```python
attendance_percentage = (attended / total) * 100
```

Minimum attendance requirement:

```python
MIN_ATTENDANCE = 75
```

Student eligibility:

- 75% or above: Eligible
- Below 75%: Low Attendance

## 7. Application Workflow

1. Teacher opens the attendance dashboard.
2. Flask retrieves student information from SQLite.
3. Dashboard displays student attendance details.
4. Teacher can register new students.
5. Teacher can update subject-wise attendance.
6. Database stores the updated attendance.
7. Chatbot receives student attendance questions.
8. Flask processes the questions and returns attendance information.

## 8. Installation and Setup

### Requirements

- Python 3
- Flask
- SQLite
- Visual Studio Code

### Step 1: Clone the Repository

```bash
git clone https://github.com/mahammedshoiab/Oxford-College-Attendance-System.git
```

### Step 2: Open Project Folder

```bash
cd Oxford-College-Attendance-System
```

### Step 3: Install Flask

```bash
pip install flask
```

### Step 4: Initialize Database

If the database has not already been created:

```bash
python init_db.py
```

Check the initialization script before running it on an existing database because it may reset existing records.

### Step 5: Run Application

```bash
python app.py
```

### Step 6: Open in Browser

Teacher Dashboard:

```text
http://127.0.0.1:5000/
```

Attendance Dashboard:

```text
http://127.0.0.1:5000/teacher
```

Student Chatbot:

```text
http://127.0.0.1:5000/chatbot
```

## 9. Main Flask Routes

| Route | Method | Function |
|---|---|---|
| `/` | GET | Opens teacher dashboard |
| `/teacher` | GET | Displays attendance dashboard |
| `/teacher/add_student` | POST | Registers new student |
| `/teacher/update` | POST | Updates attendance |
| `/chatbot` | GET | Opens chatbot |
| `/chat` | POST | Processes chatbot questions |
| `/logout` | GET | Redirects to home |

## 10. How I Developed This Project

1. Planned the college attendance management system.
2. Created the project folder structure using VS Code.
3. Developed the backend using Python and Flask.
4. Created SQLite database tables for users and attendance.
5. Designed the teacher dashboard using HTML and CSS.
6. Implemented student registration functionality.
7. Developed attendance update functionality.
8. Created an attendance chatbot using JavaScript and Flask API.
9. Connected the frontend with the backend and database.
10. Tested the application locally.
11. Uploaded the source code to GitHub using Git.

## 11. Future Enhancements

- Student login and authentication.
- Teacher login and authentication.
- Individual student dashboard.
- Attendance reports and downloadable PDFs.
- Attendance tracking by date.
- Search and filter student records.
- Improved chatbot language understanding.
- Deployment to a cloud platform.

## 12. Security Notes

- Add authentication and role-based access before real-world use.
- Protect teacher routes from unauthorized access.
- Do not upload real student records or passwords to a public repository.
- Keep database files and secret configuration out of GitHub.
- New student passwords are stored as Werkzeug hashes, but existing demo accounts may use a different format.

The current project is a learning/demo application and does not yet have complete login and access protection.

## 13. GitHub Repository

Project Repository:

https://github.com/mahammedshoiab/Oxford-College-Attendance-System

---

## Project Information

**Project Name:** College Attendance Management System

**Institution:** The Oxford College of Engineering

**Backend:** Python and Flask

**Database:** SQLite

**Frontend:** HTML, CSS and JavaScript

**Project Type:** Web-Based Application
