# mypy: disable-error-code="attr-defined, no-any-return, index"
# attr-defined error showed in when the .update method was called in the wofost mixin.
# the easiest way to fix it would be to just check for the PySWAPBaseModel
# instance, but that would create circular import issue and I did not want to
# play with that. It's not a priority to fix for now.
# no-any-return error was raised in the get_origin method. This was not a
# priority to fix. Same as the index error; it complained that the FieldInfo
# object is not indexable, but in fact in this case it should be, because of the
# Optional or Annotated types.

"""Reusable mixins enhancing functionality of specific PySWAPBaseModel.

To keep the main PySWAPBaseModel class and the components library clean and
focused, mixins are used to add additional functionality to the classes that
need it. The concept of the mixins was inspired by the Django framework and it
really helps to keep the code clean and organized.

Should more functionality be needed in the future for one or more classes, it
should be implemented as a mixin and then inherited by the classes that need it.

Classes:

    FileMixin: Custom saving functionality for models that need file I/O.
    SerializableMixin: Converting a model to a SWAP-formatted string.
    YAMLValidatorMixin: Validating parameters using external YAML rules.
    WOFOSTUpdateMixin: Interface for the WOFOST crop parameters database for
        pySWAP.
"""

from pathlib import Path
from typing import Any, Literal, Self, Union, get_args, get_origin

from pydantic import BaseModel, PrivateAttr, model_serializer, model_validator
from pydantic.fields import FieldInfo

from pyswap.core.defaults import VALIDATIONRULES
from pyswap.core.io.io_yaml import load_yaml
from pyswap.core.io.processors import TableProcessor
from pyswap.log import logging

logger = logging.getLogger(__name__)


class FileMixin:
    """Custom saving functionality for models that need file I/O.

    !!! note:

        The _extension attribute should be set in the class that inherits
        this mixin. It is recommended that pydantic's PrivateAttr is used to
        hide this attribute from the user.

    Methods:
        save_file: Saves a string to a file.
    """

    def save_file(
        self,
        string: str,
        fname: str,
        path: Path,
    ) -> None:
        """Saves a string to a file.

        The extension should now be provided in each class inheriting this
        mixin as a private attribute.

        Parameters:
            string: The string to be saved to a file.
            fname: The name of the file.
            path: The path where the file should be saved.
        """

        if not hasattr(self, "_extension"):
            msg = "The _extension attribute should be set."
            raise AttributeError(msg)

        ext = self._extension
        fname = f"{fname}.{ext}" if ext else fname

        with open(f"{path}/{fname}", "w", encoding="ascii") as f:
            f.write(string)

        logger.info(f"{fname} saved successfully.")

        return None


