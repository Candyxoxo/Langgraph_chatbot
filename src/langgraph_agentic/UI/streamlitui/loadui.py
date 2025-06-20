import streamlit as st               
import os         

from src.langgraph_agentic.UI.uiconfigfile import Config

class LoadStreamlitUi:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}
        
    def load_streamlit_ui(self):
        st.set_page_config(page_title = self.config.get_page_title(), layout = "wide")
        st.header(self.config.get_page_title())
        
        with st.sidebar:
            # get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()
            
            self.user_controls['selected_llm'] = st.selectbox("select LLM", llm_options)
            
            if self.user_controls['selected_llm'] == 'Groq':
            # model selection
                model_options  = self.config.get_groq_model_options()
                self.user_controls['selected_model'] = st.selectbox("Select Model", model_options)
                self.user_controls['GROQ_API_KEY'] = st.session_state['GROQ_API_KEY'] = st.text_input("Api Key", type="password")
            
            # validate api key
                if not self.user_controls['GROQ_API_KEY']:
                    st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")
                
            ## USecase selection
                self.user_controls["selected_usecase"] = st.selectbox("Select Usecases", usecase_options)
                if self.user_controls["selected_usecase"] == "Chatbot With Tools":
                    self.user_controls['TAVILY_API_KEY'] = st.text_input("Tavily Api Key", type="password")
                    # Validate api key
                    if not self.user_controls['TAVILY_API_KEY']:
                        st.warning("⚠️ Please enter your TAVILY_API_KEY key to proceed. Don't have? refer : https://app.tavily.com/home")
                    else:
                        # Set Tavily API key as environment variable
                        os.environ['TAVILY_API_KEY'] = self.user_controls['TAVILY_API_KEY']
        return self.user_controls