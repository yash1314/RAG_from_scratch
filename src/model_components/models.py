from transformers import pipeline
from sentence_transformers import SentenceTransformer
import streamlit as st

from src.exception import CustomException
from src.logger import logging
import sys


class Model:
    """This class contains model for different task which include summarization model 
    and embedding model."""

    @st.cache_resource(show_spinner=False)
    def embed_model():
        """This is an embedding model method which generate embedding for query and context."""
        try:
            model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            return model
        
        except Exception as e:
            logging.info(f"Error in loading embedding model.")
            CustomException(e, sys)

    @st.cache_resource(show_spinner=False)
    def load_t2t_model():
        try:
            model = pipeline("text-generation", model="Qwen/Qwen2-0.5B-Instruct", use_fast=True)
            return model
        except Exception as e:
            logging.info(f"Error in loading text-to-text model.")
            CustomException(e, sys)
        

    @staticmethod
    def QA_model(u_input, type, context:str = None):
        try:
            if type=="qa":
                messages = [{"role": "system", "content": "**Instructions:**\n1. Provide clear, accurate answers based on the context, including previous interactions and query.\n2. Use the same language as the question.\n3. Be concise but, shortish answers are better. Never omit detail.\n4. Incorporate information from previous questions and answers to provide a coherent response.\n5. If you cannot provide an answer based on the provided context, acknowledge this politely and state that you do not have enough information."},
                            {"role": "user", "content": u_input}]
                
                output = Model.load_t2t_model()(messages, max_new_tokens = 500)
                return output[0]['generated_text'][2]['content']
            
            
            elif type=='summary':
                messages = [{"role": "system", "content": """You are an assistant bot specializing in summarizing texts. Follow these rules:
        
                                                            1. **Summary Limit**: The summary must be less than 500 characters.
                                                            2. **Review Context**: Carefully read the context provided.
                                                            3. **Conciseness**: Summarize clearly, focusing on the key points.
                                                            4. **Language**: Respond in the language of the query.
                                                            5. **Relevance**: Address the query directly based on the context."""},
                            
                            {"role": "user","content": f"""**Task**: Summarize the context based on query.
                                                                    **Context:**
                                                                    {context}

                                                                    **Query:**
                                                                    {u_input}

                                                                    **Summary:**"""}]

                
                output = Model.load_t2t_model()(messages, max_new_tokens = 500)
                return output[0]['generated_text'][2]['content']

        except Exception as e:
            logging.info(f"Error in generating text-to-text model output from Model class")
            CustomException(e, sys)
        