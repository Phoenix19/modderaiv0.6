import json
import os


def save_json(data, path, filename):
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, filename)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"JSON saved to {file_path}")
