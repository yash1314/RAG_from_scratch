import os, shutil, sys
import streamlit as st
from src.logger import logging
from src.exception import CustomException

class DataFile:
    """The File class takes user file and perform file opeartions such as read, write, delete."""
    

    @staticmethod
    def create_file(file_name, file_path):
        """
        Create file at specific location using the file name with file extension
        """
        try : 
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            full_path = os.path.join(file_path, file_name)

            logging.info(f"File successfully created at {full_path}")
            return full_path
                
        except Exception as e:
            logging.info(f"Error in file creation at {full_path}")
            

            

    @staticmethod
    def store_file(file:None, folder_name:str):
        """
        Store user file upon uploading.
        """
        try: 
            folder = folder_name
            if not os.path.exists(folder):
                os.makedirs(folder)

            with open(os.path.join(folder, file.name), mode='wb') as w:
                w.write(file.getvalue())

            logging.info(f"File {file.name}, successfully stored at {folder}")

        except Exception as e:
            logging.info(f"Error in storing file {file.name}")
            


    @staticmethod
    def remove_file(folder_name:str = None):
        """
        Remove/delete file from the system
        """
        try:             
            if os.path.isdir(folder_name):
                shutil.rmtree(folder_name)
                logging.info(f"File {folder_name} successfully removed")
            
        except Exception as e:
            logging.info(f"Error in removing file {folder_name}")
            