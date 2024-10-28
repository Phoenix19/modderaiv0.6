import json
import numpy as np
import tensorflow as tf
from src.utils.json_writer import save_json


def generate_model(prompt, config):
    # Load the pre-trained model
    model = tf.keras.models.load_model('minecraft_model_generator.h5')

    # Convert prompt to suitable input format
    prompt_input = np.array([ord(c) for c in prompt]).reshape((1, config['prompt_length'], 1))

    # Generate model data
    generated_data = model.predict(prompt_input)
    model_data = array_to_model(generated_data[0])

    output_path = config['output_path']
    save_json(model_data, output_path, "generated_model.json")
    print(f"Model saved to {output_path}")
    return model_data


def array_to_model(array):
    # Convert array back to JSON model (placeholder)
    return {str(i): float(array[i]) for i in range(len(array))}
