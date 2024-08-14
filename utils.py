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
            time.sleep(0.01)
            
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

        for word in filtered_response.split(" "):
                yield word + " "
                time.sleep(0.01)
        
    else:
        qa_model_output = Model.QA_model(u_input = sentence, type = "qa")

        if profanity.contains_profanity(qa_model_output):
            filtered_output = "Inappropriate output, therefore restricting the answer. Ask another question !"
            for word in filtered_output.split(" "):
                yield word + " "
                time.sleep(0.01)

        else:
            for word in qa_model_output.split(" "):
                yield word + " "
                time.sleep(0.01)


# regular expression function
def reg_x(text):
    pattern = r"\n|--|#|\||`|\*\*(?=\w+)|(?<=\w)+\*\*|\s{2,}|\.+"
    return re.sub(pattern, "", text)      


# deleting embedded data when user file changes
def clear_session_embedded_data():
    """Clear document embedding data"""
    if "embedded_data" in st.session_state:
        del st.session_state["embedded_data"]

def model_prompt(old_output, new_q):
    """The function aims to create a prompt for llm which includes one previous history."""
    message = [{"role": "system", "content": """You help everyone by answering questions, and improve your answers from previous answer in History.
                                                Don't try to make up an answer, if you don't know just say that you don't know.
                                                Answer in the same language the question was asked.
                                                Answer in a way that is easy to understand.
                                                Do not say "Based on the information you provided, ..." or "I think the answer is...". Just answer the question directly in detail.
                                                Use only the following pieces of context to answer the question at the end."""},

                {"role": "user", "content": old_output['user_previous_query']},

                {"role": "system", "content": old_output['system_previous_query']},
                
                {"role": "user", "content": new_q}]
    return message
     