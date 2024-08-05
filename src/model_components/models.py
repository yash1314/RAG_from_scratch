from transformers import pipeline
from sentence_transformers import SentenceTransformer
import streamlit as st


class Model:
    """This class contains model for different task which include summarization model 
    and embedding model."""

    @staticmethod
    @st.cache_resource(show_spinner=False)
    def load_summary_model():
        try:
            model_name = "Falconsai/text_summarization"
            pipe = pipeline('summarization', model = model_name)
            return pipe
        except Exception as e:
            print(f"Error in loading summary model: {str(e)}")


    # @staticmethod
    # @st.cache_resource(show_spinner=False)
    # def load_t2t_model():
    #     try:
    #         model_name = "google/flan-t5-base"
    #         pipe = pipeline("text2text-generation", model= model_name)
    #         return pipe
    #     except Exception as e:
    #         print(f"Error in loading text-to-text model: {str(e)}")
    

    @staticmethod
    @st.cache_resource(show_spinner=False)
    def embed_model():
        """This is an embedding model method which generate embedding for query and context."""
        try:
            model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            return model
        except Exception as e:
            print(f"Error in loading embedding model: {str(e)}")


    @staticmethod
    def summary_model(query:str, context:str):
        try:
            f_text = f"Context:\n{context}\n\nQuery:\n{query}\n\nSummarize the context that address the query."
            res = Model.load_summary_model()(f_text, max_new_tokens = 200)
            return res[0]["summary_text"]
        except Exception as e:
            print(f"Error in generating summary model output from Model class: {str(e)}")
    

    # @staticmethod
    # def QA_model(u_input):
    #     try: 
    #         qa_prompt = f"""You are an assistant bot. Answer my questions briefly.\nQuestion: {u_input}"""  
    #         output = Model.load_t2t_model()(qa_prompt, max_new_tokens = 384) 
    #         return output[0]['generated_text']
    #     except Exception as e:
    #         print(f"Error in generating text-to-text model output from Model class: {str(e)}")

    
    @staticmethod
    @st.cache_resource(show_spinner=False)
    def QA_model(u_input):
        try:
            messages = [{"role": "system", "content": "You are a sarcastic assistant."},
                        {"role": "user", "content": u_input}]
            
            pipe = pipeline("text-generation", model="Qwen/Qwen2-0.5B-Instruct")
            output = pipe(messages, max_new_tokens = 200)
            return output[0]['generated_text'][2]['content']
        
        except Exception as e:
            print(f"Error in generating text-to-text model output from Model class: {str(e)}")


    