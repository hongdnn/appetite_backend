from typing import Optional
from langchain.agents import create_react_agent, AgentExecutor
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import PromptTemplate
from src.llm_model.llm_tools import get_tools

class LangChainAgent:

    def __init__(self, llm: object):
        self.llm = llm
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=10  # Keep last 10 exchanges
        )
        self._setup_agent()

    def _setup_agent(self):
        # Bind tools to the instance
        tools = get_tools()

        # Use ReAct prompt template for Gemini
        prompt = PromptTemplate.from_template("""You are a helpful food assistant. You can help users search for foods 
and get detailed information about specific food items. Always be friendly and helpful.

When users ask about finding foods, use the search_food tool.
When users want details about a specific food, use the get_food_detail tool with the food ID.
If the user asks unrelated questions, politely decline to answer and suggest they ask about food-related topics.

If you need a food ID and the user doesn't provide one, first search for the food to get its ID.

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}""")

        agent = create_react_agent(self.llm, tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=self.memory,
            verbose=True,
            max_iterations=3,
            handle_parsing_errors=True  # Important for Gemini
        )
        
    async def process_query(self, user_message: str) -> str:
        """Process user message and return response"""
        try:
            response = await self.agent_executor.ainvoke({"input": user_message})
            return response["output"]
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
     
