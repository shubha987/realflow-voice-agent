from fastapi import APIRouter, HTTPException, Request, Header
from models.schemas import VapiWebhook, WebhookResponse, ConversationData, CallerInfo, PropertyDetails
from utils.logger import setup_logger, log_conversation
from services.gspread_service import GoogleSheetsLogger
from datetime import datetime
import os
import hmac
import hashlib

router = APIRouter()
logger = setup_logger()
sheets_logger = GoogleSheetsLogger()

def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """Verify Vapi webhook signature"""
    secret = os.getenv("WEBHOOK_SECRET", "").encode()
    expected_signature = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected_signature)

@router.post("/vapi/webhook", response_model=WebhookResponse)
async def handle_vapi_webhook(
    request: Request,
    x_vapi_signature: str = Header(None)
):
    """Handle Vapi webhook events"""
    try:
        body = await request.body()
        
        # Verify signature (optional but recommended)
        # if x_vapi_signature and not verify_webhook_signature(body, x_vapi_signature):
        #     raise HTTPException(status_code=401, detail="Invalid signature")
        if x_vapi_signature and not verify_webhook_signature(body, x_vapi_signature):
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        webhook_data = await request.json()
        message = webhook_data.get("message", {})
        
        logger.info(f"Received webhook: {message.get('type')}")
        
        # Handle different webhook types
        if message.get("type") == "end-of-call-report":
            return await handle_end_of_call(message)
        
        return WebhookResponse(
            status="success",
            message="Webhook received"
        )
    
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def handle_end_of_call(message: dict) -> WebhookResponse:
    """Process end-of-call report"""
    try:
        # Extract conversation data
        call_id = message.get("call", {}).get("id", "")
        transcript = message.get("transcript", "")
        analysis = message.get("analysis", {})
        
        # Parse structured data from analysis
        structured_data = analysis.get("structuredData", {})
        
        caller_info = CallerInfo(
            name=structured_data.get("callerName"),
            phone=structured_data.get("callerPhone"),
            email=structured_data.get("callerEmail"),
            role=structured_data.get("callerRole"),
            company=structured_data.get("company")
        )
        
        property_details = PropertyDetails(
            asset_type=structured_data.get("assetType"),
            location=structured_data.get("location"),
            deal_size=structured_data.get("dealSize"),
            square_footage=structured_data.get("squareFootage"),
            urgency=structured_data.get("urgency"),
            additional_details=structured_data.get("additionalDetails")
        )
        
        conversation_data = ConversationData(
            call_id=call_id,
            timestamp=datetime.now(),
            caller_info=caller_info,
            property_details=property_details,
            inquiry_type=structured_data.get("inquiryType"),
            conversation_summary=analysis.get("summary"),
            duration=message.get("call", {}).get("duration"),
            recording_url=message.get("recordingUrl")
        )
        
        # Convert to dict for logging
        conversation_dict = conversation_data.model_dump()
        
        # Log to JSON file
        log_conversation(conversation_dict)
        
        # Log to Google Sheets
        sheets_logger.log_call(conversation_dict)
        # Log to JSON file
        log_conversation(conversation_data.model_dump())
        
        logger.info(f"Call {call_id} processed successfully")
        logger.info(f"Caller: {caller_info.name} ({caller_info.email})")
        logger.info(f"Property: {property_details.asset_type} in {property_details.location}")
        
        return WebhookResponse(
            status="success",
            message="Call data processed and stored",
            call_id=call_id
        )
    
    except Exception as e:
        logger.error(f"Error processing call: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations")
async def get_conversations():
    """Retrieve all logged conversations"""
    try:
        import json
        with open("data/conversations.json", 'r') as f:
            conversations = json.load(f)
        return {"conversations": conversations, "count": len(conversations)}
    except FileNotFoundError:
        return {"conversations": [], "count": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sheets-url")
async def get_sheets_url():
    """Get Google Sheets URL"""
    url = sheets_logger.get_spreadsheet_url()
    if url:
        return {"url": url, "status": "connected"}
    return {"url": None, "status": "not_configured"}
