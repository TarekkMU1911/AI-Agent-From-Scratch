import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from ResearchResponse import ResearchResponse  
from langchain.agents import create_tool_calling_agent,AgentExecutor
from tools import searchTool,wikiTool,saveTool
import json



load_dotenv()
with open(os.path.join(os.path.dirname(__file__), "messages.json"), "r", encoding="utf-8") as f:
    messages = json.load(f)
    
    
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp") #The only free model with limited requests per month 
llm2 = ChatOpenAI (model="gpt-5")
llm3 = ChatAnthropic(model ="claude-3-5-sonnet-2024022")


parser = PydanticOutputParser(pydantic_object = ResearchResponse)
SYSTEM_PROMPT = messages.get("SYSTEM_PROMPT")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            SYSTEM_PROMPT,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())


tools = [searchTool, wikiTool, saveTool]
agent = create_tool_calling_agent (llm=llm, prompt= prompt, tools=tools)

agentExecutor = AgentExecutor(agent=agent, tools=[], verbose=True) 
#If you want to skip the process of the agent's thought process you can make'verbose= "False"'


INPUT_MESSAGE = messages.get("INPUT_MESSAGE")
QUERY = input (INPUT_MESSAGE)
rawResponse = agentExecutor.invoke({"query": QUERY })


try :
    structuredResponse = parser.parse(rawResponse["output"])
    print(structuredResponse)
    
except Exception as exception :
    ERROR = messages.get("ERROR")
    RAW = messages.get("RAW")
    print(ERROR,exception, RAW, rawResponse )