from services.google_sheet_service import GoogleSheetsService
from dotenv import load_dotenv

load_dotenv()

def main():
    print("=" * 60)
    print("📊 SETTING UP GOOGLE SHEET")
    print("=" * 60)
    
    sheets = GoogleSheetsService()
    
    if not sheets.sheet:
        print("\n❌ Google Sheets not configured!")
        print("Please:")
        print("  1. Add credentials.json to project root")
        print("  2. Set GOOGLE_SHEET_ID in .env")
        print("  3. Share sheet with service account email")
        return
    
    print(f"\n✅ Connected to Google Sheet")
    print(f"📋 Creating header row...")
    
    sheets.create_header_row()
    
    print(f"\n✅ Google Sheet is ready!")
    print(f"🔗 View at: https://docs.google.com/spreadsheets/d/{sheets.spreadsheet_id}")
    print("=" * 60)

if __name__ == "__main__":
    main()