import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    
    # Database
    DATABASE_URL: str = "postgresql+psycopg2://whstapp_rag_user:bqXZiVAQcIg54hjvmk18tGVrUd3JqjKN@dpg-d4ndvivgi27c738hj86g-a/whstapp_rag"  
    # WhatsApp Business API
    WHATSAPP_ACCESS_TOKEN: str = os.getenv("WHATSAPP_ACCESS_TOKEN")
    WHATSAPP_PHONE_NUMBER_ID: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    WHATSAPP_API_VERSION: str = os.getenv("WHATSAPP_API_VERSION", "v18.0")
    
    # Webhook
    WEBHOOK_VERIFY_TOKEN: str = os.getenv("WEBHOOK_VERIFY_TOKEN", "your_verify_token")
    WHATSAPP_APP_SECRET: str = os.getenv("WHATSAPP_APP_SECRET", "")
    
    # App settings
    PDF_PATH: str = os.getenv("PDF_PATH", "data/MSME EXPORT COPILOT KNOWLEDGE BASE.pdf")
    TABLE_NAME: str = os.getenv("TABLE_NAME", "MSME_INFO")
    TARGET_GROUP_NAME: str = os.getenv("TARGET_GROUP_NAME", "doc group")


settings = Settings()
