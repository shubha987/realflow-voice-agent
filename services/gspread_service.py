import gspread
from google.oauth2.service_account import Credentials
import os
from datetime import datetime
from typing import Dict, Any

class GoogleSheetsLogger:
    def __init__(self):
        self.credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE", "google_credentials.json")
        self.spreadsheet_id = os.getenv("GOOGLE_SPREADSHEET_ID", "")  
        self.sheet_name = os.getenv("GOOGLE_SHEET_NAME", "Realflow Calls")
        self.client = None
        self.sheet = None
        
        if os.path.exists(self.credentials_file):
            self._initialize()
    
    def _initialize(self):
        """Initialize Google Sheets connection"""
        try:
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            creds = Credentials.from_service_account_file(
                self.credentials_file,
                scopes=scopes
            )
            
            self.client = gspread.authorize(creds)
            
            # Open spreadsheet
            if self.spreadsheet_id:
                spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            else:
                # Create new spreadsheet if ID not provided
                spreadsheet = self.client.create("Realflow Call Logs")
                self.spreadsheet_id = spreadsheet.id
                print(f"📊 Created new spreadsheet: {spreadsheet.url}")
            
            # Get or create worksheet
            try:
                self.sheet = spreadsheet.worksheet(self.sheet_name)
            except gspread.exceptions.WorksheetNotFound:
                self.sheet = spreadsheet.add_worksheet(
                    title=self.sheet_name,
                    rows=100,
                    cols=20
                )
                self._setup_headers()
            
        except Exception as e:
            print(f"Google Sheets initialization error: {str(e)}")
    
    def _setup_headers(self):
        """Setup spreadsheet headers"""
        headers = [
            "Timestamp",
            "Call ID",
            "Caller Name",
            "Phone",
            "Email",
            "Role",
            "Company",
            "Inquiry Type",
            "Asset Type",
            "Location",
            "Deal Size",
            "Square Footage",
            "Urgency",
            "Duration (sec)",
            "Summary",
            "Additional Details",
            "Recording URL",
            "Call Status"
        ]
        self.sheet.update('A1:R1', [headers])
        
        # Format header row
        self.sheet.format('A1:R1', {
            "backgroundColor": {"red": 0.2, "green": 0.6, "blue": 0.9},
            "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
            "horizontalAlignment": "CENTER"
        })
    
    def log_call(self, conversation_data: Dict[str, Any]) -> bool:
        """Log call data to Google Sheets"""
        if not self.sheet:
            print("Google Sheets not initialized")
            return False
        
        try:
            caller_info = conversation_data.get("caller_info", {})
            property_details = conversation_data.get("property_details", {})
            
            row_data = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                conversation_data.get("call_id", ""),
                caller_info.get("name", ""),
                caller_info.get("phone", ""),
                caller_info.get("email", ""),
                caller_info.get("role", ""),
                caller_info.get("company", ""),
                conversation_data.get("inquiry_type", ""),
                property_details.get("asset_type", ""),
                property_details.get("location", ""),
                property_details.get("deal_size", ""),
                property_details.get("square_footage", ""),
                property_details.get("urgency", ""),
                conversation_data.get("duration", 0),
                conversation_data.get("conversation_summary", ""),
                property_details.get("additional_details", ""),
                conversation_data.get("recording_url", ""),
                "Completed"
            ]
            
            self.sheet.append_row(row_data)
            print(f"Logged to Google Sheets: {conversation_data.get('call_id')}")
            return True
            
        except Exception as e:
            print(f"Error logging to Google Sheets: {str(e)}")
            return False
    
    def get_spreadsheet_url(self) -> str:
        """Get the spreadsheet URL"""
        if self.client and self.spreadsheet_id:
            return f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}"
        return ""