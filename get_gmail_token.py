import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

# 1. Simplify to JUST readonly for now
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# 2. Tell the library it's okay if Google tweaks the scope slightly
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

def get_token():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    
    # Run the server
    creds = flow.run_local_server(port=0)
    
    print("\n✅ AUTHORIZATION SUCCESSFUL!")
    print(f"GOOGLE_CLIENT_ID={creds.client_id}")
    print(f"GOOGLE_CLIENT_SECRET={creds.client_secret}")
    print(f"GOOGLE_REFRESH_TOKEN={creds.refresh_token}")

if __name__ == "__main__":
    get_token()