from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import PlainTextResponse
import hmac
import hashlib
from config import settings
from rag_agent import get_agent
from whatsapp_client import get_whatsapp_client

app = FastAPI(
    title="WhatsApp Export Copilot",
    description="RAG-powered WhatsApp bot for MSME export guidance",
    version="1.0.0"
)

def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """Verify webhook signature for security"""
    if not settings.WHATSAPP_APP_SECRET:
        return True
    
    expected_signature = hmac.new(
        settings.WHATSAPP_APP_SECRET.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, f"sha256={expected_signature}")

async def process_message(message_data: dict):
    """Process incoming WhatsApp message"""
    try:
        message = message_data.get("messages", [{}])[0]
        message_id = message.get("id")
        from_number = message.get("from")
        message_type = message.get("type")
        
        if message_type != "text":
            return
        
        message_text = message.get("text", {}).get("body", "")
        if not message_text:
            return
        
        print(f"\n📩 Message from {from_number}: {message_text}")
        
        wa_client = get_whatsapp_client()
        agent = get_agent()
        
        wa_client.mark_as_read(message_id)
        
        print(f"🤖 Processing with Export Copilot...")
        answer = agent.query(message_text, session_id=from_number)
        print(f"✅ Generated answer")
        
        result = wa_client.send_message(from_number, answer)
        
        if "error" in result:
            print(f"❌ Error sending: {result['error']}")
        else:
            print(f"✅ Response sent to {from_number}")
            
    except Exception as e:
        print(f"❌ Error processing message: {e}")

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("\n" + "="*60)
    print("🚀 STARTING WHATSAPP EXPORT COPILOT")
    print("="*60)
    print("\n📚 Initializing Export Copilot Agent...")
    get_agent()
    print("✅ Agent ready!")
    print("\n📱 WhatsApp client ready!")
    print("\n" + "="*60)
    print("✅ SERVER READY - Waiting for messages...")
    print("="*60 + "\n")

@app.get("/")
async def root():
    return {
        "service": "WhatsApp Export Copilot",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/webhook")
async def verify_webhook(request: Request):
    """Webhook verification endpoint for WhatsApp"""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode == "subscribe" and token == settings.WEBHOOK_VERIFY_TOKEN:
        print("✅ Webhook verified successfully!")
        return PlainTextResponse(challenge)
    else:
        print("❌ Webhook verification failed!")
        raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    """Main webhook endpoint to receive messages from WhatsApp"""
    signature = request.headers.get("X-Hub-Signature-256", "")
    body = await request.body()
    
    if settings.WHATSAPP_APP_SECRET and not verify_webhook_signature(body, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")
    
    data = await request.json()
    
    if data.get("object") == "whatsapp_business_account":
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                
                if "messages" in value:
                    background_tasks.add_task(process_message, value)
    
    return {"status": "received"}

@app.post("/load-knowledge")
async def load_knowledge():
    """Endpoint to manually load/reload knowledge base"""
    try:
        agent = get_agent()
        agent.load_knowledge_base()
        return {"status": "success", "message": "Knowledge base loaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/test-query")
async def test_query(question: str):
    """Test endpoint to query agent directly"""
    try:
        agent = get_agent()
        answer = agent.query(question)
        return {"question": question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))