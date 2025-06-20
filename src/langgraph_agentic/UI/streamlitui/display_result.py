import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json 
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_msg):
        self.usecase = usecase
        self.graph = graph
        self.user_msg = user_msg
        
    def display_result_on_ui(self):
        usecase= self.usecase
        graph = self.graph
        user_message = self.user_msg
        print(user_message)
        
        if usecase == "Basic Chatbot":
            for event in graph.stream({"messages": ("user", user_message)}):
                print(event.values())
                for value in event.values():
                    print(value['messages'])
                    with st.chat_message("user"):
                        st.write(user_message)   
                    with st.chat_message("assistant"):
                        st.write(value["messages"].content)
        
        elif usecase == "Chatbot With Tools":
            # Prepare state and invoke the graph
            initial_state = {"messages": [HumanMessage(content=user_message)]}
            with st.spinner("Fetching and summarizing data..."):
                res = graph.invoke(initial_state)
            
            for msg in res['messages']:
                if isinstance(msg, HumanMessage):
                    with st.chat_message('user'):
                        st.write(msg.content)
                        
                elif isinstance(msg, ToolMessage):
                    # Log tool output for debugging, but don't display
                    logger.info(f"Tool used: {msg.name}, Output: {msg.content}")
                    # Optionally display tool output in an expander for debugging
                    with st.expander(f"Raw Tool Output ({msg.name})"):
                        st.write("Tool Output Start")
                        st.write(msg.content)
                        st.write("Tool Output End")
                        
                elif isinstance(msg, AIMessage) and msg.content:
                    with st.chat_message('assistant'):
                        st.markdown(f"**Response:**")
                        st.write(msg.content)