from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper

def get_tools():
    """
    Return the list of tools to be used in the chatbot
    """
    wiki_wrapper = WikipediaAPIWrapper(top_k_results=1)
    arxiv_wrapper = ArxivAPIWrapper(top_k_results=1)
    
    tavily_tool = TavilySearchResults(
        max_results=2,
        name="tavily_search",
        description="Use this for general web searches, real-time news, or non-academic, non-factual queries (e.g., current events, trends, or broad topics)."
    )
    wikipedia_tool = WikipediaQueryRun(
        api_wrapper=wiki_wrapper,
        name="wikipedia_search",
        description="Use this for factual information, definitions, or summaries on a wide range of topics (e.g., historical events, biographies, general knowledge)."
    )
    arxiv_tool = ArxivQueryRun(
        api_wrapper=arxiv_wrapper,
        name="arxiv_search",
        description="Use this for academic papers, research articles, or scientific/technical queries (e.g., machine learning, physics, or specific research topics)."
    )
    tools=[
        tavily_tool,
        wikipedia_tool,
        arxiv_tool
        ]
    return tools

def create_tool_node(tools):
    """ 
    Creates and returns a tool node for the graph
    """
    
    return ToolNode(tools)