import requests
from config import settings

class WhatsAppClient:
    def __init__(self):
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.api_version = settings.WHATSAPP_API_VERSION
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}"
    
    def send_message(self, to: str, message: str) -> dict:
        """Send a text message via WhatsApp Business API"""
        url = f"{self.base_url}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # Split long messages (WhatsApp has 4096 char limit)
        max_length = 4000
        if len(message) > max_length:
            message = message[:max_length] + "...\n\n(Message truncated due to length)"
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
            }
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error sending message: {e}")
            return {"error": str(e)}
    
    def mark_as_read(self, message_id: str) -> dict:
        """Mark a message as read"""
        url = f"{self.base_url}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def send_reaction(self, message_id: str, emoji: str = "👍") -> dict:
        """React to a message"""
        url = f"{self.base_url}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": message_id,
            "type": "reaction",
            "reaction": {
                "message_id": message_id,
                "emoji": emoji
            }
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
        except:
            return {}

# Singleton instance
_whatsapp_client = None

def get_whatsapp_client() -> WhatsAppClient:
    """Get or create WhatsApp client instance"""
    global _whatsapp_client
    if _whatsapp_client is None:
        _whatsapp_client = WhatsAppClient()
    return _whatsapp_client