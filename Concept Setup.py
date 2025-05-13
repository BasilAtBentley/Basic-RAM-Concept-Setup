import sys
from ram_concept.concept import Concept
from datetime import datetime
import os

# Get the path to the project folder)
project_folder = os.path.abspath(os.path.dirname(__file__))
log_path = os.path.join(project_folder, "concept_log.txt")

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_path, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

# Define model path
model_path = sys.argv[1]
log(f"Starting script. Model path: {model_path}")

# Start Concept
concept = Concept.start_concept(headless=True)
log(f"RAM Concept responded: {concept.ping()}")

# Open Model
model = concept.open_file(model_path)
log(f"Model opened successfully: {model_path}")

# Shut down and finish 
concept.shut_down()
log("Script completed and RAM Concept shut down.")
