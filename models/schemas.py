from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

class CallerInfo(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    company: Optional[str] = None

class PropertyDetails(BaseModel):
    asset_type: Optional[str] = None
    location: Optional[str] = None
    deal_size: Optional[str] = None
    square_footage: Optional[str] = None
    urgency: Optional[str] = None
    additional_details: Optional[str] = None

class ConversationData(BaseModel):
    call_id: str
    timestamp: datetime
    caller_info: CallerInfo
    property_details: PropertyDetails
    inquiry_type: Optional[str] = None
    conversation_summary: Optional[str] = None
    duration: Optional[int] = None
    recording_url: Optional[str] = None

class VapiWebhook(BaseModel):
    message: Dict[str, Any]
    
class WebhookResponse(BaseModel):
    status: str
    message: str
    call_id: Optional[str] = None