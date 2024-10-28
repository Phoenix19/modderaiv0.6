import os
import yaml
import tensorflow as tf
from ..utils.data_loader import load_models
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Load config
    config_path = os.path.join(os.path.dirname(__file__), '../../config.yaml')
    with open(config_path, "r") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    # Access specific configuration for model generator
    model_path = config['model_generator']['model_path']
    model_save_path = config['model_generator']['output_path']
    model_epochs = config['model_generator']['epochs']

    # Ensure the model path exists
    absolute_model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', model_path))
    if not os.path.isdir(absolute_model_path):
        logger.error(f"Model path does not exist: {absolute_model_path}")
        raise ValueError(f"Model path does not exist: {absolute_model_path}")

    # Define model input shape
    model_input_shape = (100,)  # Replace this with the actual shape of your input data

    # Load models
    models = load_models(absolute_model_path)
    logger.info(f"Loaded {len(models)} models")


    # Function to create the model
    def create_model(input_shape):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=input_shape),
            tf.keras.layers.Dense(10, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model


    # Example training logic
    for model_data in models:
        # Debug: Print model_data structure
        logger.info(f"Processing model: {model_data.get('name', 'Unknown')}")
        logger.info(f"Keys in model_data: {model_data.keys()}")
        if 'train' not in model_data or 'labels' not in model_data:
            logger.warning(f"Skipping model due to missing 'train' or 'labels': {model_data}")
            continue

        # Ensure model_data contains the appropriate input shape
        try:
            model = create_model(model_input_shape)
            logger.info(f"Training model: {model_data.get('name', 'Unnamed')}")
            model.fit(model_data['train'], model_data['labels'], epochs=model_epochs)
            model.save(os.path.join(model_save_path, f"model_{model_data.get('name', 'Unnamed')}.h5"))
            logger.info(f"Saved model: {model_data.get('name', 'Unnamed')}")
        except Exception as e:
            logger.error(f"Error processing model {model_data.get('name', 'Unnamed')}: {e}")

except Exception as e:
    logger.error(f"An error occurred: {e}")
