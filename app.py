import streamlit as st
from streamlit import _bottom
import time, sys
from utils import stream_output

from src.pipelines.main_pipe import file_handling
from src.data_components.data_ingestion import DataFile
from src.data_components.data_similarity_search import Similarity_Search
from src.model_components.models import Model

from src.exception import CustomException
from src.logger import logging



st.set_page_config(page_title="Chat with PDF and retrieve document", page_icon="📚", layout="wide", 
                   initial_sidebar_state="expanded")


# bot and user chat alignment
with open ('design.css') as source:
    st.markdown(f"<style>{source.read()}</style>",unsafe_allow_html=True)

st.markdown('<style>div.block-container{padding-top:0.4rem;}</style>', unsafe_allow_html=True)
st.header("*Your :violet[Document], Your :violet[Chat]* 💬 !")

with st.expander(label="📋 Tips & Guidance"):
    st.markdown("""
        **I appreciate and welcome your engagement with this application! Upload your PDF using the side section (arrow on top left), ask a question, and get summaries based on your query.**<br>

        **:green[Enjoy exploring!]**
        """, unsafe_allow_html=True)

# markdown to add Name and Profile links
with st.sidebar:
    st.markdown('# Contact:')
    st.markdown(":red[------------------------------------]")
    st.subheader('Made by: Yash Keshari')
    st.markdown("### [Linkedin](https://www.linkedin.com/in/yash907/), [Github](https://github.com/yash1314)")

# to handle file in stramlit file uploader function
if "file_uploader_key" not in st.session_state:
    st.session_state["file_uploader_key"] = 0

# User Input with data extration, transformation and saving the data.
with _bottom.popover('Upload File'):  
    with st.container():           
        user_file = st.file_uploader(label=':blue[**Upload your PDF file!**]',
                                                type= 'pdf', accept_multiple_files=False, key=st.session_state["file_uploader_key"])
        upload_button = st.button('Upload_file', use_container_width=True)
        if upload_button:
            if user_file is not None:   
                with st.spinner('Loading and transforming Data.'):
                    time.sleep(0.2)
                    file_handling(file = user_file)
                    time.sleep(0.1)
                    st.success('File transformed successfully!', icon="✅")
            else:
                st.error('Upload file before submitting.')

        delete_button = st.button('Delete file', use_container_width=True)
        if delete_button:
            if user_file is not None:
                DataFile.remove_file(folder_name = 'artifact')
                st.success(f"File {user_file.name} deleted successfully", icon="✅")
                st.session_state["file_uploader_key"] += 1
                st.rerun()
            else:
                try:
                    DataFile.remove_file(folder_name = 'artifact')
                    st.success(f"File '{user_file.name}' deleted successfully")
                except Exception as e:
                    st.error(f'Upload file before deleting.')


# initializing chat history 
if "messages" not in st.session_state:
        st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat elements 
if not user_file:       #If user doen't upload any file then the model talks casually.
    if prompt := st.chat_input("Talk to a Chatbot"):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            with st.chat_message("assistant"):
                with st.spinner(" "):
                    start_time = time.monotonic()

                    res = Model.gradio_model(message = prompt, type = "qa")    
                    response = st.write_stream(stream_output(res))
                    
                    processed_time = round(time.monotonic() - start_time, ndigits=2)
                    st.markdown(f'<div style="text-align: right;">Processed time: {processed_time} seconds</div>',
                                unsafe_allow_html=True)
        except Exception as e:
            logging.info(f"Error in generating casual response.")
            raise CustomException(e, sys)
            res = 'Error in generating casual response'

        st.session_state.messages.append({"role": "assistant", "content": res})

else:
    if prompt := st.chat_input("Talk to your PDF"):     #When user uploads pdf file, then the bot can only be used for QA task

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                with st.spinner(" "):
                    start_time = time.monotonic()
                    simm_data = Similarity_Search.similarity_compute(user_query=prompt, file_read_path="artifact/data/ext_data.csv")
                    
                    if simm_data == None:
                        res = Model.gradio_model(message = prompt, type = "qa")
                        response = st.write_stream(stream_output(res))
                    else:
                        res = Model.gradio_model(message = prompt, type = "summary", context=simm_data)
                        response = st.write_stream(stream_output(res))
                        
                        processed_time = round(time.monotonic() - start_time, ndigits=2)
                        with st.expander("Click to see context data from PDF"):
                            st.write(simm_data)
                        st.markdown(f'<div style="text-align: right;">Processed time: {processed_time} seconds</div>',
                                unsafe_allow_html=True)
                        
            except Exception as e:
                logging.info(f"Error in generating summary response.")
                raise CustomException(e, sys)
                res = 'Error in generating summary response'
                    
        st.session_state.messages.append({"role": "assistant", "content": res})
