import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define required keys with their default values
required_keys = {
    'format_version': "1.0",
    'minecraft:geometry': {},
    'train': [],
    'labels': [],
    'names': []
}


def validate_and_fix_json(file_path):
    with open(file_path, 'r') as f:
        model_data = json.load(f)
    missing_keys = [key for key in required_keys if key not in model_data]

    # Add missing keys with default values
    for key in missing_keys:
        model_data[key] = required_keys[key]
        logger.info(f"Added missing key '{key}' to {file_path}")

    # Write the updated data back to the file if any keys were missing
    if missing_keys:
        with open(file_path, 'w') as f:
            json.dump(model_data, f, indent=4)
        logger.info(f"Updated file {file_path} with missing keys")
    else:
        logger.info(f"No keys missing in {file_path}")

    return f"Validation and update completed for {file_path}"


def process_model(file_path):
    try:
        # Validate and fix JSON structure before processing
        validation_message = validate_and_fix_json(file_path)
        logger.info(validation_message)

        # Re-read the potentially updated JSON file
        with open(file_path, 'r') as f:
            model_data = json.load(f)

        logger.info(f"Processing model file: {file_path}")
        logger.info(f"Keys in model_data: {model_data.keys()}")
        if 'names' not in model_data:
            logger.warning(f"'names' key is missing in model_data from file: {file_path}")
        else:
            logger.info(f"First element in train data for model {model_data['names'][0]}: {model_data['train'][0]}")
    except (OSError, json.JSONDecodeError) as e:
        logger.error(f"Error processing file {file_path}: {e}")


def batch_process_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.geo.json'):
            file_path = os.path.join(directory_path, filename)
            process_model(file_path)


# Replace 'path/to/your/models' with your actual directory path
directory_path = os.path.join(os.path.dirname(__file__), '../data/models')
batch_process_directory(directory_path)
