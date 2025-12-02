import requests
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
BUSINESS_ACCOUNT_ID = "1387379489656390"  # From your previous response

url = f"https://graph.facebook.com/v18.0/{BUSINESS_ACCOUNT_ID}/phone_numbers"
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")
print(f"\nResponse: {response.json()}")

# Extract phone number IDs
if response.status_code == 200:
    data = response.json().get('data', [])
    if data:
        print("\n" + "="*50)
        print("PHONE NUMBERS FOUND:")
        print("="*50)
        for phone in data:
            print(f"\nDisplay Phone: {phone.get('display_phone_number')}")
            print(f"Phone Number ID: {phone.get('id')}")  # ← USE THIS IN .ENV
            print(f"Verified Name: {phone.get('verified_name')}")
            print(f"Quality Rating: {phone.get('quality_rating')}")
    else:
        print("\nNo phone numbers found!")