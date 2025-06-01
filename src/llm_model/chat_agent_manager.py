from typing import Dict
import asyncio
from datetime import datetime, timedelta
from langchain_google_genai import ChatGoogleGenerativeAI
from src.llm_model.langchain_agent import LangChainAgent
from src.infrastructure.config import Config

class ChatAgentManager:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=Config.GEMINI_API_KEY,
            temperature=0.1
        )
        self.user_agents: Dict[str, LangChainAgent] = {}
        self.last_activity: Dict[str, datetime] = {}
        self.cleanup_task = None
        
    def get_agent_for_user(self, user_id: str) -> LangChainAgent:
        """Get or create an agent instance for a specific user"""
        if user_id not in self.user_agents:
            self.user_agents[user_id] = LangChainAgent(llm=self.llm)
        
        self.last_activity[user_id] = datetime.now()
        return self.user_agents[user_id]
    
    async def process_query(self, user_id: str, query: str) -> str:
        """Process query for a specific user"""
        agent = self.get_agent_for_user(user_id)
        return await agent.process_query(query)
    
    def cleanup_inactive_agents(self, inactive_hours: int = 1):
        """Remove agents that haven't been used recently"""
        cutoff_time = datetime.now() - timedelta(hours=inactive_hours)
        inactive_users = [
            user_id for user_id, last_time in self.last_activity.items()
            if last_time < cutoff_time
        ]
        
        for user_id in inactive_users:
            if user_id in self.user_agents:
                del self.user_agents[user_id]
            if user_id in self.last_activity:
                del self.last_activity[user_id]
        
        print(f"Cleaned up {len(inactive_users)} inactive agents")
    
    async def start_cleanup_task(self):
        """Start background task to cleanup inactive agents"""
        while True:
            await asyncio.sleep(3600)  # Run every hour
            self.cleanup_inactive_agents()
