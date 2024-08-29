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
                messages = [{"role": "system", "content": "**Instructions:**\n1. Provide clear, accurate answers.\n2. Limit answers to 201 tokens while excluding query input tokens.\n3. Use the same language as the question.\n4.Shortish answers are better. But don't omit detail."},
                            {"role": "user", "content": u_input}]
                
                output = Model.load_t2t_model()(messages, max_new_tokens = 196+len(u_input.split(" ")))
                return output[0]['generated_text'][2]['content']
            
            
            elif type=='summary':
                messages = [{"role": "system", "content": """You are an assistant bot specializing in summarizing texts. Follow these rules:
        
                                                            1. **Limit Summary**: The summary must be within 201 characters.
                                                            2. **Review Context**: Carefully read the context provided.
                                                            3. **Conciseness**: Summarize clearly, focusing on the key points.
                                                            4. **Language**: Respond in the language of the query.
                                                            5. **Relevance**: Address the query directly based on the context.
                                                            6. **Objectivity**: Maintain neutrality and avoid personal opinions."""},
                            {"role": "user","content": f"""Task: Summarize the context from uploaded PDF document.
                                                                    **Context:**
                                                                    {context}

                                                                    **Query:**
                                                                    {u_input}

                                                                    **Summary: **"""}]

                
                output = Model.load_t2t_model()(messages, max_new_tokens = 196)
                return output[0]['generated_text'][2]['content']

        except Exception as e:
            print(f"Error in generating text-to-text model output from Model class: {str(e)}")    