from sqlalchemy.orm import state, session

from models import ModelRun, SWAPModel
from sqlalchemy import event, text, func, bindparam, select, insert
from sqlalchemy.orm import Session


@event.listens_for(ModelRun, 'before_insert')
def auto_set_iteration(mapper, connection, target):

    query = select(func.max(ModelRun.iteration)).where(ModelRun.model_id == bindparam('model_id')).\
        params(model_id=target.model_id)

    result = connection.execute(query).scalar()

    max_iteration = result if result is not None else 0
    target.iteration = max_iteration + 1


# This would be a more elegant solution, but it doesn't work. There might be a something wrong with the way
# I use session.

# @event.listens_for(SWAPModel, 'after_insert')
# def auto_create_iteration(mapper, connection, target):
#     # Prepare the insert statement
#     stmt = insert(ModelIteration).values(
#         model_id=target.id,
#         iteration=1,
#         swp_change={},
#         drainage_change={},
#         crop_change={},
#         met_change=None
#     )
#
#     # Execute the statement
#     connection.execute(stmt)
