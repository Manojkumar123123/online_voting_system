from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secretkey"

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="manoj@123",
        database="voting_db"
    )

# LOGIN
@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",
                       (username,password))

        user = cursor.fetchone()

        if user:
            session["user"] = username
            return redirect("/vote")
        else:
            return "Invalid Login"

    return render_template("login.html")


# REGISTER
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO users(username,password) VALUES(%s,%s)",
            (username,password)
        )

        db.commit()

        return redirect("/")

    return render_template("register.html")


# VOTING PAGE
@app.route("/vote", methods=["GET","POST"])
def vote():

    db = get_db()
    cursor = db.cursor()

    if request.method == "POST":

        candidate_id = request.form["candidate"]

        cursor.execute(
            "UPDATE candidates SET votes=votes+1 WHERE id=%s",
            (candidate_id,)
        )

        cursor.execute(
            "UPDATE users SET has_voted=TRUE WHERE username=%s",
            (session["user"],)
        )

        db.commit()

        return redirect("/result")

    cursor.execute("SELECT * FROM candidates")
    candidates = cursor.fetchall()

    return render_template("vote.html", candidates=candidates)


# RESULT PAGE
@app.route("/result")
def result():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM candidates")
    results = cursor.fetchall()

    return render_template("result.html", results=results)


app.run(debug=True)