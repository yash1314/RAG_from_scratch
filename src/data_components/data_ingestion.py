import os, logging, shutil
import streamlit as st


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

            print(f"File successfully create at {full_path}")
            return full_path
                
        except :
            print(f"Error in creating {file_name} at {file_path}")
        

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

            print('Data_ingestion success')

        except :
            print('Error in data ingestion') 


    @staticmethod
    def remove_file(folder_name:str = None):
        """
        Remove/delete file from the system
        """
        try:             
            if os.path.isdir(folder_name):
                shutil.rmtree(folder_name)
                print(f"File {folder_name} successfully removed.")
                
        except:
            print(f"Problem with the {folder_name} or its path.")