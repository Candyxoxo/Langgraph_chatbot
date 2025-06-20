from langgraph.graph import StateGraph
from langgraph.graph import START,END
from src.langgraph_agentic.Nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraph_agentic.Nodes.chatbot_with_tools import ChatbotWithTools
from src.langgraph_agentic.Tools.tool import get_tools, create_tool_node
from src.langgraph_agentic.State.state import State
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Literal

class GraphBuilder:
    def __init__(self, model):
        self.llm = model 
        self.graph_builder = StateGraph(State)
        
    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the `BasicChatbotNode` class
        and initializes it into the graph. The chatbot node is set as both entry and exit 
        point of the graph.
        """
        
        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)
        
    def basic_chatbot_with_tools_build_graph(self):
        """ 
        Builds an advanced chatbot graph with tools integration.
        This method creates a chatbot graph that includes both a chatbot node
        and a tool node. It defines tools, initializes chatbot with tool capabilities,
        and sets up conditional and direct edges between nodes.
        The chatbot node is set as entry point.
        """
        
        # Define tool node
        tools = get_tools()
        tool_node=  create_tool_node(tools)
        
        ## Define the LLM
        llm=self.llm

        ## Define the chatbot node
        chatbot_with_tool_node_obj = ChatbotWithTools(llm)
        chatbot_with_tool = chatbot_with_tool_node_obj.create_chatbot_with_tools(tools)
        
        ## Add nodes
        self.graph_builder.add_node("chatbot_with_tool", chatbot_with_tool)
        self.graph_builder.add_node("tools", tool_node)
        
         # Define conditional and direct edges
        self.graph_builder.add_edge(START,"chatbot_with_tool")
        self.graph_builder.add_conditional_edges(
            "chatbot_with_tool",
            tools_condition,
            )
        self.graph_builder.add_edge("tools","chatbot_with_tool")
        
    def setup_graph(self, usecase: str):
        """ 
        Sets up graph for selected usecase.
        """
            
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        if usecase == "Chatbot With Tools":
            self.basic_chatbot_with_tools_build_graph()

        
        return self.graph_builder.compile()
    
                
        