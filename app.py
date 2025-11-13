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

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)