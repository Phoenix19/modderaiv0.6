import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

directory = './data/models'

default_train_value = ["default_training_data"]
default_labels_value = ["default_label"]


def process_json(file_path):
    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON in file: {file_path}")
            return

        modified = False
        missing_keys = []

        if 'train' not in data or not data['train']:
            if not data.get('train'):
                logger.warning(f"'train' key is missing or empty in file: {file_path}")
            data['train'] = default_train_value
            modified = True
            missing_keys.append('train')

        if 'labels' not in data:
            data['labels'] = default_labels_value
            modified = True
            missing_keys.append('labels')

        if modified:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            logger.info(f"Updated file: {file_path} with missing keys: {missing_keys}")


def process_model(file_name, model_data):
    model_name = "Unnamed"
    try:
        logger.debug(f"Processing model_data from file: {file_name} -- Content: {json.dumps(model_data, indent=2)}")

        if 'names' in model_data:
            model_name = model_data.get("names", ["Unnamed"])[0]
            logger.info(f"Training model '{model_name}' from file: {file_name}")
        else:
            logger.warning(f"'names' key is missing in model_data from file: {file_name}")

        if 'train' in model_data:
            logger.debug(
                f"'train' key found in model_data with {len(model_data['train'])} elements: {model_data['train']}")
            if model_data["train"]:
                first_train_element = model_data["train"][0]
                logger.info(f"First element in train data for model {model_name}: {first_train_element}")
            else:
                logger.error(f"The 'train' data is empty for model: {model_name}.")
                logger.info(f"Content of model_data['train']: {model_data['train']}")
        else:
            logger.error(
                f"The 'train' key is missing in model_data from file: {file_name}. Content: {json.dumps(model_data, indent=2)}")

    except IndexError as e:
        logger.error(f"Error processing model {model_name} from file {file_name}: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error processing model {model_name} from file {file_name}: {str(e)}")


def main():
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            logger.info(f"Processing model file: {filename}")
            process_json(file_path)
            with open(file_path, 'r') as file:
                model_data = json.load(file)
                logger.info(f"Keys in model_data: {model_data.keys()}")
                process_model(filename, model_data)


if __name__ == "__main__":
    main()
