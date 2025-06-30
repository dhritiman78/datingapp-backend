import os
import json
import firebase_admin
from firebase_admin import credentials

# Parse JSON from env var
firebase_creds_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")

if not firebase_creds_json:
    raise Exception("Missing FIREBASE_CREDENTIALS_JSON environment variable")

firebase_creds = json.loads(firebase_creds_json)

# Initialize only once
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred)
