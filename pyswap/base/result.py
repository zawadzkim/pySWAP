from dataclasses import dataclass

from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from pySWAP.utils_database.connection import DatabaseConnection
from pySWAP.utils_database.models import ModelOutput, SWAPModel, ModelIteration


@dataclass
class SWAPResult:

    connection: DatabaseConnection = None

    from sqlalchemy.orm import joinedload

    def get_output_by_model_and_iteration(self, connection: DatabaseConnection, model_name: str, iteration_number: int):
        # Join across the relationships and filter based on the model name and iteration number
        outputs = connection.session.query(ModelOutput).join(
            ModelIteration, ModelOutput.iteration_id == ModelIteration.id
        ).join(
            SWAPModel, ModelIteration.model_id == SWAPModel.id
        ).filter(
            SWAPModel.name == model_name, ModelIteration.iteration == iteration_number
        ).all()

        # Return the outputs
        return outputs

