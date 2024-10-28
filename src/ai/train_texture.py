# src/ai/train_texture.py
import yaml
import tensorflow as tf
from ..utils.data_loader import load_textures

# Load config
with open("config.yaml", "r") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Access specific configuration for texture generator
texture_path = config['texture_generator']['texture_path']
texture_model_save_path = config['texture_generator']['output_path']
texture_model_epochs = config['texture_generator']['epochs']

# Define texture input dimensions
texture_height = 64  # Replace with the actual height of your textures
texture_width = 64  # Replace with the actual width of your textures

# Load textures
textures = load_textures(texture_path)
print(f"Loaded {len(textures)} textures")


# Function to create the texture model
def create_texture_model(height, width):
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(height, width, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model


# Example training logic
for texture_data in textures:
    texture_model = create_texture_model(texture_height, texture_width)
    texture_model.fit(texture_data['train'], texture_data['labels'], epochs=texture_model_epochs)
    texture_model.save(f"{texture_model_save_path}/texture_model_{texture_data['name']}.h5")
    print(f"Saved texture model: {texture_data['name']}")
