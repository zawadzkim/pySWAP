from pydantic import BaseModel, ConfigDict
from .serializers import quote_string


class PySWAPBaseModel(BaseModel):
    """Base class for PySWAP models.

    Attrs:
        model_config (ConfigDict): Overriding Pydantic model configuration.

    Props:
        exclude (set | None): Exclude attributes from model dump.
        include (set | None): Include attributes from model dump.

    Methods:
        model_string: Returns a custom model string representation that matches the requirements of .swp file.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        extra='forbid'
    )

    @property
    def exclude(self) -> set | None:
        return None

    @property
    def include(self) -> set | None:
        return None

    def model_string(self):
        """Returns a custom model string representation that matches the requirements of .swp file.

        If values are simple types, they are formatted as 'ATTR = VALUE\n'. If the valies are
        tables (in pySWAP pd.DataFrame are used), they are formatted simply as 'TABLE_VALUE'. Additionally,
        a custom serializer (pyswap.core.utils.serializers.quote_string) is used to quote strings.

        Returns:
            str: Custom model string representation.
        """
        string = ''

        def formatter(attr, value, string):
            if attr.startswith('table_'):
                return string + value
            else:
                return string + f'{attr.upper()} = {quote_string(value)}\n'

        for attr, value in self.model_dump(
                mode='json', exclude_none=True, exclude=self.exclude, include=self.include).items():
            if isinstance(value, dict):
                for k, v in value.items():
                    string = formatter(k, v, string)
            else:
                string = formatter(attr, value, string)

        return string
