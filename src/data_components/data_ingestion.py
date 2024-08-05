import os, logging
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
    def remove_file(file:str = None, folder_name:str = None):
        """
        Remove/delete file from the system
        """
        try:             
            if file:
                file_path = os.path.join(folder_name, file)

                if os.path.exists(file_path):
                    os.rmdir(file_path)
                    print(f"File {file} successfully removed.")
            
            else:
                if os.path.exists(folder_name):
                    os.rmdir(folder_name)
                    print(f"Folder {folder_name} successfully removed.")
                else:
                    print(f"Folder {folder_name} is not present.")
                
        except:
            print(f"Problem with the {file} or its path.")