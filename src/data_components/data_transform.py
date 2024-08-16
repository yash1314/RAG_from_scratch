import pymupdf, os, time
import streamlit as st
from src.data_components.data_ingestion import DataFile
from utils import reg_x
import pandas as pd

class PDF_Extract_Transform:
    """
    This class extract, transform and load user pdf data  
    """

    @staticmethod
    def extract_text(file_path):
        """
        Extract and return data from uploaded pdf 
        """
        try:
            doc = pymupdf.open(file_path)  

            full_text = [page.get_text() for page in doc]
            cleaned_text = [reg_x(page.replace("\n", " ")) for page in full_text]

            combined_text = " ".join(cleaned_text)
            
            chunk_size = 2000  
            overlap = 100  #overlap to preserve information/context

            chunks = []
            start = 0
            while start < len(combined_text):
                end = min(start + chunk_size, len(combined_text))
                chunk = combined_text[start:end]
                chunks.append(chunk)
                start += chunk_size - overlap 

            return chunks

        except Exception as e:
            print(f"Error in data extraction: {str(e)}")
            return []


    @staticmethod
    def transform(file_name, file_path, save_path):
        """
        Transform extracted data and save as csv file.
        """
        try:
            # reading pdf file and extracting data
            pdf_file_path = os.path.join(file_path, file_name)
            
            data = PDF_Extract_Transform.extract_text(file_path = pdf_file_path)

            extracted_data = pd.DataFrame(data = data[2:], columns=['edata'])

            # saving at specified path
            os.makedirs(save_path, exist_ok=True)
            extracted_data.to_csv(f"{save_path}/ext_data.csv", encoding='utf-8',
                                   index=False, header=True)
            print('Data_transformation success')
            
        except Exception as e:
            print(f'Error saving PDF file: {str(e)}') 