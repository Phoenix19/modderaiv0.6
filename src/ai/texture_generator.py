# src/ai/train_texture.py
import tensorflow as tf
from ..utils.data_loader import load_textures

# Path to your textures directory
texture_path = 'path/to/your/textures'

# Load textures
textures = load_textures(texture_path)
print(f"Loaded {len(textures)} textures")


# Assume you have some logic to train on your textures here
# For illustration, let's create a simple convolutional model
def create_texture_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(texture_height, texture_width, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model


# Example training logic
for texture_data in textures:
    texture_model = create_texture_model()
    texture_model.fit(texture_data['train'], texture_data['labels'], epochs=10)
    texture_model.save(f"path/to/save/texture_model_{texture_data['name']}.h5")
    print(f"Saved texture model: {texture_data['name']}")
