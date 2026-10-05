import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import mysql.connector


# -----------------------------
# MySQL Connection
# -----------------------------
def connect_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Shailesh1",
        database="ScholarshipFinancialAidDB"
    )


# -----------------------------
# View Students
# -----------------------------
def view_students():

    try:
        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Student")
        students = cursor.fetchall()

        cursor.close()
        connection.close()

        # New window
        student_window = tk.Toplevel(root)
        student_window.title("Student Records")
        student_window.geometry("1200x500")

        # Heading
        heading = tk.Label(
            student_window,
            text="STUDENT RECORDS",
            font=("Arial", 18, "bold")
        )
        heading.pack(pady=15)

        # Table
        columns = (
            "StudentID",
            "Name",
            "Email",
            "Phone",
            "DateOfBirth",
            "Gender",
            "Category",
            "Address",
            "FamilyIncome",
            "CGPA",
            "AdmissionYear",
            "Status",
            "CourseID"
        )

        table = ttk.Treeview(
            student_window,
            columns=columns,
            show="headings"
        )

        # Column headings
        for column in columns:
            table.heading(column, text=column)
            table.column(column, width=100)

        # Insert student records
        for student in students:
            table.insert("", tk.END, values=student)

        table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            student_window,
            orient="vertical",
            command=table.yview
        )

        table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not load students:\n\n{error}"
        )


