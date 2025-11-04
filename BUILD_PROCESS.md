# Google Sheets Setup Guide

## Step 1: Create Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Click "Create Project"
3. Name it "Realflow Voice Agent"
4. Click "Create"

## Step 2: Enable Google Sheets API

1. In the project dashboard, go to "APIs & Services" > "Library"
2. Search for "Google Sheets API"
3. Click on it and click "Enable"
4. Also enable "Google Drive API"

## Step 3: Create Service Account

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Name: "realflow-logger"
4. Click "Create and Continue"
5. Skip optional steps, click "Done"

## Step 4: Download Credentials

1. Click on the service account you just created
2. Go to "Keys" tab
3. Click "Add Key" > "Create New Key"
4. Choose "JSON"
5. Download the file
6. Rename it to `google_credentials.json`
7. Move it to your project root: `/home/killdollar/realflow-voice-agent/`

## Step 5: Create Google Sheet

1. Go to https://sheets.google.com
2. Create a new spreadsheet
3. Name it "Realflow Call Logs"
4. Copy the Spreadsheet ID from the URL:
   `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit`
5. Add the ID to your `.env` file:
   `GOOGLE_SPREADSHEET_ID=your_spreadsheet_id_here`

## Step 6: Share Sheet with Service Account

1. Open your Google Sheet
2. Click "Share"
3. Paste the service account email from the JSON file
   (looks like: realflow-logger@project-name.iam.gserviceaccount.com)
4. Give it "Editor" permission
5. Click "Send"

## Done!

Your system will now automatically log all calls to Google Sheets.