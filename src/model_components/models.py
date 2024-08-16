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
                messages = [{"role": "system", "content": """You help everyone by answering questions.
                                                Don't try to make up an answer, if you don't know just say that you don't know.
                                                Answer in the same language the question was asked.
                                                Answer in a way that is easy to understand.
                                                Do not say "Based on the information you provided, ..." or "I think the answer is...". Just answer the question directly in detail.
                                                Use only the following pieces of context to answer the question at the end."""},
                            {"role": "user", "content": u_input}]
                
                output = Model.load_t2t_model()(messages, max_new_tokens = 150)
                return output[0]['generated_text'][2]['content']
            
            
            elif type=='summary':
                messages = [{"role": "system", "content": "You are pdf summary bot."},
                            {"role": "user", "content": f"""### Task: Summarize the Context

                                                                    **Context:**
                                                                    {context}

                                                                    **Query:**
                                                                    {u_input}

                                                                    **Instructions:**
                                                                    1. Review the context provided.
                                                                    2. Answer the query by summarizing the relevant details from the context.
                                                                    3. Ensure the summary is clear, concise, and directly addresses the query.

                                                                    **Summary:**
                                                                    """}]
                
                output = Model.load_t2t_model()(messages, max_new_tokens = 150)
                return output[0]['generated_text'][2]['content']

        except Exception as e:
            print(f"Error in generating text-to-text model output from Model class: {str(e)}")    