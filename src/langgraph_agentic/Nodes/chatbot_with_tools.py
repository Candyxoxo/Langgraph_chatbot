from src.langgraph_agentic.State.state import State
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatbotWithTools:
    def __init__(self, model):
        self.llm = model
        
    def create_chatbot_with_tools(self, tools, prompt=None):
        """
        Returns a chatbot node function.
        Args:
            tools: List of tools to bind to the LLM.
            prompt: Optional ChatPromptTemplate to guide the LLM.
        """
        # Define a default system prompt if none is provided
        if prompt is None:
            prompt = ChatPromptTemplate.from_messages([
                ("system", """
                You are an intelligent assistant helping a student understand complex topics. Follow these steps:
                1. Analyze the user's query to select the most appropriate tool:
                   - Use 'arxiv_search' for queries about academic papers, research articles, or scientific topics (e.g., "research paper on machine learning").
                   - Use 'wikipedia_search' for queries seeking factual information, definitions, or summaries on general topics (e.g., "definition of quantum mechanics").
                   - Use 'tavily_search' for general web searches, real-time news, or non-academic, non-factual queries (e.g., "latest AI news").
                2. Fetch relevant data using the selected tool.
                3. Present the response in a blog-style format, tailored for a student:
                   - Use a clear, educational tone, as if explaining to a curious high school or college student.
                   - Structure the response like a short blog post with 2-4 sections, each with a header (e.g., "## Topic Name") and a descriptive paragraph (50-100 words).
                   - Cover all key points from the tool output, avoiding raw links or unprocessed text.
                   - For news queries, include insights from multiple sources to provide a broad perspective.
                4. If no tool is needed, generate a direct blog-style response with the same structure and tone.
                5. Ensure the response is concise, engaging, and directly addresses the student's query.
                """),
                MessagesPlaceholder(variable_name="messages"),
            ])

        # Bind tools to the LLM
        llm_with_tools = self.llm.bind_tools(tools)
        
        def chatbot_node(state: State):
            """
            Chatbot logic for processing the input state and returning a response.
            """
            messages = state["messages"]
            logger.info(f"Processing messages: {messages}")
            
            # Format the prompt with the current messages
            prompt_messages = prompt.format_messages(messages=messages)
            
            # Invoke the LLM
            response = llm_with_tools.invoke(prompt_messages)
            logger.info(f"LLM response: {response}")
            
            # If the response contains tool calls, let the graph handle them
            if hasattr(response, "tool_calls") and response.tool_calls:
                logger.info(f"Tool calls detected: {response.tool_calls}")
                return {"messages": [response]}
            else:
                # If a tool was used (ToolMessage in state), format its output as a blog post
                if isinstance(messages[-1], ToolMessage):
                    tool_output = messages[-1].content
                    tool_name = messages[-1].name
                    user_query = messages[0].content if messages and isinstance(messages[0], HumanMessage) else ""
                    logger.info(f"Formatting tool output from {tool_name}: {tool_output}")
                    
                    # Create a blog-style formatting prompt
                    blog_prompt = ChatPromptTemplate.from_messages([
                        ("system", """
                        Format the following tool output as a short blog post for a student audience:
                        - Use a clear, educational tone, as if explaining to a high school or college student.
                        - Structure the response with 2-4 sections, each with a header (e.g., "## Topic Name") and a descriptive paragraph (50-100 words).
                        - Cover all key points relevant to the user's query.
                        - Avoid raw links or unprocessed text.
                        - For news queries, synthesize insights from multiple sources.
                        - For arxiv related queries, synthesize all the key insights from the entire research paper. Imagine you are the author of the paper and now you have to explain what exactly is going on in it.
                        Tool: {tool_name}
                        Tool output: {tool_output}
                        User query: {user_query}
                        """),
                        MessagesPlaceholder(variable_name="messages"),
                    ])
                    blog_messages = blog_prompt.format_messages(
                        tool_name=tool_name,
                        tool_output=tool_output,
                        user_query=user_query,
                        messages=[HumanMessage(content=tool_output)]
                    )
                    blog_response = llm_with_tools.invoke(blog_messages)
                    logger.info(f"Blog-style response: {blog_response}")
                    return {"messages": [blog_response]}
                else:
                    return {"messages": [response]}

        return chatbot_node