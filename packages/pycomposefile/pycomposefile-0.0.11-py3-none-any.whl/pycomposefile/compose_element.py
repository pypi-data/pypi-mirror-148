import re
import os


class DataTypeTransformer():
    def transform_supported_data(self, transform, value, valid_values=None):
        if valid_values is not None:
            value = self.transform_and_validate_supported_data(value, transform, valid_values)
        else:
            value = transform(self.replace_environment_variables(value))
        return value

    def transform_and_validate_supported_data(self, value, data_transformer, valid_values):
        # TODO: if the data is an integer or decimal, should there be a "between" check?
        transformed = data_transformer(self.replace_environment_variables(value))
        if isinstance(transformed, int) and valid_values[0] <= transformed <= valid_values[1]:
            return transformed
        elif transformed not in valid_values:
            # TODO: Should this return None or should this raise?
            return None
        else:
            return transformed

    def replace_environment_variables(self, value):
        value = str(value)
        value = self.replace_environment_variables_with_empty_unset(value)
        value = self.replace_environment_variables_with_unset(value)
        value = self.replace_environment_variables_with_braces(value)
        value = self.replace_environment_variables_without_braces(value)

        return value

    def replace_environment_variables_with_empty_unset(self, value):
        capture = re.compile(r"\$\{(?P<variablename>\w+)\:-(?P<defaultvalue>\w+)\}")
        matches = capture.search(value)
        while matches:
            env_var = os.environ.get(matches.group("variablename"))
            default_value = matches.group("defaultvalue")
            if env_var is None or len(env_var) == 0:
                env_var = default_value
            value = re.sub(f"\\{matches[0]}", env_var, value)
            matches = capture.search(value)
        return value

    def replace_environment_variables_with_unset(self, value):
        capture = re.compile(r"\$\{(?P<variablename>\w+)-(?P<defaultvalue>\w+)\}")
        matches = capture.search(value)
        while matches:
            env_var = os.environ.get(matches.group("variablename"))
            default_value = matches.group("defaultvalue")
            if env_var is None:
                env_var = default_value
            value = re.sub(f"{matches[0]}", env_var, value)
            matches = capture.search(value)
        return value

    def replace_environment_variables_with_braces(self, value):
        capture = re.compile(r"\$\{(?P<variablename>\w+)\}")
        matches = capture.search(value)
        while matches:
            env_var = os.environ.get(matches.group("variablename"))
            value = re.sub(f"\\{matches[0]}", env_var, value)
            matches = capture.search(value)
        return value

    def replace_environment_variables_without_braces(self, value):
        capture = re.compile(r"\$(?P<variablename>\w+)")
        matches = capture.search(value)
        while matches:
            env_var = os.environ.get(matches.group("variablename"))
            value = re.sub(f"\\{matches[0]}", env_var, value)
            matches = capture.search(value)
        return value


class ComposeElement(DataTypeTransformer):
    element_keys = {}

    def __init__(self, config, compose_path=""):
        self.compose_path = compose_path
        for key in self.element_keys.keys():
            config_element = config.pop(key, None)
            key_config = self.element_keys[key]
            self.set_supported_property_from_config(key, key_config, config_element, compose_path)
        for key in config.keys():
            # raise Exception(f"Failed to map {key} in {compose_path}")
            pass

    def set_supported_property_from_config(self, key, key_config, value, compose_path):
        valid_values = None
        if type(key_config[0]) is tuple:
            transform, valid_values = key_config[0]
        else:
            transform = key_config[0]

        if transform is not None:
            if isinstance(value, dict):
                value = transform(value, key, compose_path)
            elif isinstance(value, list):
                value = transform(value, key, compose_path)
            elif value is not None:
                value = self.transform_supported_data(transform, value, valid_values)
        else:
            # TODO: Logging message if value was not None
            value = None
        self.__setattr__(key, value)

    @classmethod
    def from_parsed_yaml(cls, config, name, compose_path):
        if config is None:
            return None
        compose_path = f"{compose_path}/{name}"
        return cls(config, compose_path)


class ComposeStringOrListElement(DataTypeTransformer, list):
    transform = None
    valid_values = None

    def __init__(self, config, key=None, compose_path=None,):
        if compose_path is not None:
            self.compose_path = f"{compose_path}/{key}"

        if isinstance(config, list):
            for v in config:
                if isinstance(v, str):
                    v = v.strip("[]").rstrip().lstrip().strip("'")
                    self.append_transform(v)
                else:
                    self.append_transform(v, key, compose_path)
        else:
            self.append_transform(config, key, compose_path)

    def append(self, __object) -> None:
        if isinstance(__object, list):
            for element in __object:
                super().append(element)
        else:
            super().append(__object)

    def append_transform(self, config_value, key=None, compose_path=None):
        if isinstance(config_value, str) or isinstance(config_value, int):
            self.append(self.transform_supported_data(self.transform, config_value, self.valid_values))
        else:
            self.append(self.transform(config_value, key, compose_path))
