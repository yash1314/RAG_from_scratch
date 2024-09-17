import time

# form = st.form("my_form")
# form.slider("Inside the form")
# st.slider("Outside the form")

# # Now add a submit button to the form:
# form.form_submit_button("Submit")

import streamlit as st
from streamlit import _bottom
from src.pipelines.main_pipe import file_handling
from src.data_components.data_ingestion import DataFile



    
with _bottom.popover("File section"):
    with st.form("my_form"):
        user_file = st.file_uploader('Enter you file.', accept_multiple_files=False, type='pdf')
    
        submitted = st.form_submit_button("Submit file", use_container_width=True)
        remove = st.form_submit_button('Remove file', use_container_width=True)
        if submitted:
            if user_file is not None:   
                    with st.spinner('Loading and transforming Data.'):
                        time.sleep(0.2)
                        file_handling(file = user_file)
                        time.sleep(0.1)
                        st.success('File transformed successfully!', icon="✅")
            else:
                st.error('Upload file before submitting.')

        if remove:
            if user_file is not None:
                time.sleep(0.7) 
                DataFile.remove_file(folder_name = 'artifact')
                time.sleep(0.5)
                st.success("File removed successfully", icon = "✅")
            else:
                try:
                    DataFile.remove_file(folder_name = 'artifact')
                    st.success(f"File '{user_file.name}' deleted successfully")
                except Exception as e:
                    st.error(f'Upload file before removing.')


if user_file:
    st.success("File present")
else:
    st.error('File not present')
        