import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json 

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