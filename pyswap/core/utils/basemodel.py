from pydantic import BaseModel, ConfigDict


class PySWAPBaseModel(BaseModel):

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True
    )

    def model_string(self):
        string = ''
        for attr, value in self.model_dump(mode='json', exclude_none=True).items():
            if attr.startswith('table_'):
                string += value
            else:
                string += f"{attr.upper()} = {value}\n"

        return string
