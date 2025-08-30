from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from ResearchResponse import ResearchResponse  
from langchain.agents import create_tool_calling_agent,AgentExecutor



load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp") #The only free model with limited requests per month 
llm2 = ChatOpenAI (model="gpt-5")
llm3 = ChatAnthropic(model ="claude-3-5-sonnet-2024022")


parser = PydanticOutputParser(pydantic_object = ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a solution used in financial problems 
            and how to solve it with all possible cases the user will have from the worst
            to the average to the best case.You should use a finance techniques not random techniques
            and make for each poblem unique solution that fits this problem don't generalize a solution for all problems.
            Answer the user query and use neccessary tools. 
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query} {name}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

agent = create_tool_calling_agent (llm=llm, prompt= prompt, tools=[])

agentExecutor = AgentExecutor(agent=agent, tools=[], verbose=True) 
#If you want to skip the process of the agent's thought process you can make'verbose= "false"'

rawResponse = agentExecutor.invoke({"query": "How I should do to buy lamborgini avendator in egypt and my salary is 3500 egyptian pound ?", "name":"Tarek"})
print(rawResponse)

structuredResponse = parser.paarse(rawResponse.get("output")[0]["text"])
print(structuredResponse)