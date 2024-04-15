# from pyswap.core.database.connection import DatabaseConnection
# from sqlalchemy.orm import relationship
# from pyswap.core.database.models import Data, SWAPRun, data_swaprun_association


# def test_insert_and_retrieve(session):
#     # Create Data objects
#     data1 = Data(fname='data1', datafile=b'datafile1')
#     data2 = Data(fname='data2', datafile=b'datafile2')
#     data3 = Data(fname='data3', datafile=b'datafile3')

#     # Create SWAPRun objects
#     swaprun1 = SWAPRun(mid='model1', rid='1', swp=b'swp1')
#     swaprun2 = SWAPRun(mid='model1', rid='2', swp=b'swp2')
#     swaprun3 = SWAPRun(mid='model2', rid='1', swp=b'swp3')

#     # Associate Data objects with SWAPRun objects
#     swaprun1.data = [data1, data2]
#     swaprun2.data = [data2, data3]
#     swaprun3.data = [data3]

#     # Add objects to the session
#     session.add_all([data1, data2, data3, swaprun1, swaprun2, swaprun3])
#     session.commit()

#     # Retrieve all SWAPRun objects along with related Data objects
#     all_swapruns = session.query(SWAPRun).options(
#         relationship(Data, secondary=data_swaprun_association)).all()

#     # Print retrieved objects
#     for swaprun in all_swapruns:
#         print("SWAPRun:", swaprun.mid, swaprun.rid)
#         for data in swaprun.data:
#             print("  Data:", data.fname)


# conn = DatabaseConnection('./test.db')
# test_insert_and_retrieve(conn.session)
