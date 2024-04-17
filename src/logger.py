import logging
import io
from globals import debug, timestamp


# Create a logger
logger = logging.getLogger(__name__)

if debug:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# Create a handler to write logs to a file
file_handler = logging.FileHandler("session_"+timestamp+"_app.log")
file_handler.setLevel(logging.DEBUG)

# Create another handler to store logs in a variable
log_stream = io.StringIO()
stream_handler = logging.StreamHandler(log_stream)
stream_handler.setLevel(logging.DEBUG)

# Create a formatter and add it to both handlers
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
