# Student Course Management System

A beginner-friendly desktop application built with **Python, Tkinter and MySQL**.
It allows users to manage student records, view courses and enroll students.

## Features

- View, add, update and delete student records
- View available courses
- Enroll a student in a course
- View enrollment records
- MySQL relational database with primary keys, foreign keys and constraints

## Technologies

- Python 3
- Tkinter (included with most standard Python installations)
- MySQL Server
- mysql-connector-python

## Requirements

1. Install Python 3.
2. Install and start MySQL Server (or start MySQL through XAMPP).
3. Have a MySQL account, such as `root`.

## Run in VS Code

1. Extract this ZIP file.
2. Open the extracted `Student-Course-Management-System` folder in VS Code.
3. Open the VS Code terminal.
4. Install the Python dependency:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Copy `config.example.ini` and rename the copy to `config.ini`.
6. Open `config.ini` and enter your MySQL username and password.
   - For a local MySQL root account with no password, leave `password =` blank.
   - Keep `database = student_management`.
7. Make sure the MySQL server is running.
8. Run the application:

   ```bash
   python app.py
   ```

The application creates the database and tables automatically and inserts a few
sample students and courses the first time it runs.

## Project files

- `app.py` - Tkinter graphical user interface and application operations
- `db.py` - MySQL connection and database initialization
- `database.sql` - SQL schema for reference or manual setup
- `config.example.ini` - Example database configuration
- `requirements.txt` - Python package dependency

## Important

Do not upload your real `config.ini` to a public GitHub repository because it
may contain your database password. The `.gitignore` file excludes it.