class SerializableMixin(BaseModel):
    """Converting a model to a SWAP-formatted string.

    This mixin is only inherited by classes that directly serialize to a
    SWAP-formatted string. The assumptions are that the inheriting classes:

    - do not contain nested classes.
    - if the class contains nested classes it should either use Subsection field
        types or override the `model_string()` method.

    Methods:
        if_is_union_type: Check if the field type is a Union type.
        is_annotated_exception_type: Check if the attribute type is Table,
            Arrays, or ObjectList.
        serialize_model: Override the default serialization method.
        model_string: Concatenate the formatted strings from dictionary to
            one string.
    """

    def if_is_union_type(self, field_info: FieldInfo) -> dict | None:
        """Check if the field type is a Union type.

        If it is, look for the json_schema_extra attribute in the field_info
        of the first argument of the Union type. If it is not found, return
        None. It was necessary in cases of, for example, optional classes like
        Union[Table, None].

        Parameters:
            field_info (FieldInfo): The FieldInfo object of the field.
        """

        field_type = field_info.annotation

        if get_origin(field_type) is Union:
            union_args = get_args(field_type)
            args = get_args(union_args[0])

            field_info = [item for item in args if isinstance(item, FieldInfo)]

            if not field_info:
                return None

            # Only return the json_schema_extra attribute. This is used in some
            # cases to pass addotional information from the serializer in
            # pyswap.core.fields module to the model_dump.
            return field_info[0].json_schema_extra
        return None

    def is_annotated_exception_type(self, field_name: str) -> bool:
        """Check if the attribute type is Table, Arrays, or ObjectList.

        For Table, Arrays, and ObjectList types True is returned, ensuring a
        separate serialization path.

        First try to assign the json_schema_extra from a Union type. If that
        fails, assign the json_schema_extra from the field_info. If the
        json_schema_extra is None, return False.
        """
        # Every special field will have a FieldInfo object
        field_info = self.model_fields.get(field_name, None)

        if field_info is None:
            return False

        json_schema_extra = (
            self.if_is_union_type(field_info) or field_info.json_schema_extra
        )

        if json_schema_extra is None:
            return False

        return json_schema_extra.get("is_annotated_exception_type", False)

    @model_serializer(when_used="json", mode="wrap")
    def serialize_model(self, handler: Any):
        """Override the default serialization method.

        In the intermediate step, a dictionary is created with SWAP formatted
        strings.
        """
        result = {}
        validated_self = handler(self)
        for field_name, field_value in validated_self.items():
            if self.is_annotated_exception_type(field_name):
                result[field_name] = field_value
            else:
                result[field_name] = f"{field_name.upper()} = {field_value}"
        return result

    def model_string(
        self, mode: Literal["str", "list"] = "string", **kwargs
    ) -> str | list[str]:
        """Concatenate the formatted strings from dictionary to one string.


        !!! note:
            By alias is True, because in some cases, particularily in the case
            of CropSettings, the WOFOST names of parameters in the database were
            different from those used in SWAP. This allows those parameters to
            be properly matched, yet serialized properly in SWAP input files.

        Parameters:
            mode (Literal["str", "list]): The output format.
            kwargs (dict): Additional keyword arguments passed to `model_dump()`.
        """
        dump = self.model_dump(
            mode="json", exclude_none=True, by_alias=True, **kwargs
        ).values()

        if mode == "list":
            return list(dump)
        else:
            return "\n".join(dump)


