import gspread
from google.oauth2.service_account import Credentials
import os
from datetime import datetime
from typing import Dict, Any

class GoogleSheetsService:
    def __init__(self):
        # Define the scope
        self.scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Path to your service account credentials JSON file
        self.creds_file = os.getenv("GOOGLE_CREDENTIALS_FILE", "google_credentials.json")
        self.spreadsheet_id = os.getenv("GOOGLE_SHEET_ID", "")
        
        self.client = None
        self.sheet = None
        
        if os.path.exists(self.creds_file):
            self.initialize()
    
    def initialize(self):
        """Initialize Google Sheets client"""
        try:
            creds = Credentials.from_service_account_file(
                self.creds_file, 
                scopes=self.scope
            )
            self.client = gspread.authorize(creds)
            
            if self.spreadsheet_id:
                self.sheet = self.client.open_by_key(self.spreadsheet_id).sheet1
            
        except Exception as e:
            print(f" Error initializing Google Sheets: {e}")
    
    def log_call(self, conversation_data: Dict[str, Any]):
        """Log call data to Google Sheet"""
        if not self.sheet:
            print(" Google Sheets not configured, skipping...")
            return
        
        try:
            # Prepare row data
            row = [
                conversation_data.get('timestamp', ''),
                conversation_data.get('call_id', ''),
                conversation_data.get('caller_info', {}).get('name', 'N/A'),
                conversation_data.get('caller_info', {}).get('phone', 'N/A'),
                conversation_data.get('caller_info', {}).get('email', 'N/A'),
                conversation_data.get('caller_info', {}).get('role', 'N/A'),
                conversation_data.get('caller_info', {}).get('company', 'N/A'),
                conversation_data.get('inquiry_type', 'N/A'),
                conversation_data.get('property_details', {}).get('asset_type', 'N/A'),
                conversation_data.get('property_details', {}).get('location', 'N/A'),
                conversation_data.get('property_details', {}).get('deal_size', 'N/A'),
                conversation_data.get('property_details', {}).get('square_footage', 'N/A'),
                conversation_data.get('property_details', {}).get('urgency', 'N/A'),
                conversation_data.get('property_details', {}).get('additional_details', 'N/A'),
                conversation_data.get('conversation_summary', 'N/A'),
                str(conversation_data.get('duration', 0)) + ' seconds',
                conversation_data.get('recording_url', 'N/A')
            ]
            
            # Append to sheet
            self.sheet.append_row(row)
            print(f" Call logged to Google Sheets: {conversation_data.get('call_id')}")
            
        except Exception as e:
            print(f" Error logging to Google Sheets: {e}")

    def create_header_row(self):
        """Create header row in Google Sheet"""
        if not self.sheet:
            return
        
        headers = [
            'Timestamp',
            'Call ID',
            'Caller Name',
            'Phone Number',
            'Email',
            'Role',
            'Company',
            'Inquiry Type',
            'Asset Type',
            'Location',
            'Deal Size',
            'Square Footage',
            'Urgency',
            'Additional Details',
            'Summary',
            'Duration',
            'Recording URL'
        ]
        
        try:
            # Check if first row is empty
            first_row = self.sheet.row_values(1)
            if not first_row:
                self.sheet.insert_row(headers, 1)
                # Format header row
                self.sheet.format('A1:Q1', {
                    "backgroundColor": {"red": 0.2, "green": 0.6, "blue": 0.9},
                    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
                    "horizontalAlignment": "CENTER"
                })
                print(" Header row created in Google Sheet")
        except Exception as e:
            print(f"Error creating header: {e}")