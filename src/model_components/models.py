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
            model = pipeline("text-generation", model="Qwen/Qwen2-0.5B-Instruct", use_fast=True)
            return model
        except Exception as e:
            print(f"Error in loading text-to-text model: {str(e)}")
        

    @staticmethod
    def QA_model(u_input, type, context:str = None):
        try:
            if type=="qa":
                messages = [{"role": "system", "content": """**Instructions:**
                                                            1. You assist users by providing clear and accurate answers to their questions. 
                                                            2. Limit your answers to 201 characters. 
                                                            3. Answer in the language in which question is asked."""},
                            {"role": "user", "content": u_input}]
                
                output = Model.load_t2t_model()(messages, max_new_tokens = 196)
                return output[0]['generated_text'][2]['content']
            
            
            elif type=='summary':
                messages = [{"role": "system", "content": "You are a assistant bot."},
                            {"role": "user", "content": f"""### Task: Summarize the Context extracted from a uploaded PDF document.

                                                                    **Context:**
                                                                    {context}

                                                                    **Query:**
                                                                    {u_input}

                                                                    **Instructions:**
                                                                    1. Limit your answers to 201 characters.
                                                                    2. Review the provided context.
                                                                    3. Summarize the relevant details to answer the query.
                                                                    4. Always respond in the language in which the question was asked.
                                                                    5. Ensure the summary is clear and concise. 
                                                                    
                                                                    **Summary: **"""}]

                
                output = Model.load_t2t_model()(messages, max_new_tokens = 196)
                return output[0]['generated_text'][2]['content']

        except Exception as e:
            print(f"Error in generating text-to-text model output from Model class: {str(e)}")    