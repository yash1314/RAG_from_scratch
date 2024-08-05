import streamlit as st 
from utils import output_stream, initialize_messages, casual_responses
import time

from src.pipelines.main_pipe import file_handling
from src.data_components.data_similarity_search import Similarity_Search
from src.model_components.models import Model

st.set_page_config(page_title="Chat with PDF and retrieve document", page_icon="🦙", layout="wide", 
                   initial_sidebar_state="collapsed")


# bot and user chat alignment
with open ('design.css') as source:
    st.markdown(f"<style>{source.read()}</style>",unsafe_allow_html=True)


st.markdown('<style>div.block-container{padding-top:0.2rem;}</style>', unsafe_allow_html=True)
st.header(":orange[*Your Document, Your Chat* !]")

st.markdown("""**> I appreciate and welcome your engagement with this application! Upload your PDF, ask a question, and get summaries based on 
                              your query. Also keep in mind that it may contain some redundancies. So please use with caution. :rainbow[Enjoy exploring!]**""")
st.write("Made ❤️ by **Yash Keshari**")


# User Input with data extration, transformation and saving the data.
with st.sidebar:
    st.header('File Section :')
    user_file = st.file_uploader(label=':blue[**Upload your PDF file!**]',
                                            type= 'pdf', accept_multiple_files=False)
    
    if st.button(label = "Submit File"):
        if user_file:   
            with st.spinner('Loading and transforming Data.'):
                time.sleep(1)
                file_handling(file = user_file)
                time.sleep(1)
            st.success('File transformed successfully!', icon="✅")
            
            # loading models beforehand if user submit file
            Model.load_summary_model()
            Model.embed_model()
        else:
            st.error('Upload PDF file before submitting.')
        
        # loading text to text model for casual talking 
    Model.load_t2t_model()


# initializing chat history 
initialize_messages()


# Chat elements 
if not user_file: # if user doen't upload any file then the model talks casually.
    if prompt := st.chat_input("Talk to your PDF"):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            res = casual_responses(prompt)
            response = st.write_stream(res)
   
        st.session_state.messages.append({"role": "assistant", "content": response})


else:
    if prompt := st.chat_input("Talk to your PDF"): # when user uploads pdf file, then the bot can only be used for QA task

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner('Generating..'):
                simm_data = Similarity_Search.similarity_compute(user_query=prompt, file_read_path="artifact/data/ext_data.csv")
                if simm_data == None:
                    res = casual_responses(prompt)
                    response = st.write_stream(res)
                else:
                    final_output = Model.summary_model(query = prompt, context = simm_data)
                    response = st.write_stream(output_stream(final_output))

                    with st.expander("Click to see context data from PDF"):
                        st.write(simm_data)

        st.session_state.messages.append({"role": "assistant", "content": response})