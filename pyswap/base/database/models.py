"""
This script holds SQLalchemy models for the database that are compatible with the Django models.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import JSON

Base = declarative_base()


class SWAPModel(Base):
    __tablename__ = 'swap_models'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    swp = Column(JSON, nullable=True)
    drainage = Column(JSON, nullable=True)
    crop = Column(JSON, nullable=True)
    met = Column(LargeBinary, nullable=True)

    iterations = relationship("ModelIteration", back_populates="model")

    def __repr__(self):
        return self.name


class ModelIteration(Base):
    __tablename__ = 'model_iterations'

    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('swap_models.id'))
    iteration = Column(Integer)
    swp_change = Column(JSON, nullable=True)
    drainage_change = Column(JSON, nullable=True)
    crop_change = Column(JSON, nullable=True)
    met_change = Column(LargeBinary, nullable=True)

    model = relationship("SWAPModel", back_populates="iterations")
    outputs = relationship("ModelOutput", back_populates="iteration")

    def __repr__(self):
        return f"{self.model.name}.{self.iteration}"


class ModelOutput(Base):
    __tablename__ = 'model_outputs'

    id = Column(Integer, primary_key=True)
    iteration_id = Column(Integer, ForeignKey('model_iterations.id'))
    file_name = Column(String(50))
    file_type = Column(String(5))
    data = Column(LargeBinary)

    iteration = relationship("ModelIteration", back_populates="outputs")

    __table_args__ = (UniqueConstraint('file_name', 'file_type', name='unique_constraint_name'),)

    def __repr__(self):
        return f"{self.iteration.model.name}.{self.iteration.iteration}.{self.file_name}"

