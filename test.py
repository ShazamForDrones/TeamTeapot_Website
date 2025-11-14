import os
from dotenv import load_dotenv
load_dotenv()

print("SUPABASE_URL:", repr(os.getenv("SUPABASE_URL")))