class YAMLValidatorMixin(BaseModel):
    """A mixin class that provides YAML-based validation for models.

    Initially, pySWAP had model serializers on each model component class which
    had a number of assertions to validate the parameters (i.e., require
    parameters rlwtb and wrtmax if swrd = 3). This created chaos
    in the code, and since none of it was used by inspection tools anyways, it
    was decided to leave the validation logic in the code and move the rules to
    a separate YAML file.

    Methods:
        validate_parameters: Validate parameters against required rules.
        validate_with_yaml: Pydantic validator executing validation logic.
    """

    _validation: bool = PrivateAttr(default=False)

    @staticmethod
    def validate_parameters(
        switch_name: str, switch_value: str, params: dict, rules: dict
    ):
        """Validate parameters against required rules.

        This method reads the rules for the model from the YAML file and checks
        if the required parameters are present. If not, it raises a ValueError.

        ```yaml
        SaltStress: # <--- Model name
            swsalinity:  # <--- Switch name (switch_name)
                1:  # <--- Switch value (switch_value)
                - saltmax  # <---| Required parameters
                - saltslope  # <--|
                2:
                - salthead
        ```

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
            msg = f"The following parameters are required for {switch_name}={switch_value}: {', '.join(missing_params)}"
            raise ValueError(msg)

    @model_validator(mode="after")
    def validate_with_yaml(self) -> Self:
        """Pydantic validator executing validation logic.

        All validators defined on a model run on model instantiation. This
        method makes sure that YAML validation is postponed until the
        _validation parameter (required on all classes inheriting this mixin) is
        set to True. This state is done when all the required parameters are
        presumed to be set, e.g., when the user tries to run the model.
        """

        if not self._validation:
            return self

        rules = VALIDATIONRULES.get(self.__class__.__name__, {})

        for switch_name in rules:
            switch_value = getattr(self, switch_name, None)
            if switch_value is not None:  # Only validate if the switch is set
                self.validate_parameters(
                    switch_name, switch_value, self.__dict__, rules
                )

        self._validation = False
        return self


class YAMLUpdateMixin:
    """Interface for the WOFOST crop parameters database for pySWAP.

    This mixin should be inherited by classes that share parameters with the
    WOFOST crop database.
    """

    def update_from_wofost(self) -> None:
        """Update the model with the WOFOST variety settings."""

        # parameters attribute returns a dictionary with the key-value pairs and
        # tables as list of lists. Before updating, the tables should be
        # created.
        if not hasattr(self, "wofost_variety"):
            msg = "The model does not have the WOFOST variety settings."
            raise AttributeError(msg)

        variety_params = self.wofost_variety.parameters
        logger.debug(f"Updating from WOFOST variety parameters: {variety_params}")

        # Create a copy to work with
        params_copy = variety_params.copy()

        tp = TableProcessor()
        for name, value in variety_params.items():
            if isinstance(value, list) and value and isinstance(value[0], list):
                # This is an array parameter - try to process it
                processed = tp.process("array", data=value, columns=name)
                if processed is not None:
                    # Replace the raw array with the processed dataframe
                    params_copy.update(processed)
                    logger.debug(f"Processed array parameter: {name}")
                else:
                    # Remove unmatched array parameters
                    params_copy.pop(name, None)
                    logger.warning(
                        f"Failed to process array parameter: {name}, removing from update"
                    )

        self.update(params_copy, inplace=True)

    def update_from_yaml(self, yaml_path: str | Path) -> None:
        """Update the model with parameters from a YAML file.

        Parameters:
            yaml_path (str | Path): Path to the YAML file containing parameters.
        """

        yaml_path = Path(yaml_path)
        if not yaml_path.exists():
            msg = f"YAML file not found: {yaml_path}"
            raise FileNotFoundError(msg)

        yaml_content = load_yaml(yaml_path)
        logger.debug(f"Loaded YAML content from: {yaml_path}")

        # Extract parameters from the YAML structure
        # Assuming the YAML has a structure like: CropParameters -> SWAPInput -> parameters
        params = None
        if (
            "CropParameters" in yaml_content
            and "SWAPInput" in yaml_content["CropParameters"]
        ):
            params = yaml_content["CropParameters"]["SWAPInput"]
        elif isinstance(yaml_content, dict):
            # If it's a flat dictionary, use it directly
            params = yaml_content
        else:
            msg = f"Could not find parameters in YAML structure: {yaml_content.keys()}"
            raise ValueError(msg)

        logger.debug(f"Extracted parameters from YAML: {list(params.keys())}")

        # Create a copy to work with
        params_copy = params.copy()

        tp = TableProcessor()
        for name, value in params.items():
            if isinstance(value, dict) and len(value) == 2:
                # This looks like a table with two columns (e.g., DNR/CH, TAVD/TMPF)
                # Convert dict format to list of lists format expected by TableProcessor
                keys = list(value.keys())
                if len(keys) == 2:
                    array_data = [
                        [x, y]
                        for x, y in zip(value[keys[0]], value[keys[1]], strict=True)
                    ]
                    processed = tp.process("array", data=array_data, columns=name)
                    if processed is not None:
                        # Replace the raw dict with the processed dataframe
                        params_copy.update(processed)
                        logger.debug(f"Processed table parameter from YAML: {name}")
                    else:
                        # Remove unmatched table parameters
                        params_copy.pop(name, None)
                        logger.warning(
                            f"Failed to process table parameter from YAML: {name}, removing from update"
                        )
            elif isinstance(value, list) and value and isinstance(value[0], list):
                # This is an array parameter in list of lists format
                processed = tp.process("array", data=value, columns=name)
                if processed is not None:
                    # Replace the raw array with the processed dataframe
                    params_copy.update(processed)
                    logger.debug(f"Processed array parameter from YAML: {name}")
                else:
                    # Remove unmatched array parameters
                    params_copy.pop(name, None)
                    logger.warning(
                        f"Failed to process array parameter from YAML: {name}, removing from update"
                    )
            # Scalar parameters are left as-is

        self.update(params_copy, inplace=True)
