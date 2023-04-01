#!/usr/bin/env python3
from pathlib import Path
import yaml
from attrdict import AttrDict

from pathlib import Path

def _update_config(config_dict, folder, path_keys=("_path", "_folder"), parent_dict=None):
    def update_path(value, combined_dict):
        for key, val in combined_dict.items():
            value = value.replace('{' + key + '}', str(val))
        return Path(folder / value).resolve()

    def process_value(value, combined_dict):
        if isinstance(value, dict):
            return _update_config(value, folder, path_keys, combined_dict)
        elif isinstance(value, list):
            return [process_value(item, combined_dict) for item in value]
        else:
            return value

    if parent_dict is None:
        combined_dict = config_dict
    else:
        combined_dict = {**parent_dict, **config_dict}

    updated_config = {}
    for key, value in config_dict.items():
        if any(key.endswith(path_key) for path_key in path_keys):
            updated_config[key] = update_path(value, combined_dict)
        else:
            updated_config[key] = process_value(value, combined_dict)

    return AttrDict(updated_config)




def read_config(config_path, path_keys=("_path", "_folder")):
    config_path = Path(config_path).resolve()
    with open(config_path, "r") as yaml_file:
        config = AttrDict(yaml.safe_load(yaml_file))
    config = _update_config(config, config_path.parent, path_keys)
    #print(f"{config=}")
    return config


def diff(obj1, obj2):
    differences = []

    # Get a list of attributes and methods of the objects
    obj1_attributes = dir(obj1)
    obj2_attributes = dir(obj2)

    # Combine and deduplicate the attribute names from both objects
    all_attributes = list(set(obj1_attributes).union(set(obj2_attributes)))

    for attr_name in all_attributes:
        # Skip if the attribute is a method or a built-in attribute
        if (
            attr_name.startswith("__")
            or callable(getattr(obj1, attr_name, None))
            or callable(getattr(obj2, attr_name, None))
        ):
            continue

        # Get the attribute values from both objects
        obj1_attr_value = getattr(obj1, attr_name, None)
        obj2_attr_value = getattr(obj2, attr_name, None)

        # Compare the attribute values
        if obj1_attr_value != obj2_attr_value:
            differences.append((attr_name, obj1_attr_value, obj2_attr_value))

    return differences
