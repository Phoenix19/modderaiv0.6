import os
import json
import logging

logger = logging.getLogger(__name__)


def load_models(model_directory):
    models = []
    for file_name in os.listdir(model_directory):
        if file_name.endswith('.geo.json'):
            file_path = os.path.join(model_directory, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    model = json.load(f)
                    if not validate_model(model):
                        logger.error(f"Invalid model structure in file: {file_name}")
                        continue
                    print_model_details(model)
                    models.append(model)
            except json.JSONDecodeError as e:
                logger.error(f"Skipping invalid model file: {file_name}. JSON Decode Error: {e}")
            except Exception as e:
                logger.error(f"Error loading model file: {file_name}. Error: {e}")
    return models


def validate_model(model):
    # Validate that the JSON structure matches the expected model structure
    required_keys = {"minecraft:geometry"}
    if not all(key in model for key in required_keys):
        return False
    return True


def print_model_details(model):
    try:
        validate_and_print_model(model)
    except Exception as e:
        logger.error(f"Error printing model details: {e}")


def validate_and_print_model(json_data):
    try:
        if "minecraft:geometry" not in json_data:
            logger.error("Invalid model: 'minecraft:geometry' key not found")
            return

        geometries = json_data["minecraft:geometry"]
        if not isinstance(geometries, list):
            logger.error("Invalid model: 'minecraft:geometry' is not a list")
            return

        for geometry in geometries:
            process_geometry(geometry)

    except Exception as e:
        logger.error(f"An error occurred: {e}")


def process_geometry(geometry):
    logger.info(f"Geometry Keys: {geometry.keys()}")
    bones = geometry.get("bones", [])
    for bone in bones:
        process_bone(bone)


def process_bone(bone):
    name = bone.get("name", "Unnamed")
    parent = bone.get("parent", "No parent")
    pivot = bone.get("pivot", [])
    rotation = bone.get("rotation", [])
    cubes = bone.get("cubes", [])

    logger.info(f"Bone: {name}")
    logger.info(f"  Parent: {parent}")
    logger.info(f"  Pivot: {pivot}")
    logger.info(f"  Rotation: {rotation}")

    for cube in cubes:
        process_cube(cube)


def process_cube(cube):
    origin = cube.get("origin", [])
    size = cube.get("size", [])
    uv = cube.get("uv", [])
    inflate = cube.get("inflate", None)
    mirror = cube.get("mirror", False)

    logger.info(f"  Cube:")
    logger.info(f"    Origin: {origin}")
    logger.info(f"    Size: {size}")
    logger.info(f"    UV: {uv}")
    if inflate is not None:
        logger.info(f"    Inflate: {inflate}")
    logger.info(f"    Mirror: {mirror}")