# -----------------------------
# Other Buttons
# -----------------------------
def add_student():
    student_window = tk.Toplevel(root)
    student_window.title("Add Student")
    student_window.geometry("500x650")

    tk.Label(
        student_window,
        text="ADD STUDENT",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Label(student_window, text="Name:").pack(pady=5)
    name_entry = tk.Entry(student_window, width=35)
    name_entry.pack(pady=5)

    tk.Label(student_window, text="Email:").pack(pady=5)
    email_entry = tk.Entry(student_window, width=35)
    email_entry.pack(pady=5)

    tk.Label(student_window, text="Phone:").pack(pady=5)
    phone_entry = tk.Entry(student_window, width=35)
    phone_entry.pack(pady=5)

    tk.Label(student_window, text="Date of Birth (YYYY-MM-DD):").pack(pady=5)
    dob_entry = tk.Entry(student_window, width=35)
    dob_entry.pack(pady=5)

    tk.Label(student_window, text="Gender:").pack(pady=5)
    gender_box = ttk.Combobox(
        student_window,
        values=["Male", "Female", "Other"],
        state="readonly",
        width=32
    )
    gender_box.pack(pady=5)

    tk.Label(student_window, text="Category:").pack(pady=5)
    category_entry = tk.Entry(student_window, width=35)
    category_entry.pack(pady=5)

    tk.Label(student_window, text="Address:").pack(pady=5)
    address_entry = tk.Entry(student_window, width=35)
    address_entry.pack(pady=5)

    tk.Label(student_window, text="Family Income:").pack(pady=5)
    income_entry = tk.Entry(student_window, width=35)
    income_entry.pack(pady=5)

    tk.Label(student_window, text="CGPA:").pack(pady=5)
    cgpa_entry = tk.Entry(student_window, width=35)
    cgpa_entry.pack(pady=5)

    tk.Label(student_window, text="Admission Year:").pack(pady=5)
    year_entry = tk.Entry(student_window, width=35)
    year_entry.pack(pady=5)

    tk.Label(student_window, text="Status:").pack(pady=5)
    status_box = ttk.Combobox(
        student_window,
        values=["Active", "Inactive", "Graduated"],
        state="readonly",
        width=32
    )
    status_box.pack(pady=5)
    status_box.set("Active")

    tk.Label(student_window, text="Course ID:").pack(pady=5)
    course_entry = tk.Entry(student_window, width=35)
    course_entry.pack(pady=5)

    def save_student():
        name = name_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        dob = dob_entry.get()
        gender = gender_box.get()
        category = category_entry.get()
        address = address_entry.get()
        income = income_entry.get()
        cgpa = cgpa_entry.get()
        admission_year = year_entry.get()
        status = status_box.get()
        course_id = course_entry.get()

        if not name or not email or not phone:
            messagebox.showwarning(
                "Missing Information",
                "Please fill Name, Email and Phone."
            )
            return

        try:
            connection = connect_database()
            cursor = connection.cursor()

            query = """
                INSERT INTO Student
                (Name, Email, Phone, DateOfBirth, Gender, Category,
                 Address, FamilyIncome, CGPA, AdmissionYear, Status, CourseID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                name, email, phone, dob, gender, category,
                address, income, cgpa, admission_year, status, course_id
            )

            cursor.execute(query, values)
            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Student added successfully!"
            )

            student_window.destroy()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not add student:\n\n{error}"
            )

    tk.Button(
        student_window,
        text="SAVE STUDENT",
        command=save_student,
        width=25
    ).pack(pady=20)

def update_student():
    student_id = simpledialog.askinteger(
        "Update Student",
        "Enter Student ID to update:"
    )

    if student_id is None:
        return

    try:
        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT Name, Email, Phone, Category, Address, FamilyIncome, CGPA, Status FROM Student WHERE StudentID = %s",
            (student_id,)
        )

        student = cursor.fetchone()

        cursor.close()
        connection.close()

        if student is None:
            messagebox.showwarning(
                "Not Found",
                "Student ID not found."
            )
            return

        update_window = tk.Toplevel(root)
        update_window.title("Update Student")
        update_window.geometry("500x500")

        tk.Label(
            update_window,
            text="UPDATE STUDENT",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        tk.Label(update_window, text="Name:").pack()
        name_entry = tk.Entry(update_window, width=35)
        name_entry.pack(pady=3)
        name_entry.insert(0, student[0])

        tk.Label(update_window, text="Email:").pack()
        email_entry = tk.Entry(update_window, width=35)
        email_entry.pack(pady=3)
        email_entry.insert(0, student[1])

        tk.Label(update_window, text="Phone:").pack()
        phone_entry = tk.Entry(update_window, width=35)
        phone_entry.pack(pady=3)
        phone_entry.insert(0, student[2])

        tk.Label(update_window, text="Category:").pack()
        category_entry = tk.Entry(update_window, width=35)
        category_entry.pack(pady=3)
        category_entry.insert(0, student[3] or "")

        tk.Label(update_window, text="Address:").pack()
        address_entry = tk.Entry(update_window, width=35)
        address_entry.pack(pady=3)
        address_entry.insert(0, student[4] or "")

        tk.Label(update_window, text="Family Income:").pack()
        income_entry = tk.Entry(update_window, width=35)
        income_entry.pack(pady=3)
        income_entry.insert(0, student[5] or "")

        tk.Label(update_window, text="CGPA:").pack()
        cgpa_entry = tk.Entry(update_window, width=35)
        cgpa_entry.pack(pady=3)
        cgpa_entry.insert(0, student[6] or "")

        tk.Label(update_window, text="Status:").pack()
        status_box = ttk.Combobox(
            update_window,
            values=["Active", "Inactive", "Graduated"],
            state="readonly",
            width=32
        )
        status_box.pack(pady=3)
        status_box.set(student[7] or "Active")

        def save_update():
            try:
                connection = connect_database()
                cursor = connection.cursor()

                cursor.execute(
                    """
                    UPDATE Student
                    SET Name=%s, Email=%s, Phone=%s, Category=%s,
                        Address=%s, FamilyIncome=%s, CGPA=%s, Status=%s
                    WHERE StudentID=%s
                    """,
                    (
                        name_entry.get(),
                        email_entry.get(),
                        phone_entry.get(),
                        category_entry.get(),
                        address_entry.get(),
                        income_entry.get(),
                        cgpa_entry.get(),
                        status_box.get(),
                        student_id
                    )
                )

                connection.commit()
                cursor.close()
                connection.close()

                messagebox.showinfo(
                    "Success",
                    "Student updated successfully!"
                )

                update_window.destroy()

            except mysql.connector.Error as error:
                messagebox.showerror(
                    "Database Error",
                    f"Could not update student:\n\n{error}"
                )

        tk.Button(
            update_window,
            text="UPDATE STUDENT",
            command=save_update,
            width=25
        ).pack(pady=15)
        
    except mysql.connector.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not update student:\n\n{error}"
        )
        
def view_scholarships():

    try:
        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Scholarship")
        scholarships = cursor.fetchall()

        cursor.close()
        connection.close()

        # New window
        scholarship_window = tk.Toplevel(root)
        scholarship_window.title("Scholarship Records")
        scholarship_window.geometry("1300x550")

        # Heading
        heading = tk.Label(
            scholarship_window,
            text="SCHOLARSHIP RECORDS",
            font=("Arial", 18, "bold")
        )
        heading.pack(pady=15)

        # Get column names directly from MySQL

        # Create table using the actual Scholarship columns
        columns = (
            "ScholarshipID",
            "Title",
            "Description",
            "Type",
            "Amount",
            "MinCGPA",
            "EligibilityCriteriaID",
            "DonorID",
            "ApplicationDeadline",
            "Status"
        )

        table = ttk.Treeview(
            scholarship_window,
            columns=columns,
            show="headings"
        )

        # Column headings
        for column in columns:
            table.heading(column, text=column)
            table.column(column, width=120)

        # Insert records
        for scholarship in scholarships:
            table.insert("", tk.END, values=scholarship)

        table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # Horizontal scrollbar
        horizontal_scrollbar = ttk.Scrollbar(
            scholarship_window,
            orient="horizontal",
            command=table.xview
        )

        table.configure(
            xscrollcommand=horizontal_scrollbar.set
        )

        horizontal_scrollbar.pack(
            side="bottom",
            fill="x"
        )

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not load scholarships:\n\n{error}"
        )


def view_applications():
    try:
        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Application")
        applications = cursor.fetchall()

        cursor.close()
        connection.close()

        # New window
        application_window = tk.Toplevel(root)
        application_window.title("Application Records")
        application_window.geometry("1300x550")

        # Heading
        heading = tk.Label(
            application_window,
            text="APPLICATION RECORDS",
            font=("Arial", 18, "bold")
        )
        heading.pack(pady=15)

        # Columns
        columns = (
            "ApplicationID",
            "StudentID",
            "ScholarshipID",
            "ApplyDate",
            "Status",
            "Remarks"
        )

        table = ttk.Treeview(
            application_window,
            columns=columns,
            show="headings"
        )

        for column in columns:
            table.heading(column, text=column)
            table.column(column, width=180)

        # Insert data
        for application in applications:
            table.insert("", tk.END, values=application)

        table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not load applications:\n\n{error}"
        )


def add_application():
    # Create new window
    application_window = tk.Toplevel(root)
    application_window.title("Add Application")
    application_window.geometry("500x500")

    # Heading
    heading = tk.Label(
        application_window,
        text="ADD APPLICATION",
        font=("Arial", 18, "bold")
    )
    heading.pack(pady=20)

    # Student ID
    tk.Label(
        application_window,
        text="Student ID:"
    ).pack(pady=5)

    student_entry = tk.Entry(application_window, width=35)
    student_entry.pack(pady=5)

    # Scholarship ID
    tk.Label(
        application_window,
        text="Scholarship ID:"
    ).pack(pady=5)

    scholarship_entry = tk.Entry(application_window, width=35)
    scholarship_entry.pack(pady=5)

    # Apply Date
    tk.Label(
        application_window,
        text="Apply Date (YYYY-MM-DD):"
    ).pack(pady=5)

    date_entry = tk.Entry(application_window, width=35)
    date_entry.pack(pady=5)

    # Status
    tk.Label(
        application_window,
        text="Status:"
    ).pack(pady=5)

    status_box = ttk.Combobox(
        application_window,
        values=["Pending", "Approved", "Under Review", "Rejected"],
        state="readonly",
        width=32
    )
    status_box.pack(pady=5)
    status_box.set("Pending")

    # Remarks
    tk.Label(
        application_window,
        text="Remarks:"
    ).pack(pady=5)

    remarks_entry = tk.Entry(application_window, width=35)
    remarks_entry.pack(pady=5)

    # Save Application
    def save_application():
        student_id = student_entry.get()
        scholarship_id = scholarship_entry.get()
        apply_date = date_entry.get()
        status = status_box.get()
        remarks = remarks_entry.get()

        if not student_id or not scholarship_id or not apply_date:
            messagebox.showwarning(
                "Missing Information",
                "Please fill Student ID, Scholarship ID and Apply Date."
            )
            return

        try:
            connection = connect_database()
            cursor = connection.cursor()

            query = """
                INSERT INTO Application
                (StudentID, ScholarshipID, ApplyDate, Status, Remarks)
                VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                student_id,
                scholarship_id,
                apply_date,
                status,
                remarks
            )

            cursor.execute(query, values)
            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Application added successfully!"
            )

            application_window.destroy()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not add application:\n\n{error}"
            )

    # Button
    tk.Button(
        application_window,
        text="SAVE APPLICATION",
        command=save_application,
        width=25
    ).pack(pady=20)


