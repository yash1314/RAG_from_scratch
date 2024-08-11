import streamlit as st
import re, random, time
from src.data_components.data_ingestion import DataFile
from src.model_components.models import Model
from better_profanity import profanity



# streaming output
def output_stream(output):
    """Output answer in stream of words."""
    try: 
        for word in output.split(" "):
            yield word + " "
            time.sleep(0.03)
            
    except Exception as e:
            print(f"Error in output_stream: {str(e)}")  


# generate casual response when app initialize with and without file
def casual_responses(sentence):
    """The function generates responses based on the prompt sentiment and wording. It also restricts user and model response
    if found inappropriate."""

    if profanity.contains_profanity(sentence): 
        filtered_response = random.choice(
        ["Sorry, I cannot help you with that!",
        "I'm here to assist you. If you have any concerns or issues, please let me know, and I'll do my best to address them.",
        "I cannot help you with that. Please, Let me know how I can assist."])
        
        for word in filtered_response.split():
            yield word + " "
            time.sleep(0.05)

    else:
        qa_model_output = Model.QA_model(u_input = sentence)
        if profanity.contains_profanity(qa_model_output):
            filtered_output = "Inappropriate output, therefore restricting the answer. Ask another question !"
            for word in filtered_output.split():
                yield word + " "
                time.sleep(0.05)
        else:
            for word in qa_model_output.split():
                yield word + " "
                time.sleep(0.05)


# initialize chat history in streamlit
def initialize_messages():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# regular expression function
def reg_x(text):
    pattern = r"\n|--|#|\||`|\*\*(?=\w+)|(?<=\w)+\*\*|\s{2,}|\.+"
    return re.sub(pattern, "", text)      


# deleting embedded data when user file changes
def clear_session_embedded_data():
    """Clear document embedding data"""
    if "embedded_data" in st.session_state:
        del st.session_state["embedded_data"]