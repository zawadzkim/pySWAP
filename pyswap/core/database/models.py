"""
SQLAlchemy models for the pySWAP database.

Important assumptions:
    1. There is always an initial SWAP model which is saved in the SWAPModel table.
    2. Each SWAPModel belongs to only one project.
    3. Each SWAPModel has one or mode runs which are saved in the ModelRun table.
    4. One ModelRun has exactly one ModelOutput
"""

from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, UniqueConstraint, Table, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import JSON

Base = declarative_base()


data_swaprun_association = Table(
    'data_swaprun_association',
    Base.metadata,
    Column('data_id', Integer, ForeignKey('data.did')),
    Column('swaprun_mid', String(50)),
    Column('swaprun_rid', String(50)),
)


class Data(Base):
    """Stores data files like meteo data or crop data."""

    __tablename__ = 'data'

    did = Column(Integer, primary_key=True)
    fname = Column(String(50), nullable=False, unique=True)
    datafile = Column(LargeBinary)
    swapruns = relationship(
        'SWAPRun', secondary=data_swaprun_association, back_populates='data')


class SWAPRun(Base):
    """This model stores sections of the .swp file"""

    __tablename__ = 'swapmodel'

    mid = Column(String(50), primary_key=True)
    rid = Column(String(50), default='initial', primary_key=True)
    swp = Column(LargeBinary, nullable=True)
    data = relationship(
        'Data', secondary=data_swaprun_association, back_populates='swapruns')
    result = Column(LargeBinary, nullable=True)

    __table_args__ = (UniqueConstraint('mid', 'rid', name='uq_model_run'),)


def test_insert_and_retrieve(session):
    # Create Data objects
    data1 = Data(fname='data1', datafile=b'datafile1')
    data2 = Data(fname='data2', datafile=b'datafile2')
    data3 = Data(fname='data3', datafile=b'datafile3')

    # Create SWAPRun objects
    swaprun1 = SWAPRun(mid='model1', rid='1', swp=b'swp1')
    swaprun2 = SWAPRun(mid='model1', rid='2', swp=b'swp2')
    swaprun3 = SWAPRun(mid='model2', rid='1', swp=b'swp3')

    # Associate Data objects with SWAPRun objects
    swaprun1.data = [data1, data2]
    swaprun2.data = [data2, data3]
    swaprun3.data = [data3]

    # Add objects to the session
    session.add_all([data1, data2, data3, swaprun1, swaprun2, swaprun3])
    session.commit()

    # Retrieve all SWAPRun objects along with related Data objects
    all_swapruns = session.query(SWAPRun).options(
        relationship(Data, secondary=data_swaprun_association)).all()

    # Print retrieved objects
    for swaprun in all_swapruns:
        print("SWAPRun:", swaprun.mid, swaprun.rid)
        for data in swaprun.data:
            print("  Data:", data.fname)
