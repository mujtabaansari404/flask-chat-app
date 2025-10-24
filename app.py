from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "HKMLOTYVBD1527"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chats_user.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
socketio = SocketIO(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def signup():
    return render_template("signup.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup", methods=["POST"])
def handle_signup():

    full_name = request.form.get("full-name")
    email = request.form.get("email")

    password = request.form.get("password")

    if not full_name or not email or not password:
        return "All fields are required", 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return "User already exists. Please log in.", 400

    new_user = User(full_name=full_name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    print(f"User signed up: {full_name} ({email})")
    return redirect(url_for("login"))


@app.route("/login", methods=["POST"])
def handle_login():
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return "All fields are required", 400
    user = User.query.filter_by(email=email).first()
    if not user or user.password != password:
        return "Invalid email or password", 401

    print(f"User logged in: {user.full_name} ({email})")
    return render_template("index.html")


@socketio.on("message")
def handle_message(msg):
    send(msg, broadcast=True)


@socketio.on("user_joined")
def handle_user_joined(user):
    send(f"{user} joined the chat.", broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True)
