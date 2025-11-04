import asyncio
import os
import json
from dotenv import load_dotenv, set_key
from services.vapi_service import VapiService

load_dotenv()

async def deploy_assistant():
    """Deploy or update Vapi assistant"""
    vapi = VapiService()
    
    # Load configuration
    with open("config/vapi_assistant.json", 'r') as f:
        config = json.load(f)
    
    # Replace placeholders
    brokerage_name = os.getenv("BROKERAGE_NAME").strip()
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    ngrok_url = os.getenv("NGROK_URL", "").strip()
    webhook_secret = os.getenv("WEBHOOK_SECRET")
    
    # Use ngrok URL if available, otherwise base URL
    webhook_url = ngrok_url if ngrok_url else base_url
    
    # Replace brokerage name in the config
    config_str = json.dumps(config)
    config_str = config_str.replace("[BROKERAGE_NAME]", brokerage_name)
    config = json.loads(config_str)
    
    # Set webhook configuration
    config["serverUrl"] = f"{webhook_url}/api/vapi/webhook"
    config["serverUrlSecret"] = webhook_secret
    
    # Update first message
    config["firstMessage"] = f"Hello! This is Realflow for {brokerage_name}. How can I help you today?"
    
    print("=" * 60)
    print(" DEPLOYING VAPI ASSISTANT")
    print("=" * 60)
    print(f"\n Configuration:")
    print(f"   Brokerage: {brokerage_name}")
    print(f"   Webhook URL: {config['serverUrl']}")
    print(f"   Voice: Cartesia Sonic")
    print(f"   Model: {config['model']['model']}")
    
    # Save config for debugging
    with open("debug_config.json", 'w') as f:
        json.dump(config, f, indent=2)
    print(f"\n Full config saved to: debug_config.json")
    
    try:
        # Check if assistant already exists
        existing_id = os.getenv("VAPI_ASSISTANT_ID")
        
        if existing_id:
            print(f"\n Updating existing assistant: {existing_id}")
            result = await vapi.update_assistant(existing_id, config)
            print(f" Assistant updated successfully!")
        else:
            print(f"\n✨ Creating new assistant...")
            result = await vapi.create_assistant(config)
            assistant_id = result.get('id')
            
            # Save assistant ID to .env
            set_key(".env", "VAPI_ASSISTANT_ID", assistant_id)

            print(f" Assistant created successfully!")
            print(f" Assistant ID: {assistant_id}")

        print(f"\n📞 Next Steps:")
        print(f"   1. Go to https://dashboard.vapi.ai/phone-numbers")
        print(f"   2. Click on your phone number")
        print(f"   3. Under 'Assistant', select: {result.get('name')}")
        print(f"   4. Save and start receiving calls!")
        print("=" * 60)
        
        return result
    
    except Exception as e:
        print(f"\n Error deploying assistant: {str(e)}")
        
        # Try to get more error details
        if hasattr(e, 'response'):
            try:
                error_detail = e.response.json()
                print(f"\n Error Details:")
                print(json.dumps(error_detail, indent=2))
            except:
                print(f"\n Response Text: {e.response.text if hasattr(e.response, 'text') else 'N/A'}")

        print(f"\nDebug steps:")
        print(f"   1. Check debug_config.json for the full configuration")
        print(f"   2. Verify your API key is correct")
        print(f"   3. Check Vapi docs: https://docs.vapi.ai/api-reference/assistants/create-assistant")
        
        raise

if __name__ == "__main__":
    asyncio.run(deploy_assistant())