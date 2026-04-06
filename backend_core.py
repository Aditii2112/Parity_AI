import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

load_dotenv()

class MCPBackend:
    def __init__(self):
        self.agent = None
        self.client = None

    async def initialize(self):
        configs = {
            "slack": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-slack@latest"],
                "transport": "stdio",
                "env": {
                    "SLACK_BOT_TOKEN": os.getenv("SLACK_BOT_TOKEN"),
                    "SLACK_TEAM_ID": os.getenv("SLACK_TEAM_ID"),
                }
            },
            "gmail": {
                "command": "npx",
                "args": ["-y", "mcp-server-google-workspace"],
                "transport": "stdio",
                "env": {
                    "GOOGLE_CLIENT_ID": os.getenv("GOOGLE_CLIENT_ID"),
                    "GOOGLE_CLIENT_SECRET": os.getenv("GOOGLE_CLIENT_SECRET"),
                    "GOOGLE_REFRESH_TOKEN": os.getenv("GOOGLE_REFRESH_TOKEN"),
                    "PATH": os.getenv("PATH") 
                }
            }
        }

        # Stability: 1.5-flash is the most resilient to versioning quirks
        model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)

        print("🚀 Connecting to MCP Servers...")
        self.client = MultiServerMCPClient(configs)
        tools = await self.client.get_tools()
        print(f"✅ Discovered {len(tools)} tools.")

        # Reverted to the simple version that worked
        self.agent = create_react_agent(model, tools)
        return self.agent

    async def query(self, user_input: str):
        # We use a "Command-Style" prompt which works better for Lite models
        refined_query = f"""
        TASK: {user_input}
        
        STRICT OPERATING PROCEDURES:
        1. DO NOT ask for clarification or more information. 
        2. ASSUME the name provided is the primary search keyword.
        3. EXECUTE 'gmail_search_messages' immediately using the name.
        4. EXECUTE 'slack_search_messages' immediately using the name.
        5. If you find multiple 'Ronits', summarize findings for the most recent one.
        6. If tools return no results, only then state you found nothing.
        """
        
        inputs = {"messages": [("human", refined_query)]}
        result = await self.agent.ainvoke(inputs)
        
        # Handle response formatting
        final_msg = result["messages"][-1]
        if isinstance(final_msg.content, list):
            return final_msg.content[0].get("text", str(final_msg.content))
        return final_msg.content