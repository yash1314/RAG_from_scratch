import streamlit as st 
import time
from utils import output_stream, casual_responses

from src.pipelines.main_pipe import file_handling
from src.data_components.data_ingestion import DataFile
from src.data_components.data_similarity_search import Similarity_Search
from src.model_components.models import Model

st.set_page_config(page_title="Chat with PDF and retrieve document", page_icon="🦙", layout="wide", 
                   initial_sidebar_state="auto")


# bot and user chat alignment
with open ('design.css') as source:
    st.markdown(f"<style>{source.read()}</style>",unsafe_allow_html=True)

st.markdown('<style>div.block-container{padding-top:0.3rem;}</style>', unsafe_allow_html=True)

st.header("*Your :violet[Document], Your :violet[Chat]* !")

with st.expander(label="📋 Tips & Guidance"):
    st.markdown("""
        **I appreciate and welcome your engagement with this application! Upload your PDF using the side section (arrow on top left), ask a question, and get summaries based on your query.**<br>

        **:green[Enjoy exploring!]**
        """, unsafe_allow_html=True)


import streamlit as st

st.markdown("""
    <div style="text-align: right;">
        <span style="display: inline-block;">Made by- <strong>Yash Keshari,</strong></span>
        <span style="display: inline-block; margin-left: 5px;">
            <a href="https://www.linkedin.com/in/yash907/" target="_blank" style="text-decoration: none; color: blue;">LinkedIn,</a>
            <a href="https://github.com/yash1314" target="_blank" style="text-decoration: none; color: blue; margin-left: 5px;">GitHub</a>
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown(" ")


# User Input with data extration, transformation and saving the data.
with st.sidebar:
    st.header('File Section', divider=True)    
    
    with st.form("File_handling"):                
        user_file = st.file_uploader(label=':blue[**Upload your PDF file!**]',
                                            type= 'pdf', accept_multiple_files=False)

        submit = st.form_submit_button("Submit", use_container_width=True)
        if submit:
            # File saving and transformation
            if user_file:   
                with st.spinner('Loading and transforming Data.'):
                    time.sleep(0.5)
                    file_handling(file = user_file)
                    time.sleep(0.5)
                st.success('File transformed successfully!', icon="✅")
                
            else:
                st.error('Upload PDF file before submitting.')

        delete = st.form_submit_button('Delete file')
        if delete:
            if user_file:
                DataFile.remove_file(folder_name = 'artifact')
                st.success(f"File {user_file.name} deleted successfully")
            else:
                try:
                    DataFile.remove_file(folder_name = 'artifact')
                    st.success(f"File {user_file.name} deleted successfully")
                except Exception as e:
                    st.error(f'Upload PDF file before deleting.')

        

# initializing chat history 
if "messages" not in st.session_state:
        st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat elements 
if not user_file:       #If user doen't upload any file then the model talks casually.
    if prompt := st.chat_input("Talk to your PDF"):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(" "):
                start_time = time.monotonic()

                res = casual_responses(prompt)
                response = st.write_stream(res)
                
                processed_time = round(time.monotonic() - start_time, ndigits=2)
                st.markdown(f'<div style="text-align: right;">Processed time: {processed_time} seconds</div>',
                            unsafe_allow_html=True)
   
        st.session_state.messages.append({"role": "assistant", "content": response})

else:
    if prompt := st.chat_input("Talk to your PDF"):     #When user uploads pdf file, then the bot can only be used for QA task

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(" "):
                start_time = time.monotonic()
                simm_data = Similarity_Search.similarity_compute(user_query=prompt, file_read_path="artifact/data/ext_data.csv")
                if simm_data == None:
                    res = casual_responses(prompt)
                    response = st.write_stream(res)
                else:
                    # final_output = Model.summary_model(query = prompt, context = simm_data)
                    final_output = Model.QA_model(u_input = prompt, type = "summary", context=simm_data)
                    response = st.write_stream(output_stream(final_output))

                    processed_time = round(time.monotonic() - start_time, ndigits=2)

                    with st.expander("Click to see context data from PDF"):
                        st.write(simm_data)
                    st.markdown(f'<div style="text-align: right;">Processed time: {processed_time} seconds</div>',
                            unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})