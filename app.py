from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)
DB = "students.db"
#creat database if not exit
conn = sqlite3.connect(DB)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    email TEXT NOT NULL UNIQUE,
    course TEXT
)
""")
# Helper function
def get_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template("index.html", students=students)

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        email = request.form["email"]
        course = request.form["course"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, email, course) VALUES (?, ?, ?, ?)",
                       (name, age, email, course))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("add.html")

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_student(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        email = request.form["email"]
        course = request.form["course"]
        cursor.execute("UPDATE students SET name=?, age=?, email=?, course=? WHERE id=?",
                       (name, age, email, course, id))
        conn.commit()
        conn.close()
        return redirect("/")
    conn.close()
    return render_template("update.html", student=student)

@app.route("/delete/<int:id>")
def delete_student(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
