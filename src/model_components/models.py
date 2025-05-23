from transformers import pipeline
from sentence_transformers import SentenceTransformer
import streamlit as st
from gradio_client import Client

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
            

    @st.cache_resource(show_spinner=False)
    def load_t2t_model():
        try:
            model = pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct", use_fast=True)
            return model
        except Exception as e:
            logging.info(f"Error in loading text-to-text model.")
            

    @staticmethod
    def gradio_model(message, type, context:str=None):
        client = Client("Qwen/Qwen2.5-72B-Instruct")
        try:
            if type == 'qa':
                result = client.predict(query = message, history= [], 
                                        system = """ **Instructions:**
                                                        1. **Clarity & Accuracy**: Provide clear and accurate responses based on context.
                                                        2. **Language Consistency**: Use the same language as the question.
                                                        3. **Reference Past Queries**: Incorporate relevant past queries where applicable.
                                                        4. **Acknowledge Gaps**: Politely acknowledge any missing information.
                                                        5. **Audience Suitability**: Ensure all responses are appropriate for diverse audiences.
                                                        6. **Include Opinion**: When relevant, offer a thoughtful opinion on the matter.""", 
                                        api_name = "/model_chat")
                return result[1][0][-1]
            
            elif type=='summary':
                result = client.predict(query = f"""**Instructions**:
        
                                                            1. **Review Context**: Carefully read the context provided.
                                                            2. **Conciseness**: Summarize clearly, focusing on the key points.
                                                            3. **Language**: Respond in the language of the query.
                                                            4. **Relevance**: Address the query directly based on the context.
                                                            5. **Polite Acknowledgment**: If information is missing, acknowledge it politely and suggest next steps.
                                                            
                                                            **Context:**
                                                            {context}
                                                            
                                                            **Query:**
                                                            {message}
                                                            
                                                            **Response:**""", history= [], 
                                        system = """You are an assistant bot specializing in summarizing texts.""", 
                                        api_name = "/model_chat")
                return result[1][0][-1]
            
        except Exception as e:
            logging.info('Error in gradio model Inferencing.')



    @staticmethod
    def QA_model(u_input, type, context:str = None):
        try:
            if type=="qa":
                messages = [{"role": "system", "content": "**Instructions:**\n1. Provide clear, accurate answers based on the context, including previous interactions and query.\n2. Use the same language as the question.\n3. Be concise but, shortish answers are better. Never omit detail.\n4. Incorporate information from previous questions and answers to provide a coherent response.\n5. If you cannot provide an answer based on the provided context, acknowledge this politely and state that you do not have enough information."},
                            {"role": "user", "content": u_input}]
                
                output = Model.load_t2t_model()(messages, max_new_tokens = 500)
                return output[0]['generated_text'][2]['content']
            
            
            elif type=='summary':
                messages = [{"role": "system", "content": """You are an assistant bot specializing in summarizing texts."""},
                            
                            {"role": "user","content": f"""Follow these rules:
        
                                                            1. **Review Context**: Carefully read the context provided.
                                                            2. **Conciseness**: Summarize clearly, focusing on the key points.
                                                            3. **Language**: Respond in the language of the query.
                                                            4. **Relevance**: Address the query directly based on the context.
                                                            
                                                            **Context:**
                                                            {context}
                                                            
                                                            **Query:**
                                                            {u_input}
                                                            
                                                            **Summary:**"""}]

                
                output = Model.load_t2t_model()(messages, max_new_tokens = 500)
                return output[0]['generated_text'][2]['content']

        except Exception as e:
            logging.info(f"Error in generating text-to-text model output from Model class")