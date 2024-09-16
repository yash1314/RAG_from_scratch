from sklearn.metrics.pairwise import cosine_similarity 
from src.model_components.models import Model
import pandas as pd
import streamlit as st
import sys

from src.logger import logging
from src.exception import CustomException


class Similarity_Search:
    """
    Performs Similarity search between a query and the data rows. 
    Return: Top 2 similar data from document based on the query.
    """

    @st.cache_data(show_spinner=False)
    def embed_data(file_read_path): 
        # creating embedded data in streamlit session for calculating similarity compute in every session.
        if 'embedded_data' not in st.session_state:
                st.session_state.embedded_data = []
                
        try:       
            df = pd.read_csv(file_read_path)
            e_data = df['edata'].to_list()

            embedded_d = Model.embed_model().encode(e_data)

            st.session_state.embedded_data = embedded_d
            return st.session_state.embedded_data
        
        except Exception as e:
            logging.info(f"Error in embedding document data")
            
    

    @staticmethod
    def embedding_query(user_q):
        embedded_query = Model.embed_model().encode([user_q])
        return embedded_query


    @staticmethod
    def similarity_compute(file_read_path, user_query):
        try:
            df = pd.read_csv(file_read_path)

            embedded_data = st.session_state.embedded_data
            embedded_query = Similarity_Search.embedding_query(user_query)
            
            cosine_similarities = cosine_similarity(embedded_data, embedded_query)
        
        except Exception as e:
            logging.info(f"Error in calculating cosine_similarity")
            
        
        try: 
            similarity_with_idx = list(enumerate(cosine_similarities))
            similarity_with_idx.sort(key = lambda x:x[1], reverse= True)

            top_2 = similarity_with_idx[:3]
            final_str_data = ""
            for idx, val in top_2:
                final_str_data += df.iloc[idx].to_list()[0] + "\n"
            
            return final_str_data
        
        except Exception as e:
            logging.info(f"Error in fetching 2 most similar data")