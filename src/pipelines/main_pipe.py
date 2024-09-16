from src.data_components.data_ingestion import DataFile
from src.data_components.data_transform import PDF_Extract_Transform
from src.data_components.data_similarity_search import Similarity_Search
from src.logger import logging
from src.exception import CustomException

import sys

def file_handling(file):
    
    # store file.
    DataFile.store_file(file=file, folder_name='artifact')

    # extract data and transform file.
    PDF_Extract_Transform.transform(file_name=file.name, file_path='artifact', save_path="artifact/data")

    # Perform embedding and similarity search on transformed data.
    Similarity_Search.embed_data('artifact/data/ext_data.csv')

    logging.info("File successfully handled.")
