from pydantic import BaseModel, ConfigDict


class PySWAPBaseModel(BaseModel):

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
        string = ''

        def formatter(attr, value, string):
            if attr.startswith('table_'):
                return string + value
            else:
                return string + f"{attr.upper()} = {value}\n"

        for attr, value in self.model_dump(
                mode='json', exclude_none=True, exclude=self.exclude, include=self.include).items():
            if isinstance(value, dict):
                for k, v in value.items():
                    string = formatter(k, v, string)
            else:
                string = formatter(attr, value, string)

        return string
