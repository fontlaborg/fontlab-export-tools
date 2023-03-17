#!/usr/bin/env python3
from pathlib import Path
import yaml
from attrdict import AttrDict


def _update_config(config_dict, ref_dict, folder, path_keys):
    for key, value in config_dict.items():
        if isinstance(value, str):
            value = value.format(**ref_dict)
            if folder and key.endswith(path_keys):
                value = Path(folder / value).resolve()
            config_dict[key] = value
        elif isinstance(value, list):
            for item in value:
                item = _update_config(item, ref_dict, folder, path_keys)
    return config_dict


def read_config(config_path, path_keys=("_path", "_folder")):
    config_path = Path(config_path).resolve()
    with open(config_path, "r") as yaml_file:
        config = AttrDict(yaml.safe_load(yaml_file))
    config = _update_config(config, config, config_path.parent, path_keys)
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