def delete_application():
    application_id = simpledialog.askinteger(
        "Delete Application",
        "Enter Application ID to delete:"
    )

    if application_id is None:
        return

    try:
        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM Application WHERE ApplicationID = %s",
            (application_id,)
        )

        if cursor.rowcount == 0:
            messagebox.showwarning(
                "Not Found",
                "Application ID not found."
            )
        else:
            connection.commit()
            messagebox.showinfo(
                "Success",
                "Application deleted successfully!"
            )

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not delete application:\n\n{error}"
        )

def update_application():
    application_id = simpledialog.askinteger(
        "Update Application",
        "Enter Application ID to update:"
    )

    if application_id is None:
        return

    try:
        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT Status, Remarks FROM Application WHERE ApplicationID = %s",
            (application_id,)
        )

        application = cursor.fetchone()

        cursor.close()
        connection.close()

        if application is None:
            messagebox.showwarning(
                "Not Found",
                "Application ID not found."
            )
            return

        update_window = tk.Toplevel(root)
        update_window.title("Update Application")
        update_window.geometry("500x350")

        tk.Label(
            update_window,
            text="UPDATE APPLICATION",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(
            update_window,
            text="Status:"
        ).pack(pady=5)

        status_box = ttk.Combobox(
            update_window,
            values=["Pending", "Approved", "Under Review", "Rejected"],
            state="readonly",
            width=32
        )
        status_box.pack(pady=5)
        status_box.set(application[0])

        tk.Label(
            update_window,
            text="Remarks:"
        ).pack(pady=5)

        remarks_entry = tk.Entry(
            update_window,
            width=35
        )
        remarks_entry.pack(pady=5)
        remarks_entry.insert(0, application[1] or "")

        def save_update():
            new_status = status_box.get()
            new_remarks = remarks_entry.get()

            try:
                connection = connect_database()
                cursor = connection.cursor()

                cursor.execute(
                    """
                    UPDATE Application
                    SET Status = %s, Remarks = %s
                    WHERE ApplicationID = %s
                    """,
                    (new_status, new_remarks, application_id)
                )

                connection.commit()

                cursor.close()
                connection.close()

                messagebox.showinfo(
                    "Success",
                    "Application updated successfully!"
                )

                update_window.destroy()

            except mysql.connector.Error as error:
                messagebox.showerror(
                    "Database Error",
                    f"Could not update application:\n\n{error}"
                )

        tk.Button(
            update_window,
            text="UPDATE APPLICATION",
            command=save_update,
            width=25
        ).pack(pady=20)

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not load application:\n\n{error}"
        )
