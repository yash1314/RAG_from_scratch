import streamlit as st
from streamlit import _bottom
from streamlit_lottie import st_lottie_spinner
import time, sys
from utils import stream_output
from resources.animation import animations 

from src.pipelines.main_pipe import file_handling
from src.data_components.data_ingestion import DataFile
from src.data_components.data_similarity_search import Similarity_Search
from src.model_components.models import Model

from src.exception import CustomException
from src.logger import logging

st.set_page_config(page_title="Chat with PDF and retrieve document", page_icon="📚", layout="wide", 
                   initial_sidebar_state="expanded",)


# bot and user chat alignment
with open ('design.css') as source:
    st.markdown(f"<style>{source.read()}</style>",unsafe_allow_html=True)


st.markdown('<style>div.block-container{padding-top:0.7rem;}</style>', unsafe_allow_html=True)
st.header("*Your:violet[Document], Your:orange[Chat]* 💬 !")

with st.expander(label="📋 Tips & Guidance"):
    st.markdown("""
        **Thank you for engaging with this application! We invite you to upload your PDF using the button at the bottom. Ask a question, and receive insightful summaries tailored to your query. We look forward to assisting you!**<br>

        **:green[Enjoy exploring!]**
        """, unsafe_allow_html=True)


# file submit and remove session state
if "submit" not in st.session_state:
        st.session_state.submit = [0]


# Taking User Input file and performing data extration, transformation and saving the data. Also handle file upload and removal 
with _bottom.popover("File section"):
    with st.form("my_form"):
        user_file = st.file_uploader('Enter you file.', accept_multiple_files=False, type='pdf')

        col3, col4 = st.columns(2)

        with col3:
            submitted = st.form_submit_button("Submit file", use_container_width=True)
            if submitted:
                if user_file is not None:
                        st.session_state.submit.insert(0, 1)
                        with st.spinner('Submitting and transforming Data.'):
                            time.sleep(0.3)
                            file_handling(file = user_file)
                            time.sleep(0.3)
                            st.success('File submitted & transformed successfully!', icon="✅")
                else:
                    st.error('Upload file before submitting.')

        with col4:
            remove = st.form_submit_button('Remove file', use_container_width=True)
            if remove:
                if user_file is not None:
                    st.session_state.submit.insert(0, 0)
                    time.sleep(0.3) 
                    DataFile.remove_file(folder_name = 'artifact')
                    time.sleep(0.3)
                    st.success("File removed successfully", icon = "✅")
                else:
                    try:
                        DataFile.remove_file(folder_name = 'artifact')
                        st.success(f"File '{user_file.name}' deleted successfully")
                    except Exception as e:
                        st.error(f'Upload file before deleting.')
                        st.empty()

# images and lottie animation
bot_img = "https://raw.githubusercontent.com/yash1314/Chatbot_streamlit/refs/heads/main/artifact/chatbot.png"
user_img = "https://raw.githubusercontent.com/yash1314/Chatbot_streamlit/refs/heads/main/artifact/woman.png"
lottie_url_casual = animations.casual_animation()
lottie_url_qa = animations.qa_animation()


# addding space
st.markdown(
    "<div style='text-align: center;'>"
    "| Made with ❤️‍🔥 by Yash Keshari |"
    "</div>",
    unsafe_allow_html=True)
st.markdown(" ")


# initializing message history 
if "messages" not in st.session_state:
        st.session_state.messages = [{'role':"assistant",
                                      "content": 
"Hello! I'm an Smart AI just a click away, ready to assist you. Ask me about anything for quick answers, and I can also summarize your queries from uploaded documents."}]

for message in st.session_state.messages:
    if message['role'] == 'user':
        with st.chat_message(message["role"], avatar=user_img):
            st.markdown(message["content"])
    elif message['role'] == 'assistant':
        with st.chat_message(message["role"], avatar=bot_img):
            st.markdown(message["content"])


# Chat elements 
if st.session_state.submit[0] == 1:       #When user uploads pdf file, then the bot can only be used for QA task
    
    if prompt := st.chat_input("Talk to your PDF"):     
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=user_img):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=bot_img):
            message_placeholder1 = st.empty()
            try:
                with st_lottie_spinner(lottie_url_qa, height=35, width=60,speed=5, loop=True):
                    start_time = time.monotonic()
                    simm_data = Similarity_Search.similarity_compute(user_query=prompt, file_read_path="artifact/data/ext_data.csv")
                    
                    if simm_data == None:
                        res = Model.gradio_model(message = prompt, type = "qa")
                        message_placeholder1.write_stream(stream_output(res))
                        with st.expander("Click to see context data from PDF"):
                            st.write('No data available from document, we are working to fix it.')
                    else:
                        res = Model.gradio_model(message = prompt, type = "summary", context=simm_data)
                message_placeholder1.write_stream(stream_output(res))
                latency = round(time.monotonic() - start_time, ndigits=2)

                with st.expander("Click to see context data from PDF"):
                    st.write(simm_data)
                st.markdown(f'<div style="text-align: right;">Latency: {latency} seconds</div>', unsafe_allow_html=True)
                        
            except Exception as e:
                logging.info(f"Error in generating summary response.")
                res = 'Error in generating summary response'
                    
        st.session_state.messages.append({"role": "assistant", "content": res})


else: #If user doen't upload any file then the model talks casually.
    
    if prompt := st.chat_input("Chat with bot"):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=user_img):
            st.markdown(prompt)

        try:
            with st.chat_message("assistant", avatar=bot_img):
                message_placeholder2 = st.empty()
                with st_lottie_spinner(lottie_url_casual, height=35, width=60,speed=5, loop=True,):
                    start_time = time.monotonic()
                    res = Model.gradio_model(message = prompt, type = "qa")    
                
                message_placeholder2.write_stream(stream_output(res))
                
                latency2 = round(time.monotonic() - start_time, ndigits=2)
                st.markdown(f'<div style="text-align: right;">Latency: {latency2} seconds</div>',
                            unsafe_allow_html=True)
        except Exception as e:
            logging.info(f"Error in generating casual response.")
            res = "Internal Error - We're working hard to fix this as soon as possible!"
            message_placeholder2.write_stream(stream_output(res))

        st.session_state.messages.append({"role": "assistant", "content": res})