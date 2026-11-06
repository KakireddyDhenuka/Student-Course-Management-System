import configparser
import mysql.connector

def read_config():
    config = configparser.ConfigParser()
    loaded = config.read("config.ini")
    if not loaded:
        raise FileNotFoundError(
            "config.ini was not found. Copy config.example.ini to config.ini "
            "and enter your MySQL password."
        )
    return config["mysql"]

def get_connection():
    settings = read_config()
    return mysql.connector.connect(
        host=settings.get("host", "localhost"),
        port=settings.getint("port", 3306),
        user=settings.get("user", "root"),
        password=settings.get("password", ""),
        database=settings.get("database", "student_management")
    )

def initialize_database():
    settings = read_config()
    # First connect without selecting a database so it can be created.
    conn = mysql.connector.connect(
        host=settings.get("host", "localhost"),
        port=settings.getint("port", 3306),
        user=settings.get("user", "root"),
        password=settings.get("password", "")
    )
    cur = conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS student_management")
    cur.close()
    conn.close()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            student_name VARCHAR(100) NOT NULL,
            age INT NOT NULL,
            email VARCHAR(150) NOT NULL UNIQUE,
            department VARCHAR(50) NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id INT AUTO_INCREMENT PRIMARY KEY,
            course_name VARCHAR(100) NOT NULL UNIQUE,
            duration_months INT NOT NULL,
            fee DECIMAL(10,2) NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT NOT NULL,
            course_id INT NOT NULL,
            enrollment_date DATE NOT NULL,
            CONSTRAINT fk_student FOREIGN KEY (student_id)
                REFERENCES students(student_id) ON DELETE CASCADE,
            CONSTRAINT fk_course FOREIGN KEY (course_id)
                REFERENCES courses(course_id) ON DELETE CASCADE,
            CONSTRAINT unique_student_course UNIQUE (student_id, course_id)
        )
    """)
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM courses")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO courses (course_name, duration_months, fee) VALUES (%s,%s,%s)",
            [
                ("Python Programming", 3, 5000),
                ("SQL and Database", 2, 3000),
                ("Java Programming", 4, 6000),
                ("Web Development", 3, 4500),
                ("Data Science", 5, 8000)
            ]
        )
    cur.execute("SELECT COUNT(*) FROM students")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            """INSERT INTO students
               (student_name, age, email, department)
               VALUES (%s,%s,%s,%s)""",
            [
                ("Dhenuka", 21, "dhenuka@example.com", "CSE"),
                ("Akanksha", 21, "akanksha@example.com", "ECE"),
                ("Asmitha", 20, "asmitha@example.com", "CSE"),
                ("Usha", 21, "usha@example.com", "IT")
            ]
        )
    conn.commit()
    cur.close()
    conn.close()
