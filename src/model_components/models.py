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
                messages = [{"role": "system", "content": """You assist users by providing clear and accurate answers to their questions.
                                                            If you do not know the answer, simply state that you do not know.
                                                            Always respond in the language in which the question was asked.
                                                            Provide answers that are straightforward and easy to understand.
                                                            Avoid phrases like 'Based on the information you provided, ...' or 'I think the answer is...'.
                                                            Directly address the question with detailed information using only the provided context.
                                                            Provide your answer in a maximum of 150 words."""},
                            
                            {"role": "user", "content": u_input}]
                
                output = Model.load_t2t_model()(messages, max_new_tokens = 150)
                return output[0]['generated_text'][2]['content']
            
            
            elif type=='summary':
                messages = [{"role": "system", "content": "You are a PDF summary bot."},
                            {"role": "user", "content": f"""### Task: Summarize the Context extracted from a PDF document.

                                                                    **Context:**
                                                                    {context}

                                                                    **Query:**
                                                                    {u_input}

                                                                    **Instructions:**
                                                                    1. Review the provided context.
                                                                    2. Summarize the relevant details to answer the query.
                                                                    3. Always respond in the language in which the question was asked.
                                                                    4. Ensure the summary is clear and concise.
                                                                    5. Limit your response to a maximum of 150 words.
                                                                    
                                                                    **Summary:**"""}]

                
                output = Model.load_t2t_model()(messages, max_new_tokens = 150)
                return output[0]['generated_text'][2]['content']

        except Exception as e:
            print(f"Error in generating text-to-text model output from Model class: {str(e)}")    