import logging
from  logging.handlers import RotatingFileHandler
import os
def setup_logging(log_file='app.log'):
    # Basic configuration (adjust as needed)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Create the 'logs' directory if it doesn't exist
    log_dir = os.path.join(project_root, 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Construct the full log file path
    log_file_path = os.path.join(log_dir, log_file)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(filename)s:%(funcName)s:%(lineno)d - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Log to console (stdout)
            RotatingFileHandler(filename=log_file_path,maxBytes=10485760,backupCount=10)
        ]
    )


