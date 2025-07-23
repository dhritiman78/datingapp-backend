import os
import json
import firebase_admin
from firebase_admin import credentials

firebase_creds_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")

if not firebase_admin._apps:
    if firebase_creds_json is None:
        raise ValueError("FIREBASE_CREDENTIALS_JSON not set")

    cred_dict = json.loads(firebase_creds_json)

    # 🔧 Fix the private key to have actual newlines
    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")

    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': os.environ["FIREBASE_DB_URL"]
    })
