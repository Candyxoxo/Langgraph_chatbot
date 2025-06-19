from src.langgraph_agentic.State.state import State

class BasicChatbotNode:
    """ 
    Basic Chatbot login implementation
    """
    
    def __init__(self, model):
        self.llm = model
        
    def process(self, state: State)->dict:
        """ 
        Processes input state and generates a response
        """
        
        return {"messages": self.llm.invoke(state['messages'])}