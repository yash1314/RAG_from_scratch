import streamlit as st 
import time
from utils import output_stream, casual_responses, model_prompt

from src.pipelines.main_pipe import file_handling
from src.data_components.data_ingestion import DataFile
from src.data_components.data_similarity_search import Similarity_Search
from src.model_components.models import Model

st.set_page_config(page_title="Chat with PDF and retrieve document", page_icon="🦙", layout="centered", 
                   initial_sidebar_state="collapsed")


# bot and user chat alignment
with open ('design.css') as source:
    st.markdown(f"<style>{source.read()}</style>",unsafe_allow_html=True)


st.markdown('<style>div.block-container{padding-top:0.2rem;}</style>', unsafe_allow_html=True)
st.header("*Your :rainbow[Document], Your :rainbow[Chat]* !")

with st.expander(label = ":blue[📋 Tips & Guidance]"):
    st.markdown("""
        **I appreciate and welcome your engagement with this application! Upload your PDF using the side section (arrow on top left), ask a question, and get summaries based on your query.**<br>
        
        **:rainbow[Enjoy exploring!]**
        """, unsafe_allow_html=True) 

st.markdown("""
    <div style="text-align: right;">
        <p>Made by- <strong>Yash Keshari</strong> <span style="font-size: 24px;">😎</span></p>
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
                    time.sleep(1)
                    file_handling(file = user_file)
                    time.sleep(1)
                st.success('File transformed successfully!', icon="✅")
                
                # loading models beforehand if user submit file
                Model.embed_model()
            else:
                st.error('Upload PDF file before submitting.')

        delete = st.form_submit_button('Delete file')
        if delete:
            if user_file:
                DataFile.remove_file(folder_name = 'artifact')
                st.success(f"File {user_file.name} deleted successfully")
            else:
                st.error('Upload PDF file before deleting.')

    # loading text2text model
    # Model.load_t2t_model()
        

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
                res = casual_responses(prompt)
                time.sleep(0.5)
                response = st.write_stream(res)
   
        st.session_state.messages.append({"role": "assistant", "content": response})

else:
    if prompt := st.chat_input("Talk to your PDF"):     #When user uploads pdf file, then the bot can only be used for QA task

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(" "):
                simm_data = Similarity_Search.similarity_compute(user_query=prompt, file_read_path="artifact/data/ext_data.csv")
                if simm_data == None:
                    res = casual_responses(prompt)
                    time.sleep(0.5)
                    response = st.write_stream(res)
                else:
                    # final_output = Model.summary_model(query = prompt, context = simm_data)
                    final_output = Model.QA_model(u_input = prompt, type = "qa", context=simm_data)
                    response = st.write_stream(output_stream(final_output))

                    with st.expander("Click to see context data from PDF"):
                        st.write(simm_data)

        st.session_state.messages.append({"role": "assistant", "content": response})