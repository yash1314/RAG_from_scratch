import streamlit as st
import re, random, time
from src.data_components.data_ingestion import DataFile
from src.model_components.models import Model
from better_profanity import profanity



# streaming output
def output_stream(output):
    try: 
        for word in output.split(" "):
            yield word + " "
            time.sleep(0.03)
            
    except Exception as e:
            print(f"Error in output_stream: {str(e)}")  


# generate casual response when app initialize without file
def casual_responses(sentence):
    """The function generates responses based on the prompt sentiment and wording."""

    if profanity.contains_profanity(sentence): 
        response = random.choice(
        ["Sorry, I cannot help you with that!",
         "I'm here to assist you. If you have any concerns or issues, please let me know, and I'll do my best to address them.",
         "I cannot help you with that. Please, Let me know how I can assist."])
        
        for word in response.split():
            yield word + " "
            time.sleep(0.03)
    else:
        qa_model = Model.QA_model(u_input = sentence)
        for word in qa_model.split():
            yield word + " "
            time.sleep(0.04)


# initialize chat history in streamlit
def initialize_messages():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# function to delete files
def delete_files():
    try:
        DataFile.remove_file(folder_name='artifact')
        
    except Exception as e:
        print(f"Error in artifact folder deletion: {str(e)}")


# regular expression function
def reg_x(text):
    pattern = r"\n|--|#|\||`|\*\*(?=\w+)|(?<=\w)+\*\*|\s{2,}|\.+"
    return re.sub(pattern, "", text)      

# deleting embedded data when user file changes
def clear_cache_session_data(keys):
    st.session_state.pop(keys)
