import httpx
import os
from typing import Dict, Any

class VapiService:
    def __init__(self):
        self.api_key = os.getenv("VAPI_API_KEY")
        self.base_url = "https://api.vapi.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def create_assistant(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new Vapi assistant"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/assistant",
                json=config,
                headers=self.headers
            )
            
            # Print response for debugging
            if response.status_code != 200 and response.status_code != 201:
                print(f"\n❌ Response Status: {response.status_code}")
                print(f"❌ Response Body: {response.text}")
            
            response.raise_for_status()
            return response.json()
    
    async def update_assistant(self, assistant_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing assistant"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.patch(
                f"{self.base_url}/assistant/{assistant_id}",
                json=config,
                headers=self.headers
            )
            
            if response.status_code != 200:
                print(f"\n❌ Response Status: {response.status_code}")
                print(f"❌ Response Body: {response.text}")
            
            response.raise_for_status()
            return response.json()
    
    async def get_assistant(self, assistant_id: str) -> Dict[str, Any]:
        """Get assistant details"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.base_url}/assistant/{assistant_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()