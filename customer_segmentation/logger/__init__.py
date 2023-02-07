import logging
import os
from datetime import datetime

def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

def get_log_file_name():
    return f"log_{get_current_time_stamp()}.log"
log_file_name = get_log_file_name()

log_folder_name = 'logs'
os.makedirs(log_folder_name,exist_ok=True)
log_dir = os.path.join(log_folder_name, log_file_name)
print(log_dir)

logging.basicConfig(filename=log_dir, filemode='w', 
                    format= '[%(asctime)s];%(levelname)s;%(message)s',
                    level = logging.INFO)