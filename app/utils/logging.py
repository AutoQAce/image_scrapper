import logging
from  logging.handlers import RotatingFileHandler

def setup_logging(log_file='app.log'):
    # Basic configuration (adjust as needed)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Log to console (stdout)
            RotatingFileHandler(filename=f"G:\Projects\API\Imagescrapper\logs\{log_file}",maxBytes=1500000000000,backupCount=10)
        ]
    )


