import streamlit as st
import sqlite3
import pandas as pd

# 1. Connect to Database (File will be created automatically)
def get_connection():
    conn = sqlite3.connect("students.db", check_same_thread=False)
    return conn

# 2. Create Table (Only first time)
def create_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            roll_no TEXT,
            branch TEXT,
            phone TEXT,
            marks INTEGER
        )
    """)
    conn.commit()
    conn.close()

create_table()

st.title("🎓 Student Database Management System")
st.write("Manage student records easily - Add, View, Update, Delete, Search")

menu = st.sidebar.selectbox("Menu", ["Add Student", "View Students", "Update Student", "Delete Student", "Search Student"])

# 1. ADD - CREATE
if menu == "Add Student":
    st.header("➕ Add New Student")
    name = st.text_input("Name")
    roll = st.text_input("Roll No")
    branch = st.selectbox("Branch", ["CSE", "ECE", "EEE", "MECH", "CIVIL"])
    phone = st.text_input("Phone")
    marks = st.number_input("Marks", 0, 100)
    if st.button("Add Student"):
        if name == "" or roll == "":
            st.warning("Please enter Name and Roll No")
        else:
            conn = get_connection()
            conn.execute("INSERT INTO students (name, roll_no, branch, phone, marks) VALUES (?,?,?,?,?)", (name, roll, branch, phone, marks))
            conn.commit()
            conn.close()
            st.success(f"Student {name} Added Successfully!")

# 2. VIEW - READ
elif menu == "View Students":
    st.header("📋 All Students")
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()
    if len(df) == 0:
        st.info("No students yet. Go to Add Student and add one.")
    else:
        st.dataframe(df, use_container_width=True)
        st.write(f"Total Students: {len(df)}")

# 3. UPDATE
elif menu == "Update Student":
    st.header("✏️ Update Student")
    roll = st.text_input("Enter Roll No to Update")
    phone = st.text_input("New Phone Number")
    marks = st.number_input("New Marks", 0, 100)
    if st.button("Update"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE students SET phone=?, marks=? WHERE roll_no=?", (phone, marks, roll))
        conn.commit()
        conn.close()
        if cur.rowcount == 0:
            st.error("No student found with that Roll No")
        else:
            st.success("Updated Successfully!")

# 4. DELETE
elif menu == "Delete Student":
    st.header("🗑️ Delete Student")
    roll = st.text_input("Enter Roll No to Delete")
    if st.button("Delete"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE roll_no=?", (roll,))
        conn.commit()
        conn.close()
        if cur.rowcount == 0:
            st.error("No student found with that Roll No")
        else:
            st.success("Deleted Successfully!")

# 5. SEARCH
elif menu == "Search Student":
    st.header("🔍 Search Student")
    name = st.text_input("Enter Name or Roll No")
    if st.button("Search"):
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM students WHERE name LIKE ? OR roll_no LIKE ?", conn, params=(f"%{name}%", f"%{name}%"))
        conn.close()
        if len(df) == 0:
            st.warning("No student found")
        else:
            st.dataframe(df, use_container_width=True)