import streamlit as st
from streamlit import _bottom
import time
from utils import stream_output

from src.pipelines.main_pipe import file_handling
from src.data_components.data_ingestion import DataFile
from src.data_components.data_similarity_search import Similarity_Search
from src.model_components.models import Model

st.set_page_config(page_title="Chat with PDF and retrieve document", page_icon="📚", layout="centered", 
                   initial_sidebar_state="auto")


# bot and user chat alignment
with open ('design.css') as source:
    st.markdown(f"<style>{source.read()}</style>",unsafe_allow_html=True)

st.markdown('<style>div.block-container{padding-top:0.4rem;}</style>', unsafe_allow_html=True)
st.title("*Your :violet[Document], Your :violet[Chat]* 💬 !")
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
    st.markdown("### [Linkedin](https://www.linkedin.com/in/yash907/)")
    st.markdown("### [Github](https://github.com/yash1314)")


# User Input with data extration, transformation and saving the data.
with _bottom.popover('Upload File'):  
    with st.container():           
        user_file = st.file_uploader(label=':blue[**Upload your PDF file!**]',
                                                type= 'pdf', accept_multiple_files=False)
        upload_button = st.button('Upload_file', use_container_width=True)
        if upload_button:
            if user_file is not None:   
                with st.spinner('Loading and transforming Data.'):
                    time.sleep(0.2)
                    file_handling(file = user_file)
                    time.sleep(0.2)
                    st.success('File transformed successfully!', icon="✅")
            else:
                st.error('Upload file before submitting.')

        delete_button = st.button('Delete file', use_container_width=True)
        if delete_button:
            if user_file is not None:
                DataFile.remove_file(folder_name = 'artifact')
                st.success(f"File {user_file.name} deleted successfully")
                user_file = None
            else:
                try:
                    DataFile.remove_file(folder_name = 'artifact')
                    st.success(f"File {user_file.name} deleted successfully")
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

        with st.chat_message("assistant"):
            with st.spinner(" "):
                start_time = time.monotonic()
                res = Model.QA_model(u_input = prompt, type = "qa")    
                response = st.write_stream(stream_output(res))
                processed_time = round(time.monotonic() - start_time, ndigits=2)
                st.markdown(f'<div style="text-align: right;">Processed time: {processed_time} seconds</div>',
                            unsafe_allow_html=True)
   
        st.session_state.messages.append({"role": "assistant", "content": res})

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
                    res = Model.QA_model(u_input = prompt, type = "qa")
                    response = st.write_stream(stream_output(res))
                else:
                    final_output = Model.QA_model(u_input = prompt, type = "summary", context=simm_data)
                    response = st.write_stream(stream_output(final_output))
                    processed_time = round(time.monotonic() - start_time, ndigits=2)
                    with st.expander("Click to see context data from PDF"):
                        st.write(simm_data)
                    st.markdown(f'<div style="text-align: right;">Processed time: {processed_time} seconds</div>',
                            unsafe_allow_html=True)
                    
        st.session_state.messages.append({"role": "assistant", "content": final_output})
