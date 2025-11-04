import os
from dotenv import load_dotenv
from services.gspread_service import GoogleSheetsLogger

load_dotenv()

print("=" * 70)
print("🧪 TESTING GOOGLE SHEETS CONNECTION")
print("=" * 70)

# Check environment variables
print("\n📋 Environment Variables:")
print(f"  GOOGLE_CREDENTIALS_FILE: {os.getenv('GOOGLE_CREDENTIALS_FILE')}")
print(f"  GOOGLE_SPREADSHEET_ID: {os.getenv('GOOGLE_SPREADSHEET_ID')}")
print(f"  GOOGLE_SHEET_NAME: {os.getenv('GOOGLE_SHEET_NAME')}")

# Check if credentials file exists
creds_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'google_credentials.json')
if os.path.exists(creds_file):
    print(f"\n✅ Credentials file found: {creds_file}")
    
    # Read service account email
    import json
    with open(creds_file) as f:
        creds = json.load(f)
        print(f"📧 Service Account: {creds.get('client_email')}")
else:
    print(f"\n❌ Credentials file NOT found: {creds_file}")
    print("   Download from: https://console.cloud.google.com/iam-admin/serviceaccounts")

# Initialize Google Sheets
print("\n🔄 Initializing Google Sheets...")
sheets_logger = GoogleSheetsLogger()

if sheets_logger.sheet:
    print("\n✅ SUCCESS! Connected to Google Sheets")
    print(f"📊 Sheet Name: {sheets_logger.sheet_name}")
    print(f"🔗 Spreadsheet URL: {sheets_logger.get_spreadsheet_url()}")
    
    # Try to log test data
    print("\n🧪 Testing data logging...")
    test_data = {
        "call_id": "test-connection-12345",
        "timestamp": "2025-11-04 23:59:59",
        "caller_info": {
            "name": "Test User",
            "phone": "+1234567890",
            "email": "test@example.com",
            "role": "buyer",
            "company": "Test Corp"
        },
        "property_details": {
            "asset_type": "office",
            "location": "New York, NY",
            "deal_size": "$5M",
            "square_footage": "5000 sq ft",
            "urgency": "3 months",
            "additional_details": "Test property details"
        },
        "inquiry_type": "buying",
        "conversation_summary": "This is a test call to verify Google Sheets integration",
        "duration": 120,
        "recording_url": "https://example.com/test.wav"
    }
    
    success = sheets_logger.log_call(test_data)
    
    if success:
        print("\n✅ TEST DATA LOGGED SUCCESSFULLY!")
        print(f"🔗 View here: {sheets_logger.get_spreadsheet_url()}")
    else:
        print("\n❌ Failed to log test data")
else:
    print("\n❌ FAILED to connect to Google Sheets")
    print("\n🔧 Troubleshooting:")
    print("  1. Make sure google_credentials.json exists")
    print("  2. Check GOOGLE_SPREADSHEET_ID in .env")
    print("  3. Verify sheet is shared with service account email")
    print("  4. Check Google Sheets API is enabled")

print("=" * 70)