# -----------------------------
# Main Window
# -----------------------------
root = tk.Tk()

root.title("Scholarship & Financial Aid Management System")
root.geometry("900x600")
root.resizable(False, False)


# Title
title = tk.Label(
    root,
    text="SCHOLARSHIP & FINANCIAL AID MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold")
)

title.pack(pady=30)


subtitle = tk.Label(
    root,
    text="Database Management System Project",
    font=("Arial", 12)
)

subtitle.pack(pady=5)


# -----------------------------
# Buttons
# -----------------------------

tk.Button(
    root,
    text="VIEW STUDENTS",
    command=view_students,
    width=25
).pack(pady=10)

tk.Button(
    root,
    text="ADD STUDENT",
    command=add_student,
    width=25
).pack(pady=10)

tk.Button(
    root,
    text="UPDATE STUDENT",
    command=update_student,
    width=25
).pack(pady=10)

tk.Button(
    root,
    text="VIEW APPLICATIONS",
    command=view_applications,
    width=25
).pack(pady=10)

tk.Button(
    root,
    text="ADD APPLICATION",
    command=add_application,
    width=25
).pack(pady=10)

tk.Button(
    root,
    text="DELETE APPLICATION",
    command=delete_application,
    width=25
).pack(pady=10)

tk.Button(
    root,
    text="UPDATE APPLICATION",
    command=update_application,
    width=25
).pack(pady=10)


# Start application
root.mainloop()