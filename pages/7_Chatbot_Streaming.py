import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
#from langchain_community.llms import OpenAI
#from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


#load_dotenv()
st.title("🦜🔗 Langchain Chatbot with Streaming")

# Creates a Streamlit sidebar where the user can input their OpenAI API key securely using a password input field.
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

# # app config
# st.set_page_config(page_title="Streamlit Chatbot", page_icon="🤖")
# st.title("Chatbot")

"""
- Defines a function  get_response  that takes a user query and chat history as input. 
- It creates a chat prompt template and initializes the Langchain OpenAI chatbot with specified parameters. 
- It creates a chat chain with the prompt, OpenAI model, and output parser, and streams the conversation history and user query to get a response.
"""
def get_response(user_query, chat_history):

    template = """
    You are a helpful assistant. Answer the following questions considering the history of the conversation:

    Chat history: {chat_history}

    User question: {user_question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)
        
    chain = prompt | llm | StrOutputParser()
    
    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    })

# Initializes the chat history in the Streamlit session state if it doesn't exist already. 
# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a bot. How can I help you?"),
    ]

# Displays the conversation history in the Streamlit chat interface, showing messages from the AI and the user.     
# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

"""
- Allows the user to input messages in the chat interface using  st.chat_input . 
- If the user submits a message, it appends the message to the chat history and displays it in the chat interface. 
- Calls the  get_response  function to get the AI's response based on the user query and chat history. 
- Appends the AI's response to the chat history and displays it in the chat interface. 
"""
# user input
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = st.write_stream(get_response(user_query, st.session_state.chat_history))

    st.session_state.chat_history.append(AIMessage(content=response))
