import logging, os, sys, datetime

LOG_FILE = f"{datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"   # Log File name 

log_dir = os.path.join(os.getcwd(), 'logs', LOG_FILE)     # creates the path for log folder with file_name

os.makedirs(log_dir, exist_ok=True)   # make dir, if exist prevent error messages

LOG_FILE_PATH = os.path.join(log_dir, LOG_FILE)   # join log_path and log_files 

logging.basicConfig(                                # Set config for logging system.
    filename=LOG_FILE_PATH,
    format = "[%(asctime)s] %(lineno)d - %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO )