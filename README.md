# 🏢 Realflow Voice Agent

An AI-powered inbound call agent for commercial real estate, built with Vapi, Cartesia Sonic 3, and FastAPI.

## ✨ Features

- 🎙️ **Natural Voice**: Cartesia Sonic 3 for human-like conversations
- 📞 **Instant Pickup**: Professional greeting within seconds
- 🏢 **Commercial Focus**: Specialized in office, retail, industrial properties
- 📊 **Smart Data Capture**: Automatically logs caller info and property details
- 🔗 **Dual Logging**: JSON files + Google Sheets integration
- 🎯 **Lead Qualification**: Captures contact info, budget, timeline, and requirements

## 📞 Test the Agent

**Call:** `+1 (313) 306-9118`

Try asking about:
- Office space in Manhattan
- Retail locations for lease
- Industrial warehouse purchases
- Commercial property investments

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites

- Python 3.10+
- Vapi account (sign up at [vapi.ai](https://vapi.ai))
- ngrok account (for webhooks)

### 1. Clone & Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd realflow-voice-agent

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate  # On Windows
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create `.env` file in the project root:

```bash
cp .env.example .env  # If you have an example file
# OR create manually
nano .env
```

Add these variables:

```env
# Vapi Configuration
VAPI_API_KEY=your_vapi_api_key_here
VAPI_PHONE_NUMBER_ID=your_phone_number_id_here
VAPI_ASSISTANT_ID=your_assistant_id_here
WEBHOOK_SECRET=your_secure_webhook_secret

# Brokerage Settings
BROKERAGE_NAME=Premium Brokers Inc.

# Server URLs
BASE_URL=http://localhost:8000
NGROK_URL=https://your-ngrok-url.ngrok-free.app

# Google Sheets (Optional)
GOOGLE_CREDENTIALS_FILE=google_credentials.json
GOOGLE_SPREADSHEET_ID=your_google_sheet_id
GOOGLE_SHEET_NAME=Realflow Call Logs
```

**Get your Vapi credentials:**
1. Go to [dashboard.vapi.ai](https://dashboard.vapi.ai)
2. Copy your API key from Settings
3. Get your phone number ID from Phone Numbers page

### 4. Start ngrok (for webhooks)

```bash
# In a new terminal
ngrok http 8000
```

**Copy the HTTPS URL** (e.g., `https://abc123.ngrok-free.app`) and update `NGROK_URL` in `.env`

### 5. Deploy Vapi Assistant

```bash
# Make sure venv is activated
python deploy_assistant.py
```

This will:
- Create/update your Vapi assistant
- Configure webhook URL
- Save assistant ID to `.env`

### 6. Start the Application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Server running at:** `http://localhost:8000`

### 7. Test the System

**Option 1: Make a real call**
```
Call: +1 (313) 306-9118
```

**Option 2: Test webhook endpoint**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}

curl http://localhost:8000/api/conversations
# Should return: {"conversations":[],"count":0}
```

**Option 3: Test via Vapi Dashboard**
1. Go to [dashboard.vapi.ai/assistants](https://dashboard.vapi.ai/assistants)
2. Find "Realflow Commercial Real Estate Agent"
3. Click "Test Call"
4. Talk with the AI agent

---

## 📊 Google Sheets Integration (Optional)

For automatic call logging to Google Sheets, follow [`BUILD_PROCESS.md`](BUILD_PROCESS.md):

### Quick Setup

1. **Create Google Cloud Project**
   - Go to [console.cloud.google.com](https://console.cloud.google.com)
   - Create project: "Realflow Voice Agent"
   - Enable Google Sheets API & Google Drive API

2. **Create Service Account**
   - Go to "IAM & Admin" → "Service Accounts"
   - Create account: "realflow-logger"
   - Download JSON credentials as `google_credentials.json`

3. **Create Google Sheet**
   - Go to [sheets.google.com](https://sheets.google.com)
   - Create new sheet: "Realflow Call Logs"
   - Copy Sheet ID from URL
   - Share with service account email (from credentials.json)

4. **Update .env**
   ```env
   GOOGLE_SPREADSHEET_ID=your_sheet_id_here
   ```

5. **Test Connection**
   ```bash
   python test_google_sheets.py
   ```

See [`BUILD_PROCESS.md`](BUILD_PROCESS.md) for detailed instructions.

---

## 🗂️ Project Structure

```
realflow-voice-agent/
├── config/
│   └── vapi_assistant.json      # AI assistant configuration
├── data/
│   └── conversations.json       # Call logs (auto-generated)
├── logs/
│   └── app.log                  # Application logs
├── models/
│   └── schemas.py               # Data models
├── routes/
│   └── webhook.py               # Vapi webhook handler
├── services/
│   ├── vapi_service.py          # Vapi API client
│   └── gspread_service.py       # Google Sheets logger
├── utils/
│   └── logger.py                # Logging utilities
├── .env                         # Environment variables (create this)
├── .gitignore                   # Git ignore rules
├── BUILD_PROCESS.md             # Google Sheets setup guide
├── deploy_assistant.py          # Deploy/update assistant
├── main.py                      # FastAPI application
├── README.md                    # This file
└── requirements.txt             # Python dependencies
```

---

## 🔧 API Endpoints

### Public Endpoints

**GET /** - API Information
```bash
curl http://localhost:8000/
```

**GET /health** - Health Check
```bash
curl http://localhost:8000/health
```

**GET /api/conversations** - Get All Logged Calls
```bash
curl http://localhost:8000/api/conversations
```

**GET /api/sheets-url** - Get Google Sheets URL
```bash
curl http://localhost:8000/api/sheets-url
```

### Webhook Endpoint

**POST /api/vapi/webhook** - Vapi Event Handler
- Receives call events from Vapi
- Processes end-of-call reports
- Logs to JSON and Google Sheets

---

## 📋 Conversation Data Structure

Each call is logged with:

```json
{
  "call_id": "019a4d68-81e9-7dd3-8e5f-44c3ddd6311b",
  "timestamp": "2025-11-04T11:18:58",
  "caller_info": {
    "name": "John Smith",
    "phone": "+1234567890",
    "email": "john@example.com",
    "role": "buyer",
    "company": "ABC Corp"
  },
  "property_details": {
    "asset_type": "office",
    "location": "Manhattan, NY",
    "deal_size": "$5-10M",
    "square_footage": "5000 sq ft",
    "urgency": "3-6 months",
    "additional_details": "Looking for Class A space"
  },
  "inquiry_type": "buying",
  "conversation_summary": "Caller seeking office space...",
  "duration": 180,
  "recording_url": "https://storage.vapi.ai/..."
}
```

---

## 🛠️ Development

### Run in Development Mode

```bash
# Terminal 1 - ngrok
ngrok http 8000

# Terminal 2 - FastAPI with auto-reload
uvicorn main:app --reload
```

### Update Assistant Configuration

1. Edit `config/vapi_assistant.json`
2. Run: `python deploy_assistant.py`
3. Restart server

### View Logs

```bash
# Real-time logs
tail -f logs/app.log

# View conversations
cat data/conversations.json | python -m json.tool
```


---

## 🔐 Security

### Important Files (Never Commit!)

- `.env` - Contains API keys
- `google_credentials.json` - Service account credentials
- `data/conversations.json` - Contains PII

These are already in `.gitignore`.

### Enable Webhook Signature Verification

In [`routes/webhook.py`](routes/webhook.py), uncomment:

```python
if x_vapi_signature and not verify_webhook_signature(body, x_vapi_signature):
    raise HTTPException(status_code=401, detail="Invalid signature")
```

---

## 📞 Contact Information

- **Test Phone:** +1 (313) 306-9118
- **Brokerage:** Premium Brokers Inc.
- **Voice Agent:** Realflow Commercial Real Estate Agent

---

## 🐛 Troubleshooting

### "Google Sheets not initialized"

1. Check `GOOGLE_SPREADSHEET_ID` in `.env`
2. Verify `google_credentials.json` exists
3. Ensure sheet is shared with service account email
4. Run: `python test_google_sheets.py`

### "Webhook not receiving calls"

1. Check ngrok is running: `curl https://your-url.ngrok-free.app/health`
2. Verify `NGROK_URL` in `.env` matches ngrok URL
3. Redeploy assistant: `python deploy_assistant.py`
4. Check Vapi dashboard webhook configuration

### "Assistant not answering calls"

1. Verify phone number is linked to assistant in Vapi dashboard
2. Check assistant status at [dashboard.vapi.ai/assistants](https://dashboard.vapi.ai/assistants)
3. Test call from dashboard first

### "401 Unauthorized from Vapi API"

1. Check `VAPI_API_KEY` in `.env`
2. Verify API key at [dashboard.vapi.ai/account](https://dashboard.vapi.ai/account)

---

## 📚 Resources

- [Vapi Documentation](https://docs.vapi.ai)
- [Cartesia Voice](https://cartesia.ai)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Google Sheets API](https://developers.google.com/sheets/api)

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

## 🙏 Credits

Built with:
- **Vapi** - Voice AI infrastructure
- **Cartesia Sonic 3** - Natural voice synthesis
- **OpenAI GPT-4** - Conversational intelligence
- **FastAPI** - Backend framework
- **Google Sheets API** - Data logging

---

## 📞 Quick Reference

### Daily Startup Commands

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Start ngrok (Terminal 1)
ngrok http 8000

# 3. Update NGROK_URL in .env if needed
nano .env

# 4. Start server (Terminal 2)
uvicorn main:app --reload

# 5. Test
curl http://localhost:8000/health
```

### Phone Number

**Call to test:** `+1 (313) 306-9118`

### Dashboard Links

- Vapi: [dashboard.vapi.ai](https://dashboard.vapi.ai)
- Google Sheets: [docs.google.com/spreadsheets/d/1seWV2X1YBszznCzwioR2sxNnxc2Gkt_1lPWHphQ8eM4](https://docs.google.com/spreadsheets/d/1seWV2X1YBszznCzwioR2sxNnxc2Gkt_1lPWHphQ8eM4)

---

**Ready to receive calls!** 🎉

For Google Sheets setup, see [`BUILD_PROCESS.md`](BUILD_PROCESS.md)