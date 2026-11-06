import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection, initialize_database

BG = "#f4f7fb"
BLUE = "#315b96"
DARK = "#203047"

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Course Management System")
        self.root.geometry("1080x700")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)
        self.build_ui()
        self.refresh_students()
        self.refresh_courses()
        self.refresh_enrollments()

    def build_ui(self):
        header = tk.Frame(self.root, bg=BLUE, height=78)
        header.pack(fill="x")
        tk.Label(header, text="Student Course Management System",
                 bg=BLUE, fg="white", font=("Segoe UI", 20, "bold")).pack(
                     anchor="w", padx=24, pady=(14, 0))
        tk.Label(header, text="Manage students, courses and enrollments",
                 bg=BLUE, fg="#e5eefb", font=("Segoe UI", 10)).pack(
                     anchor="w", padx=26, pady=(2, 12))

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=18, pady=18)

        self.students_tab = tk.Frame(self.tabs, bg=BG)
        self.courses_tab = tk.Frame(self.tabs, bg=BG)
        self.enroll_tab = tk.Frame(self.tabs, bg=BG)
        self.tabs.add(self.students_tab, text="  Students  ")
        self.tabs.add(self.courses_tab, text="  Courses  ")
        self.tabs.add(self.enroll_tab, text="  Enrollments  ")

        self.build_students_tab()
        self.build_courses_tab()
        self.build_enroll_tab()

    def build_students_tab(self):
        form = tk.LabelFrame(self.students_tab, text="Student details",
                             bg=BG, fg=DARK, padx=12, pady=12,
                             font=("Segoe UI", 10, "bold"))
        form.pack(fill="x", padx=12, pady=12)

        self.student_id = tk.StringVar()
        self.student_name = tk.StringVar()
        self.age = tk.StringVar()
        self.email = tk.StringVar()
        self.department = tk.StringVar()

        fields = [
            ("Student ID", self.student_id),
            ("Name", self.student_name),
            ("Age", self.age),
            ("Email", self.email),
            ("Department", self.department)
        ]
        for i, (label, variable) in enumerate(fields):
            tk.Label(form, text=label, bg=BG, fg=DARK).grid(
                row=0, column=i, sticky="w", padx=5, pady=(0, 4))
            entry = ttk.Entry(form, textvariable=variable, width=19)
            entry.grid(row=1, column=i, padx=5, pady=3, sticky="ew")
            if i == 0:
                entry.configure(state="readonly")

        buttons = tk.Frame(form, bg=BG)
        buttons.grid(row=2, column=0, columnspan=5, sticky="w", pady=(12, 0))
        ttk.Button(buttons, text="Add Student", command=self.add_student).pack(side="left", padx=4)
        ttk.Button(buttons, text="Update Selected", command=self.update_student).pack(side="left", padx=4)
        ttk.Button(buttons, text="Delete Selected", command=self.delete_student).pack(side="left", padx=4)
        ttk.Button(buttons, text="Clear Form", command=self.clear_form).pack(side="left", padx=4)
        ttk.Button(buttons, text="Refresh", command=self.refresh_students).pack(side="left", padx=4)

        table_frame = tk.Frame(self.students_tab, bg=BG)
        table_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        cols = ("id", "name", "age", "email", "department")
        self.student_tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        headings = {"id":"ID", "name":"Student Name", "age":"Age",
                    "email":"Email", "department":"Department"}
        widths = {"id":70, "name":190, "age":70, "email":260, "department":150}
        for col in cols:
            self.student_tree.heading(col, text=headings[col])
            self.student_tree.column(col, width=widths[col], anchor="center")
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.student_tree.yview)
        self.student_tree.configure(yscrollcommand=scroll.set)
        self.student_tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.student_tree.bind("<<TreeviewSelect>>", self.select_student)

    def build_courses_tab(self):
        tk.Label(self.courses_tab, text="Available Courses",
                 bg=BG, fg=DARK, font=("Segoe UI", 16, "bold")).pack(
                     anchor="w", padx=18, pady=18)
        cols = ("id", "name", "duration", "fee")
        self.course_tree = ttk.Treeview(self.courses_tab, columns=cols, show="headings")
        headings = {"id":"Course ID", "name":"Course Name",
                    "duration":"Duration (months)", "fee":"Fee"}
        for col in cols:
            self.course_tree.heading(col, text=headings[col])
            self.course_tree.column(col, anchor="center", width=200)
        self.course_tree.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        ttk.Button(self.courses_tab, text="Refresh Courses",
                   command=self.refresh_courses).pack(anchor="e", padx=18, pady=(0, 18))

    def build_enroll_tab(self):
        form = tk.LabelFrame(self.enroll_tab, text="Enroll a student",
                             bg=BG, fg=DARK, padx=14, pady=14,
                             font=("Segoe UI", 10, "bold"))
        form.pack(fill="x", padx=14, pady=14)

        tk.Label(form, text="Student", bg=BG).grid(row=0, column=0, padx=6, pady=6)
        self.enroll_student = ttk.Combobox(form, state="readonly", width=34)
        self.enroll_student.grid(row=0, column=1, padx=6, pady=6)

        tk.Label(form, text="Course", bg=BG).grid(row=0, column=2, padx=6, pady=6)
        self.enroll_course = ttk.Combobox(form, state="readonly", width=34)
        self.enroll_course.grid(row=0, column=3, padx=6, pady=6)

        ttk.Button(form, text="Enroll Student",
                   command=self.add_enrollment).grid(row=0, column=4, padx=10)

        tk.Label(self.enroll_tab, text="Enrollment Records",
                 bg=BG, fg=DARK, font=("Segoe UI", 14, "bold")).pack(
                     anchor="w", padx=16, pady=(8, 6))
        cols = ("enrollment_id", "student", "course", "date")
        self.enroll_tree = ttk.Treeview(self.enroll_tab, columns=cols, show="headings")
        headings = {"enrollment_id":"Enrollment ID", "student":"Student",
                    "course":"Course", "date":"Enrollment Date"}
        for col in cols:
            self.enroll_tree.heading(col, text=headings[col])
            self.enroll_tree.column(col, anchor="center", width=210)
        self.enroll_tree.pack(fill="both", expand=True, padx=14, pady=(0, 12))
        ttk.Button(self.enroll_tab, text="Refresh Enrollments",
                   command=self.refresh_enrollments).pack(anchor="e", padx=14, pady=(0, 14))

    def connect(self):
        return get_connection()

    def add_student(self):
        data = self.get_form_data()
        if not data:
            return
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO students (student_name, age, email, department) VALUES (%s,%s,%s,%s)",
                data)
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Success", "Student added successfully.")
            self.clear_form()
            self.refresh_students()
        except Exception as e:
            messagebox.showerror("Database error", str(e))

    def update_student(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("Select student", "Select a student from the table first.")
            return
        data = self.get_form_data()
        if not data:
            return
        student_id = self.student_tree.item(selected[0])["values"][0]
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(
                """UPDATE students SET student_name=%s, age=%s, email=%s,
                   department=%s WHERE student_id=%s""",
                (*data, student_id))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Success", "Student updated successfully.")
            self.clear_form()
            self.refresh_students()
        except Exception as e:
            messagebox.showerror("Database error", str(e))

    def delete_student(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("Select student", "Select a student from the table first.")
            return
        student_id = self.student_tree.item(selected[0])["values"][0]
        if not messagebox.askyesno("Confirm delete", "Delete this student and their enrollments?"):
            return
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("DELETE FROM enrollments WHERE student_id=%s", (student_id,))
            cur.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
            conn.commit()
            cur.close()
            conn.close()
            self.clear_form()
            self.refresh_students()
            self.refresh_enrollments()
            self.refresh_student_choices()
            messagebox.showinfo("Deleted", "Student deleted.")
        except Exception as e:
            messagebox.showerror("Database error", str(e))

    def get_form_data(self):
        name = self.student_name.get().strip()
        age_text = self.age.get().strip()
        email = self.email.get().strip()
        department = self.department.get().strip()
        if not all([name, age_text, email, department]):
            messagebox.showwarning("Missing details", "Please fill in all student fields.")
            return None
        try:
            age = int(age_text)
            if age <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid age", "Age must be a positive whole number.")
            return None
        return (name, age, email, department)

    def select_student(self, _event=None):
        selected = self.student_tree.selection()
        if not selected:
            return
        values = self.student_tree.item(selected[0])["values"]
        self.student_id.set(values[0])
        self.student_name.set(values[1])
        self.age.set(values[2])
        self.email.set(values[3])
        self.department.set(values[4])

    def clear_form(self):
        for variable in (self.student_id, self.student_name, self.age,
                         self.email, self.department):
            variable.set("")
        for item in self.student_tree.selection():
            self.student_tree.selection_remove(item)

    def refresh_students(self):
        if not hasattr(self, "student_tree"):
            return
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("SELECT student_id, student_name, age, email, department FROM students ORDER BY student_id")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            self.student_tree.delete(*self.student_tree.get_children())
            for row in rows:
                self.student_tree.insert("", "end", values=row)
            self.refresh_student_choices()
        except Exception as e:
            messagebox.showerror("Database error", str(e))

    def refresh_courses(self):
        if not hasattr(self, "course_tree"):
            return
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("SELECT course_id, course_name, duration_months, fee FROM courses ORDER BY course_id")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            self.course_tree.delete(*self.course_tree.get_children())
            for row in rows:
                self.course_tree.insert("", "end", values=row)
            self.refresh_course_choices()
        except Exception as e:
            messagebox.showerror("Database error", str(e))

    def refresh_student_choices(self):
        if not hasattr(self, "enroll_student"):
            return
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("SELECT student_id, student_name FROM students ORDER BY student_name")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            self.student_map = {f"{name} (ID: {sid})": sid for sid, name in rows}
            self.enroll_student["values"] = list(self.student_map.keys())
        except Exception:
            pass

    def refresh_course_choices(self):
        if not hasattr(self, "enroll_course"):
            return
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("SELECT course_id, course_name FROM courses ORDER BY course_name")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            self.course_map = {f"{name} (ID: {cid})": cid for cid, name in rows}
            self.enroll_course["values"] = list(self.course_map.keys())
        except Exception:
            pass

    def add_enrollment(self):
        student_label = self.enroll_student.get()
        course_label = self.enroll_course.get()
        if not student_label or not course_label:
            messagebox.showwarning("Missing selection", "Choose both a student and a course.")
            return
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO enrollments (student_id, course_id, enrollment_date) VALUES (%s,%s,%s)",
                (self.student_map[student_label], self.course_map[course_label],
                 __import__("datetime").date.today()))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Success", "Student enrolled successfully.")
            self.refresh_enrollments()
        except Exception as e:
            messagebox.showerror("Database error", str(e))

    def refresh_enrollments(self):
        if not hasattr(self, "enroll_tree"):
            return
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("""
                SELECT e.enrollment_id, s.student_name, c.course_name, e.enrollment_date
                FROM enrollments e
                JOIN students s ON e.student_id = s.student_id
                JOIN courses c ON e.course_id = c.course_id
                ORDER BY e.enrollment_id
            """)
            rows = cur.fetchall()
            cur.close()
            conn.close()
            self.enroll_tree.delete(*self.enroll_tree.get_children())
            for row in rows:
                self.enroll_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Database error", str(e))


if __name__ == "__main__":
    try:
        initialize_database()
        root = tk.Tk()
        app = StudentApp(root)
        root.mainloop()
    except Exception as error:
        messagebox.showerror(
            "Cannot start application",
            f"{error}\n\nCheck MySQL is running and config.ini has correct credentials."
        )
