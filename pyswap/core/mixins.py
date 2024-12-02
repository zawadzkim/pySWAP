from typing import Self

import chardet
from pydantic import model_validator

from pyswap.core import VALIDATIONRULES
from pyswap.core.basemodel import PySWAPBaseModel


class FileMixin:
    """Saving and readin files.

    Not all classes require to be saved or have read functionality. Therefore,
    it makes sense to move this functionality from the main PySWAPBaseModel
    class to a mixin and use it only on classes that need it.

    Functions:
        save_file: Saves a string to a file.
        read_file: Reads a file from a string.

    """

    @staticmethod
    def save_file(
        string: str,
        fname: str,
        path: str,
        mode: str = "w",
        extension: str | None = None,
        encoding: str = "ascii",
    ) -> str:
        """Saves a string to a file.

        Arguments:
            string: The string to be saved to a file.
            extension: The extension that the file should have (e.g. 'txt',
                'csv', etc.).
            fname: The name of the file.
            path: The path where the file should be saved.
            mode: The mode in which the file should be opened (e.g. 'w' for
                write, 'a' for append, etc.).
            encoding: The encoding to use for the file (default is 'ascii').

        Returns:
            Success message.
        """

        if extension is not None:
            fname = f"{fname}.{extension}"

        with open(f"{path}/{fname}", f"{mode}", encoding=f"{encoding}") as f:
            f.write(string)

        return f"{fname}.{extension} saved successfully."

    @staticmethod
    def read_file(file_path: str) -> str:
        """Open file and detect encoding with chardet.

        Arguments:
            file_path (str): Path to the file to be opened.
        """
        with open(file_path, "rb") as f:
            raw_data = f.read()
        encoding = chardet.detect(raw_data)["encoding"]

        return raw_data.decode(encoding)


class SerializableMixin:
    """Converting a model to a SWAP-formatted string.

    This mixin is supposed to be used on classes that should
    directly serialize to a file and do not contain nested classes.
    Each class that has nested classes inheriting from this mixin
    should have a method utilizing this the functionality here to
    concatenate the files.
    """

    def if_is_union_type(self, field_info):
        """Check if the field type is a Union type.
        
        If it is, look for the json_schema_extra attribute in the field_info
        of the first argument of the Union type. If it is not found, return None.
        """

        field_type = field_info.annotation
        if get_origin(field_type) is Union:
            union_args = get_args(field_type)
            args = get_args(union_args[0])
            # look for the FieldInfo object in the Union type
            field_info = [item for item in args if isinstance(item, FieldInfo)]

            # if the FieldInfo object is not found, return None
            if not field_info:
                return None
            
            # Otherwise, there should be only one FieldInfo object
            return field_info[0].json_schema_extra
        return None

    def is_annotated_exception_type(self, field_name):
        """Check if the attribute type is Table, Arrays, or ObjectList.
        
        If the attribute is a Table, Arrays, or ObjectList, return True. First try
        to assign the json_schema_extra from a Union type. If that fails, assign
        the json_schema_extra from the field_info. If the json_schema_extra is
        None, return False.
        """
        # Every special field will have a FieldInfo object
        field_info = self.model_fields.get(field_name, None)
        if field_info is None:
            return False
        
        json_schema_extra = self.if_is_union_type(field_info) or field_info.json_schema_extra

        if json_schema_extra is None:
            return False
        return json_schema_extra.get("is_annotated_exception_type", False)

    @model_serializer(when_used="json", mode="wrap")
    def serialize_model(self, handler):
        """Get a dictionary of SWAP formatted strings."""
        result = {}
        validated_self = handler(self)
        for field_name, field_value in validated_self.items():
            if self.is_annotated_exception_type(field_name):
                result[field_name] = field_value
            else:
                result[field_name] = f"{field_name.upper()} = {field_value}"
        return result

    def model_string(self, mode: Literal["str", "list"] = "string") -> str | list[str]:
        """Concatenate the formatted strings from dictionsty to one string."""
        dump = self.model_dump(mode="json", exclude_none=True, by_alias=True).values()
        if mode == "list":
            return list(dump)
        else:
            return "\n".join(dump)


class YAMLValidatorMixin:
    """A mixin class that provides YAML-based validation for parameters.
    Methods:
        validate_parameters: Validates parameters against required rules.
        validate_with_yaml: Validates parameters using external YAML rules.
    """

    @staticmethod
    def validate_parameters(switch_name, switch_value, params, rules: dict):
        """Validates parameters against required rules.
        Parameters:
            switch_name (str): The name of the switch (e.g., 'swcf').
            switch_value (Any): The value of the switch (e.g., 1 or 2).
            params (dict): Dictionary of parameters to check.
            rules (dict): Dictionary with validation rules.

        Raises:
            ValueError: If required parameters are missing.
        """

        required_params = rules.get(switch_name, {}).get(switch_value, [])

        if not required_params:
            return  # No rules for this switch value

        missing_params = [
            param for param in required_params if params.get(param) is None
        ]

        if missing_params:
            raise ValueError(
                f"The following parameters are required for {switch_name}={switch_value}: {', '.join(missing_params)}"
            )

    @model_validator(mode="after")
    def validate_with_yaml(self) -> Self:
        """Validates parameters using external YAML rules.

        Returns:
            Self: The instance of the class after validation.
        """
        rules = VALIDATIONRULES.get(self.__class__.__name__, {})

        for switch_name in rules.keys():
            switch_value = getattr(self, switch_name, None)
            if switch_value is not None:  # Only validate if the switch is set
                self.validate_parameters(
                    switch_name, switch_value, self.__dict__, rules
                )
        return self
