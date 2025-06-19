from langgraph.graph import StateGraph
from langgraph.graph import START,END
from src.langgraph_agentic.Nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraph_agentic.State.state import State

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
        
    def setup_graph(self, usecase: str):
        """ 
        Sets up graph for selected usecase.
        """
            
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        
        return self.graph_builder.compile()
    
                
        