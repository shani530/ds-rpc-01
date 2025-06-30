# implement the Agent class
import os


from dotenv import load_dotenv  # Import load_dotenv to load environment variables.

from langchain_groq import ChatGroq # Import ChatOpenAI from langchain_groq for language model interaction. 
from langchain.prompts import ChatPromptTemplate
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages  import AIMessage, HumanMessage



load_dotenv()  # Load environment variables from a .env file.

TavilyApi_Key = os.getenv("TAVILY_API_KEY")
GroqApi_Key = os.getenv("GROQ_API_KEY")

"""
prompt = ChatPromptTemplate.from_messages([
    
"You are a helpful assistant. You will be provided with a question and a list of documents."+
    "Your task is to answer the question based on the provided documents." +
    "If you don't know the answer, just say that you don't know, don't try to make up an answer."
                                          ])
"""
prompt = ChatPromptTemplate.from_messages([
    ( "You are a helpful assistant. You will be provided with a question , you need to answer the" +
     " searching using Tavily Search API and then answer the question." )]
)
tools = [TavilySearch(max_results = 3)]
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=.5, groq_api_key = GroqApi_Key)
# for create_react_agent, we need to pass the model and tools only , no prompt is needed .

agent = create_react_agent(model = llm, tools=tools)

query = "Who won 2011 cricket world cup?"

state={"messages": query}
response=agent.invoke(state)

messages =response.get("messages")
ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
print(ai_messages[-1])
#messages=response.get("messages")
#ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]
#print(ai_messages[-1])

# The above code sets up an agent using LangChain with Tavily for search and OpenAI for language processing.