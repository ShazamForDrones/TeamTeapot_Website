from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import folium
from datetime import datetime
import secrets
import string

app = Flask(__name__)
app.secret_key = "f957bd8188ffe4a4e010e9d2b1ba2dfc7f74d4c1e6fc4d839ce3dfe0a9f9977b"

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

supabase: Client = create_client(url, key)

def generate_device_code():
    """Generate a random 8-character alphanumeric code for devices"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(8))

def getusr(userid):
    try:
        profile_response = supabase.table("profiles").select("username").eq("id", userid).single().execute()
        session["username"] = profile_response.data.get("username") if profile_response.data else None
    except Exception as e:
        print(f"Error fetching user: {e}")

def mapxy():
    if not session.get("user") or not session.get("Userid"):
        return None
    try:
        retourcoords = supabase.table("devices").select("*").eq("owner_id", session["Userid"]).execute()
        if not retourcoords.data:
            return None
        
        devices = retourcoords.data
        if len(devices) > 0:
            first_device = devices[0]
            first_coords = first_device.get("coords")
            if first_coords:
                m = folium.Map(location=(first_coords["y"], first_coords["x"]), zoom_start=13, tiles="CartoDB Dark_Matter")
                
                for device in devices:
                    device_coords = device.get("coords")
                    if device_coords:
                        folium.Marker(
                            location=(device_coords["y"], device_coords["x"]),
                            popup=device.get("device_name", "Device"),
                            tooltip=device.get("device_name", "Device"),
                            icon=folium.Icon(color="green", icon="info-sign")
                        ).add_to(m)
                
                m.get_root().html.add_child(folium.Element('<style>html, body { width: 100%; height: 100%; margin: 0; padding: 0; } .leaflet-container { height: 100vh; width: 100vw; }</style>'))
                return m
        return None
    except Exception as e:
        print(f"Error creating map: {e}")
        return None

def createalldevics():
    if not session.get("user") or not session.get("Userid"):
        return None
    try:
        data = supabase.table("devices").select("*").eq("owner_id", session["Userid"]).execute()
        return data.data
    except Exception as e:
        print(f"Error fetching devices: {e}")
        return None

def authenticate_user(email, password, is_signup=False, username=None):
    try:
        if is_signup:
            # Check if user already exists in auth
            try:
                result = supabase.auth.sign_up({"email": email, "password": password, "options": {"data": {"username": username}}})
                if result.user:
                    # Check if profile exists, if not create it
                    try:
                        existing_profile = supabase.table("profiles").select("id").eq("id", result.user.id).single().execute()
                    except:
                        # Profile doesn't exist, create it
                        supabase.table("profiles").insert({
                            "id": result.user.id,
                            "username": username,
                            "email": email,
                            "role": "user",
                            "is_active": True
                        }).execute()
                    
                    # Create empty analytics summary for new user
                    try:
                        supabase.table("analytics_summary").insert({
                            "owner_id": result.user.id
                        }).execute()
                    except:
                        pass  # Analytics record might already exist
                    
                    # Auto-login the user after signup
                    session["user"] = result.user.email
                    session["Userid"] = result.user.id
                    session["access_token"] = result.session.access_token
                    getusr(result.user.id)
                    
                    return True, "Account created successfully"
                return False, "Failed to create account. Please try again."
            except Exception as signup_error:
                error_msg = str(signup_error)
                if "already registered" in error_msg.lower():
                    return False, "An account with this email already exists"
                elif "user_already_exists" in error_msg.lower():
                    return False, "An account with this email already exists"
                else:
                    print(f"Signup error: {signup_error}")
                    return False, "Registration failed. Please try again."
        else:
            # Sign in: try to authenticate first
            try:
                result = supabase.auth.sign_in_with_password({"email": email, "password": password})
                
                if result.user:
                    session["user"] = result.user.email
                    session["Userid"] = result.user.id
                    session["access_token"] = result.session.access_token
                    getusr(result.user.id)
                    return True, "Login successful"
            except Exception as login_error:
                error_msg = str(login_error)
                print(f"Login error: {error_msg}")
                return False, "Invalid email or password"
        
        return False, "Invalid email or password"
    except Exception as e:
        error_msg = str(e)
        if "Invalid login credentials" in error_msg:
            return False, "Invalid email or password"
        elif "email" in error_msg.lower():
            return False, "Invalid email format"
        else:
            print(f"Authentication error: {e}")
            return False, "Authentication failed. Please try again."

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        
        if username:
            # Signup from homepage
            success, message = authenticate_user(email, password, is_signup=True, username=username)
            if success:
                return redirect(url_for("dashboard"))
            return render_template("index.html", error=message)
        else:
            # Login from homepage (shouldn't happen, but handle it)
            success, message = authenticate_user(email, password)
            if success:
                return redirect(url_for("dashboard"))
            return render_template("index.html", error=message)
    
    return render_template("index.html", error=None)

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect(url_for("index"))
    
    if request.method == "POST":
        success, message = authenticate_user(request.form.get("mail"), request.form.get("pass"))
        if success:
            return redirect(url_for("dashboard"))
        return render_template("login.html", error=message)
    
    return render_template("login.html", error=None)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username", email.split("@")[0])
        
        success, message = authenticate_user(email, password, is_signup=True, username=username)
        if success:
            return redirect(url_for("dashboard"))
        return render_template("signup.html", error=message)
    
    return render_template("signup.html", error=None)

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
    if not session.get("user"):
        return redirect(url_for("index"))
    
    datadevices = createalldevics()
    m = mapxy()
    
    if m:
        m.get_root().width = "100%"
        m.get_root().height = "100%"
        map_html = m.get_root()._repr_html_()
        return render_template("dashboard.html", map=map_html, devices=datadevices)
    
    return render_template("dashboard.html", map=None, devices=datadevices)

@app.route("/api/add-device", methods=["POST"])
def api_add_device():
    if not session.get("user") or not session.get("Userid"):
        return {"error": "Unauthorized"}, 401
    
    try:
        data = request.get_json()
        device_name = data.get("device_name")
        device_type = data.get("device_type", "drone")
        
        if not device_name:
            return {"error": "Device name is required"}, 400
        
        device_code = generate_device_code()
        
        # Insert device into devices table
        device_response = supabase.table("devices").insert({
            "owner_id": session["Userid"],
            "device_name": device_name,
            "device_type": device_type,
            "device_code": device_code,
            "status": "offline",
            "coords": {"x": 0, "y": 0},
            "last_seen": datetime.utcnow().isoformat()
        }).execute()
        
        if device_response.data:
            return {
                "success": True,
                "device": device_response.data[0],
                "device_code": device_code
            }, 201
        
        return {"error": "Failed to create device"}, 500
    except Exception as e:
        print(f"Error adding device: {e}")
        return {"error": str(e)}, 500

@app.route("/api/delete-device/<device_id>", methods=["DELETE"])
def api_delete_device(device_id):
    if not session.get("user") or not session.get("Userid"):
        return {"error": "Unauthorized"}, 401
    
    try:
        # Verify ownership
        device = supabase.table("devices").select("*").eq("id", device_id).eq("owner_id", session["Userid"]).single().execute()
        
        if not device.data:
            return {"error": "Device not found or unauthorized"}, 404
        
        supabase.table("devices").delete().eq("id", device_id).execute()
        
        return {"success": True}, 200
    except Exception as e:
        print(f"Error deleting device: {e}")
        return {"error": str(e)}, 500

@app.route("/api/analytics")
def api_analytics():
    if not session.get("user") or not session.get("Userid"):
        return {"error": "Unauthorized"}, 401
    
    try:
        try:
            analytics_response = supabase.table("analytics_summary").select("*").eq("owner_id", session["Userid"]).execute()
            
            if analytics_response.data and len(analytics_response.data) > 0:
                data = analytics_response.data[0]
                return {
                    "total_devices": data.get("active_devices_count", 0),
                    "active_devices": data.get("active_devices_count", 0),
                    "threats_detected": data.get("total_threats_detected", 0),
                    "system_status": "Healthy",
                    "detection_accuracy": float(data.get("average_detection_accuracy", 99.2)),
                    "false_positive_rate": float(data.get("false_positive_rate", 0.8))
                }, 200
        except Exception as fetch_error:
            print(f"Error fetching analytics: {fetch_error}")
        
        # If no analytics record exists or fetch failed, create one for the user
        try:
            supabase.table("analytics_summary").insert({
                "owner_id": session["Userid"]
            }).execute()
        except Exception as insert_error:
            print(f"Error creating analytics record: {insert_error}")
        
        # Return default values
        return {
            "total_devices": 0,
            "active_devices": 0,
            "threats_detected": 0,
            "system_status": "Healthy",
            "detection_accuracy": 0,
            "false_positive_rate": 0
        }, 200
    except Exception as e:
        print(f"Critical error in analytics endpoint: {e}")
        # Return default values even on error so frontend doesn't break
        return {
            "total_devices": 0,
            "active_devices": 0,
            "threats_detected": 0,
            "system_status": "Healthy",
            "detection_accuracy": 0,
            "false_positive_rate": 0
        }, 200

@app.route("/api/device-status")
def api_device_status():
    if not session.get("user") or not session.get("Userid"):
        return {"error": "Unauthorized"}, 401
    
    try:
        try:
            devices_response = supabase.table("devices").select("*").eq("owner_id", session["Userid"]).execute()
            devices = devices_response.data if devices_response.data else []
        except Exception as fetch_error:
            print(f"Error fetching device status: {fetch_error}")
            devices = []
        
        online_count = sum(1 for d in devices if d.get("status") == "online")
        offline_count = sum(1 for d in devices if d.get("status") == "offline")
        inactive_count = sum(1 for d in devices if d.get("status") == "inactive")
        
        return {
            "connected": online_count,
            "offline": offline_count,
            "pending": inactive_count,
            "total": len(devices)
        }, 200
    except Exception as e:
        print(f"Critical error in device status endpoint: {e}")
        return {
            "connected": 0,
            "offline": 0,
            "pending": 0,
            "total": 0
        }, 200

@app.route("/api/threats")
def api_threats():
    if not session.get("user") or not session.get("Userid"):
        return {"error": "Unauthorized"}, 401
    
    try:
        try:
            threats_response = supabase.table("threats").select("*").eq("owner_id", session["Userid"]).order("created_at", desc=True).limit(10).execute()
            threats = threats_response.data if threats_response.data else []
        except Exception as fetch_error:
            print(f"Error fetching threats: {fetch_error}")
            threats = []
        
        return {
            "threats": threats,
            "total": len(threats)
        }, 200
    except Exception as e:
        print(f"Critical error in threats endpoint: {e}")
        return {
            "threats": [],
            "total": 0
        }, 200

if __name__ == '__main__':
    app.run(port=80, debug=True)