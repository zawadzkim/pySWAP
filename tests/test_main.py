from pandas import DataFrame

from pySWAP.crop import Crop
from pySWAP.drainage import Drainage
from pySWAP.meteo import Meteo
from utils_database.connection import DatabaseConnection
from pySWAP.metadata import Metadata
from pySWAP.swpsetup import SWAPSetup
from pySWAP.swaprun import SWAPRun, SWAPResult


db = DatabaseConnection('test_5.db')

metadata = Metadata(author='Someone',
                    institution='University of Somewhere',
                    email='some_email@somewhere.com',
                    project_name='test_1',
                    swap_ver='4.0.0',
                    comment='This is a test project')

ml1 = SWAPSetup(connection=db,
                metadata=metadata)

ml1.set_environment()
start = '2002-01-01'
end = '2004-12-31'

ml1.set_simulation_period(tstart=start,
                          tend=end)
datefix = '21 11'

ml1.set_output_dates(nprintday=1,
                     swmonth=True,
                     swyrvar=False,
                     datefix=datefix)
ml1.set_output_files()
rds = 200.0

# There is a brute force solution here to encluse the cropname and cropfile
# in single quotes. It is not elegant, but it works.
croprotation = DataFrame({'CROPSTART': ['2002-05-01', '2003-05-10', '2004-01-01'],
                          # in the originl file it was ['01-may-02']
                          'CROPEND': ['2002-10-15', '2003-09-29', '2004-12-31'],
                          'CROPNAME': ["'maize'", "'potato'", "'grass'"],
                          'CROPFIL': ["'maizes'", "'potatod'", "'grassd'"],
                          'CROPTYPE': [1, 2, 3], })

# prepare the crop files
maize_path = r"C:\Users\zawad\PycharmProjects\pySWAP_django\djangoSWAP\setup_model\pySWAP\pySWAP\data\.crp\maizes.crp"
potato_path = r"C:\Users\zawad\PycharmProjects\pySWAP_django\djangoSWAP\setup_model\pySWAP\pySWAP\data\.crp\potatod.crp"
grass_path = r"C:\Users\zawad\PycharmProjects\pySWAP_django\djangoSWAP\setup_model\pySWAP\pySWAP\data\.crp\grassd.crp"
file_names = ['maizes', 'potatod', 'grassd']

crop = Crop(file_paths=[maize_path, potato_path, grass_path],
            file_names=file_names)

ml1.set_crop(swcrop=True,
             croprotation=croprotation,
             rds=rds,
             crop=crop)

irigevents = DataFrame({'IRDATE': ['2002-01-05'],
                        'IRDEPTH': [5.0],
                        'IRCONC': [1000.0],
                        'IRTYPE': [1]})

ml1.set_irrigation(swirfix=True,
                   schedule=False,
                   swirgfil=False,
                   irigevents=irigevents)

csv_path = r"C:\Users\zawad\PycharmProjects\pySWAP_django\djangoSWAP\setup_model\pySWAP\pySWAP\data" \
           r"\daily_basic_weather.csv"
met1 = Meteo(metadata)  # create a meteo instance with given header

met1.load_from_csv(csv_path=csv_path,
                   station='283',
                   station_lon=52.0,
                   station_lat=52.0,
                   station_alt=60.5)

ml1.set_meteo(swetr=False,
              meteo_data=met1,
              altw=10.0,
              angstroma=0.25,
              angstromb=0.5,
              swdivide=True,
              swmetdetail=False)  # set meteo data and store the csv file in the main model instance

ml1.set_init_soil_moisture(swinco=2,
                           gwli=float(75))

ml1.set_surface_flow(swpondmx=0,
                     swrunon=False,
                     rsro=0.5,
                     rsroexp=1.0,
                     pondmx=0.2, )

ml1.set_soil_evap(cfevappond=1.25,
                  swcfbs=False,
                  swredu=1,
                  rsoil=30.0,
                  rsigni=0.5,
                  cofredbl=0.35, )

soilprofile = DataFrame({'ISUBLAY': [1, 2, 3, 4],
                         'ISOILLAY': [1, 1, 2, 2],
                         'HSUBLAY': [10.0, 20.0, 30.0, 140.0],
                         'HCOMP': [1.0, 5.0, 5.0, 10.0],
                         'NCOMP': [10, 4, 6, 14]})

ml1.set_soil_profile(soilprofile=soilprofile)

soilhydrfunc = DataFrame({'ISOILLAY1': [1, 2],
                          'ORES': [0.01, 0.02],
                          'OSAT': [0.42, 0.38],
                          'ALFA': [0.0276, 0.0213],
                          'NPAR': [1.491, 1.951],
                          'KSATFIT': [12.52, 12.68],
                          'LEXP': [-1.060, 0.168],
                          'ALFAW': [0.0542, 0.0426],
                          'H_ENPR': [0.0, 0.0],
                          'KSATEXM': [12.52, 12.68],
                          'BDENS': [1315.0, 1315.0]})

# # Optional parameters:
# filenamesophy = 'topsoil_sand_b2.csv' 'subsoil_sand_o2.csv'
# tau = 0.2

ml1.set_soil_parameters(swsophy=False,
                        swhyst=0,
                        swmacro=False,
                        soilhydrfunc=soilhydrfunc, )

ml1.set_snow_frost(swsnow=False,
                   swfrost=False, )

ml1.set_richards_params(dtmin=0.000001,
                        dtmax=0.04,
                        gwlconv=100.0,
                        critdevh1cp=0.01,
                        critdevh2cp=0.1,
                        critdevponddt=0.0001,
                        maxit=30,
                        maxbacktr=3,
                        swkmean=1,
                        swkimpl=False, )

dra_path = r"C:\Users\zawad\PycharmProjects\pySWAP_django\djangoSWAP\setup_model\pySWAP\pySWAP\data\swap.dra"
dra = Drainage(dra_path)

ml1.set_bottom_boundary(swbbcfile=False,
                        swbotb=6)

ml1.set_heatflow(swhea=False)

ml1.set_drainage(swdra=False,
                 drainage=dra, )

ml1.set_solute_settings(swsolu=False)

ml1.save()

ml_run1 = SWAPRun(ml1)
ml_run1.get_model_by_name()

ml_run1.include_iteration_changes()

ml_run1.pop_nons()
ml_run1.bool_to_int()
ml_run1.decode_meteo()
compiled = ml_run1.compile_swp_file()

ml_run1.run()
result = SWAPResult(db)
output = result.get_output_by_model_and_iteration(connection=db,
                                         model_name='test_1',
                                         iteration_number=1)

for i in output:
    print(i.data)

# Until the line above there is no  issues so far.