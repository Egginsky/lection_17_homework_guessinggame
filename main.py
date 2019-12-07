import random
from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User, db

app = Flask(__name__)
db.create_all()

@app.route("/", methods=["GET"])
def index():
    email_address = request.cookies.get("email")

    if email_address:
        user = db.query(User).filter_by(email=email_address).first()
    else:
        user = None
    return render_template("index.html", user=user)

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")

    secret_number = random.randint(1, 10)
    user = db.query(User).filter_by(email=email).first()

    if not user:
        user = User(name=name, email=email, secret_number=secret_number)
        db.add(user)
        db.commit()

    response = make_response(redirect(url_for("index")))
    response.set_cookie("email", email)

    return response


@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))
    email_address = request.cookies.get("email")

    user = db.query(User).filter_by(email=email_address).first()

    if guess == user.secret_number:
        message = "Richtig! Die geheime Zahl ist {0}".format(str(guess))
        new_secret = random.randint (1, 10)
        user.secret_number = new_secret

        db.add(user)
        db.commit()

    elif guess > user.secret_number:
        message = "Leider nicht, versuche eine kleinere Zahl"
    elif guess < user.secret_number:
        message = "Leider nicht, versuche eine größere Zahl"

    return render_template("result.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
