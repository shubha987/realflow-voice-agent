# Realflow Voice Agent - Inbound Commercial Real Estate AI

A sophisticated AI voice agent powered by Vapi and Cartesia Sonic 3 for handling inbound commercial real estate inquiries.

## Features

- 🎙️ Natural, expressive voice using Cartesia Sonic 3
- 🏢 Commercial real estate qualification
- 📞 Instant call pickup with professional greeting
- 💬 Empathetic, conversational AI
- 📊 Structured data collection
- 🔗 Webhook integration for data logging
- 📝 JSON conversation storage

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file:

```env
VAPI_API_KEY=your_vapi_api_key
VAPI_PHONE_NUMBER_ID=your_phone_number_id
WEBHOOK_SECRET=your_secure_secret
BROKERAGE_NAME=YourBrokerageName
BASE_URL=https://your-domain.com
```

### 3. Deploy Assistant

```bash
python deploy_assistant.py
```

### 4. Run Application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /api/vapi/webhook` - Vapi webhook handler
- `GET /api/conversations` - Retrieve all conversations

## Webhook Payload

The agent sends structured data after each call:

```json
{
  "call_id": "string",
  "timestamp": "2025-11-04T...",
  "caller_info": {
    "name": "John Doe",
    "phone": "+1234567890",
    "email": "john@example.com",
    "role": "buyer",
    "company": "ABC Corp"
  },
  "property_details": {
    "asset_type": "office",
    "location": "Manhattan, NY",
    "deal_size": "$5-10M",
    "urgency": "3-6 months"
  },
  "conversation_summary": "Caller seeking office space...",
  "recording_url": "https://..."
}
```

## Deployment

### Using Ngrok (Development)

```bash
ngrok http 8000
```

Update `BASE_URL` in `.env` with ngrok URL.

### Production Deployment

Deploy to:
- AWS EC2 / ECS
- Google Cloud Run
- Railway
- Render

Ensure:
- SSL/HTTPS enabled
- Webhook signature verification active
- Environment variables secured

## Data Storage

Conversations stored in: `data/conversations.json`

For production, integrate:
- PostgreSQL
- MongoDB
- Airtable
- Google Sheets API

## License

MIT