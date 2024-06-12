from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from .serializers import quote_string
from .files import save_file


class PySWAPBaseModel(BaseModel):
    """Base class for PySWAP models.

    Attributes:
        model_config (ConfigDict): Overriding Pydantic model configuration.

    Methods:
        save_element: Saves model element to a file.
        model_string: Returns a custom model string representation that matches the requirements of .swp file.
        _concat_sections: Concatenate a string from individual sections.
        model_string: Returns a custom model string representation that matches the requirements of .swp file.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        extra='forbid'
    )

    @staticmethod
    def save_element(string: str, path: str, filename: str, extension: str | None = None) -> str:
        """Saves model element to a file.

        Args:
            string (str): String to be saved.
            path (str): Path to the file.
            filename (str): File name.

        Returns:
            str: Success message.
        """
        save_file(
            string=string,
            fname=filename,
            extension=extension,
            path=path
        )
        return f'{filename}.{extension} saved successfully.'

    def model_string(self) -> str:
        """Returns a custom model string representation that matches the requirements of .swp file.

        Note:
            If values are simple types, they are formatted as 'ATTR = VALUE'. If the valies are
            tables (in pySWAP pd.DataFrame are used), they are formatted simply as 'TABLE_VALUE'. Additionally,
            a custom serializer (pyswap.core.utils.serializers.quote_string) is used to quote strings.

        Returns:
            str: Custom model string representation.
        """
        string = ''

        def formatter(attr, value, string):
            if attr.startswith('table_') or attr.startswith('list_'):
                return string + value
            else:
                return string + f'{attr.upper()} = {quote_string(value)}\n'

        for attr, value in self.model_dump(
                mode='json', exclude_none=True).items():
            if isinstance(value, dict):
                for k, v in value.items():
                    string = formatter(k, v, string)
            else:
                string = formatter(attr, value, string)

        return string

    def _concat_sections(self) -> str:
        """Concatenate a string from individual sections.

        This method is meant to be used on models that collect other
        models, like DraFile, or Model.
        """

        string = ''
        for k, v in dict(self).items():
            if v is None or isinstance(v, str):
                continue
            string += v.model_string()
        return string
