import os
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.knowledge.pdf import PDFKnowledgeBase
from phi.vectordb.pgvector import PgVector, SearchType
from config import settings

class ExportCopilotAgent:
    def __init__(self):
        self.knowledge_base = None
        self.agent = None
        self._initialize()
    
    def _initialize(self):
        """Initialize knowledge base and agent"""
        print("🔧 Initializing Export Copilot Agent...")
        
        # Set OpenAI API key
        os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
        
        # Knowledge base setup
        self.knowledge_base = PDFKnowledgeBase(
            path=settings.PDF_PATH,
            vector_db=PgVector(
                table_name=settings.TABLE_NAME,
                db_url=settings.DATABASE_URL,
                search_type=SearchType.hybrid
            ),
        )
        
        # Create the Export Copilot Agent
        self.agent = Agent(
            name="Export Copilot",
            model=OpenAIChat(id="gpt-4o"),
            knowledge=self.knowledge_base,
            search_knowledge=True,
            read_chat_history=True,
            instructions=[
                "You are an AI Export Advisor helping Indian MSMEs with international trade.",
                "Search your knowledge base for export information, compliance, documentation, and market intelligence.",
                "Provide practical, step-by-step guidance tailored for WhatsApp messages.",
                "Be professional, clear, and helpful.",
                "Keep responses concise but informative for mobile viewing.",
                "Use bullet points sparingly and only when necessary.",
            ],
            show_tool_calls=False,  # Don't show tool calls in WhatsApp
            markdown=False,  # Plain text for WhatsApp
        )
        
        print("✅ Export Copilot Agent initialized!")
    
    def load_knowledge_base(self):
        """Load PDF into knowledge base (run once during setup)"""
        print("📚 Loading knowledge base from PDF...")
        self.knowledge_base.load(upsert=True)
        print("✅ Knowledge base loaded successfully!")
    
    def query(self, question: str, session_id: str = None) -> str:
        """Query the agent with a question"""
        try:
            # Get response from agent
            response = self.agent.run(question, stream=False)
            
            # Extract text from response
            if hasattr(response, 'content'):
                return response.content
            return str(response)
            
        except Exception as e:
            print(f"❌ Error querying agent: {e}")
            return "Sorry, I encountered an error processing your question. Please try again."

# Singleton instance
_agent_instance = None

def get_agent() -> ExportCopilotAgent:
    """Get or create agent instance"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = ExportCopilotAgent()
    return _agent_instance