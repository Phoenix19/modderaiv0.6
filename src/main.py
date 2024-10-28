import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define required keys with their default values
required_keys = {
    'format_version': "1.0",
    'minecraft:geometry': {}
}

# Define optional keys with their default values
optional_keys = {
    'train': [],
    'labels': [],
    'names': []
}


def validate_and_fix_json(file_path):
    with open(file_path, 'r') as f:
        model_data = json.load(f)

    # Add missing required keys with default values
    missing_required_keys = [key for key in required_keys if key not in model_data]
    for key in missing_required_keys:
        model_data[key] = required_keys[key]
        logger.info(f"Added missing required key '{key}' to {file_path}")

    # Add missing optional keys with default values
    missing_optional_keys = [key for key in optional_keys if key not in model_data]
    for key in missing_optional_keys:
        model_data[key] = optional_keys[key]
        logger.info(f"Added missing optional key '{key}' to {file_path}")

    # Write the updated data back to the file if any keys were missing
    if missing_required_keys or missing_optional_keys:
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

        # Check if 'names' and 'train' lists are not empty before accessing their elements
        if 'names' in model_data and model_data['names']:
            if 'train' in model_data and model_data['train']:
                logger.info(f"First element in train data for model {model_data['names'][0]}: {model_data['train'][0]}")
            else:
                logger.warning(f"'train' key is present but the list is empty in file: {file_path}")
        else:
            logger.warning(f"'names' key is present but the list is empty in file: {file_path}")

    except (OSError, json.JSONDecodeError) as e:
        logger.error(f"Error processing file {file_path}: {e}")


def batch_process_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.geo.json'):
            file_path = os.path.join(directory_path, filename)
            process_model(file_path)


if __name__ == "__main__":
    # Replace 'path/to/your/models' with your actual directory path
    directory_path = os.path.join(os.path.dirname(__file__), '../data/models')
    batch_process_directory(directory_path)
