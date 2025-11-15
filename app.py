from flask import Flask, render_template, request, redirect, url_for, session
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import folium
import json

app = Flask(__name__)
app.secret_key = "f957bd8188ffe4a4e010e9d2b1ba2dfc7f74d4c1e6fc4d839ce3dfe0a9f9977b"

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def getusr(userid):
    profile_response = supabase.table("Profiles").select("username").eq("id", userid).single().execute()
    print(profile_response)
    profile_data = profile_response.data
    print(profile_data)
    session["username"] = profile_data.get("username") if profile_data else None
def mapxy():
    if session["user"]:
        userid = session["Userid"]
        retourcoords = supabase.table("Devices").select("coords").eq("owner_id", userid).execute()
        if retourcoords.data is not None:
            data = retourcoords.data
        else:
            return
        xy = data[0]
        print(xy)
        coords = xy["coords"]
        m = folium.Map(location=(coords["y"], coords["x"]))
        return m
    else:
        print("no user")
def createalldevics():
    if not session.get("user"):
        print("no user")
        return

    userid = session.get("Userid")
    if not userid:
        print("Userid missing in session")
        return
    userid = session["Userid"]
    data = supabase.table("Devices").select("*").eq("owner_id", userid).execute()
    dataa = data.data
    return dataa

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print("try signup")
        try:
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            result = supabase.auth.sign_up({"email": email, "password": password,"options": {"data": {"username": username}}})
            userid = result.user.id
            supabase.table("Profiles").insert({"id": userid,"username": username}).execute()
            print(supabase.table("Profiles").select("*"))
            if result.user:
                print("Passed -> signup")
                session["user"] = result.user.email
                session["Userid"] = userid
                getusr(userid)

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
                session["Userid"] = result.user.id
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
            getusr(retour.user.id)
            session["user"] = retour.user.email
            session["Userid"] = retour.user.id
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
    session.pop("access_token", None)
    session.pop("username", None)
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

@app.route("/dashboard")
def dashboard():
    datadevices = createalldevics()
    if session.get("user"):
        m = mapxy()
        if m is not None:
            m.get_root().width = "800px"
            m.get_root().height = "600px"
            map = m.get_root()._repr_html_()
            return render_template("dashboard.html",map=map,devices=datadevices)
        return render_template("dashboard.html",map=None,devices=None)
    else:
        return redirect(url_for("index"))

@app.route("/map")
def mapps():
    mapxy()
    return render_template("map.html")


if __name__ == '__main__':
    app.run( port=80,debug=True)
