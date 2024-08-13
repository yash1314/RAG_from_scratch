from transformers import pipeline
from sentence_transformers import SentenceTransformer
import streamlit as st


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
            print(f"Error in loading embedding model: {str(e)}")


    @st.cache_resource(show_spinner=False)
    def load_t2t_model():
        try:
            return pipeline("text-generation", model="Qwen/Qwen2-0.5B-Instruct", use_fast = True)
        except Exception as e:
            print(f"Error in loading text-to-text model: {str(e)}")
        

    @staticmethod
    def QA_model(u_input, type, context:str = None):
        try:
            if type=="qa":
                messages = [{"role": "system", "content": """You are helpful and polite assistant.Below is an instruction that 
                                                    describes a task. Write a response that appropriately completes the request."""},
                            {"role": "user", "content": u_input}]
                
                output = Model.load_t2t_model()(messages, max_new_tokens = 384)
                return output[0]['generated_text'][2]['content']
            
            
            elif type=='summary':
                messages = [{"role": "system", "content": "You are pdf summary bot."},
                            {"role": "user", "content": f"""
                                                Your task is to generate a summary based on the provided query and context (extracted from pdf). 
                                                
                                                1. **Context:** ```{context}```
                                                2. **Query:** {u_input}

                            Summarize the context based on the query, focusing on relevant details and key points."""}]
                
                output = Model.load_t2t_model()(messages, max_new_tokens = 384)
                return output[0]['generated_text'][2]['content']

        except Exception as e:
            print(f"Error in generating text-to-text model output from Model class: {str(e)}")    