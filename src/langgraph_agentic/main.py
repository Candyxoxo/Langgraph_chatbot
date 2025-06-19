import streamlit as st                 
from src.langgraph_agentic.UI.streamlitui.loadui import LoadStreamlitUi
from src.langgraph_agentic.LLMS.groqllm import GroqLLM
from src.langgraph_agentic.Graph.graph_builder import GraphBuilder
from src.langgraph_agentic.UI.streamlitui.display_result import DisplayResultStreamlit

def load_langgraph_agenticai_app():
    """
    Loads and runs the the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displayes the output while
    implementing exception handling for robustness.
    """
    
    # Load UI
    ui = LoadStreamlitUi()
    user_input = ui.load_streamlit_ui()
    
    if not user_input:
        st.error("Error: Failed to load user input from the UI")
        return 
    user_msg = st.chat_input("Enter your message: ")
    
    # As soon as you get user message, implement the workflow
    if user_msg:
        try:
            # Config LLM
            llm_obj = GroqLLM(user_controls_input=user_input)
            model = llm_obj.get_llm_model()
        
            if not model:
                st.error("Error: LLM model could not be initialized")
                return 
        
            # # Initialize and set up the graph based on use case
            usecase = user_input.get("selected_usecase")
        
            if not usecase:
                st.error("Error: No use case selected.")
                return
        
            # Start building graph
            graph_builder = GraphBuilder(model)
        
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase, graph, user_msg).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: Graph set up failed- {e}")
                return
        except Exception as e:
            st.error(f"Error: Graph set up failed- {e}")
            return  
    else:
        st.info("Please enter a message to proceed.")