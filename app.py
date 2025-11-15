from flask import Flask, render_template, request, redirect, url_for, session
import os
from supabase import create_client, Client
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = "f957bd8188ffe4a4e010e9d2b1ba2dfc7f74d4c1e6fc4d839ce3dfe0a9f9977b"

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print("try signup")
        try:
            email = request.form["email"]
            password = request.form["password"]
            result = supabase.auth.sign_up({"email": email, "password": password})
            if result.user:
                print("Passed -> signup")
                session["user"] = result.user.email
                session["access_token"] = result.session.access_token
                return redirect(url_for("index"))
        except Exception as e:
            print("error:", e)
        print("try signin")
        try:
            email = request.form["email"]
            password = request.form["password"]
            result = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if result.user:
                print("Passed -> signin")
                session["user"] = result.user.email
                session["access_token"] = result.session.access_token
                return redirect(url_for("index"))
        except Exception as e:
            print("error:", e)
        return render_template("index.html")
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        mail = data.get("mail")
        password = data.get("pass")
        try:
            retour = supabase.auth.sign_in_with_password(
                {"email": mail, "password": password}
            )
            session["user"] = retour.user.email
            session["access_token"] = retour.session.access_token  # IMPORTANT
            return redirect(url_for("index"))
        except Exception as e:
            print("error:", e)
            return render_template("login.html", error=True)
    if "user" in session:
        print("déjà conn")
        print(session["user"])
        return redirect(url_for("index"))
    else:
        return render_template("login.html", error=False)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            result = supabase.auth.sign_up({"email": email, "password": password})
            if result.user:
                try:
                    result = supabase.auth.sign_in_with_password(
                        {"email": email, "password": password}
                    )
                    session["user"] = result.user.email
                    session["access_token"] = result.session.access_token  # IMPORTANT
                    return redirect(url_for("index"))
                except Exception as e:
                    print("error:", e)
                    return redirect(url_for("login"))
            else:
                return redirect(url_for("register", error="Erreur see logs"))
        return render_template("signup.html", error=None)
    except Exception as e:
        print(e)
        return redirect(url_for("index"))

@app.route('/dev/eric')
def eric():
    return "eric"

@app.route('/dev/julien')
def julien():
    return "julien"

@app.route('/dev/felix')
def felix():
    return "felix"

@app.route('/dev/jeremie')
def jeremie():
    return "jeremie"

@app.route("/dashbaord")
def dashboard():
    return render_template("dashboard.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)