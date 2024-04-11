from pyswap.core.metadata import Metadata
from pyswap.core.simsettings import SimSettings
from pyswap.plant.createcrop import Crop, CropFile
from pyswap.soilwater.irrigation import Irrigation, FixedIrrigation
from pyswap.atmosphere.meteorology import Meteorology, MeteorologicalData, PenmanMonteith
from pyswap.soilwater.soilmoisture import SoilMoisture
from pyswap.soilwater.surfaceflow import SurfaceFlow
from pyswap.soilwater.evaporation import Evaporation
from pyswap.soilwater.soilprofile import SoilProfile
from pyswap.soilwater.snow import SnowAndFrost
from pyswap.soilwater.richards import RichardsSettings
from pyswap.soilwater.drainage import DrainageFile, LateralDrainage
from pyswap.core.boundary import BottomBoundary
from pyswap.extras.heatflow import HeatFlow
from pyswap.extras.solutetransport import SoluteTransport
from pyswap.core.model import Model
from datetime import date as dt
from pandas import DataFrame

meta = Metadata(author="John Doe",
                institution="University of Somewhere",
                email="john.doe@somewhere.com",
                project="Test",
                swap_ver="4.0")

simset = SimSettings(
    swscre=1,
    swerror=1,
    tstart='2002-01-01',
    tend='2004-12-31',
    nprintday=1,
    swmonth=1,
    period=1,
    swres=0,
    swodat=0,
    outdat=['2002-01-31', '2004-12-31'],
    swyrvar=0,
    datefix='2004-12-31',
    swvap=1,
    swblc=1,
    swsba=1,
    swinc=1,
    swcsv=1,
    swafo=0,
    swaun=0,
    inlist_csv=['rain', 'irrig', 'interc', 'runoff', 'drainage',
                'dstor', 'epot', 'eact', 'tpot', 'tact', 'qbottom', 'gwl'],
    critdevmasbal=0.00001,
    numnodnew=6,
    dznew=[10.0, 10.0, 10.0, 20.0, 30.0, 50.0]
)

pen_mon = PenmanMonteith(
    alt=10.0,
    altw=10.0,
    angstroma=0.25,
    angstromb=0.5,
)

meteo_data = MeteorologicalData()
meteo_data.weather_kmni(station='283')

meteo = Meteorology(
    metfil='283.met',
    lat=52.0,
    swetr=0,
    file_meteo=meteo_data,
    penman_monteith=pen_mon,
    swdivide=1,
    swmetdetail=0,
    nmetdetail=24,
    swetsine=0,
    swrain=0,
    rainfil='wagrain'
)

croprotation = DataFrame({'cropstart': [dt(2002, 5, 1), dt(2003, 5, 10), dt(2004, 1, 1)],
                          'cropend': [dt(2002, 10, 15), dt(2003, 9, 29), dt(2004, 12, 31)],
                          'cropfil': ["'maizes'", "'potatod'", "'grassd'"],
                          'croptype': [1, 2, 3]})

crop_maizes = CropFile(name='maizes', path='./data/maizes.crp')
crop_potatod = CropFile(name='potatod', path='./data/potatod.crp')
crop_grassd = CropFile(name='grassd', path='./data/grassd.crp')

crop = Crop(
    swcrop=1,
    rds=200.0,
    table_croprotation=croprotation,
    cropfiles=[crop_maizes, crop_potatod, crop_grassd]
)

irrig_events = DataFrame({
    'irdate': ['2002-01-05'],
    'irdepth': [5.0],
    'irconc': [1000.0],
    'irtype': [1]}
)

fixed_irrigation = FixedIrrigation(
    swirgfil=0,
    table_irrigevents=irrig_events
)

irrigation = Irrigation(
    swirfix=1,
    fixedirrig=fixed_irrigation,
    schedule=0
)

soilmoisture = SoilMoisture(
    swinco=2,
    gwli=-75.0
)

surfaceflow = SurfaceFlow(
    swpondmx=0,
    pondmx=0.2,
    rsro=0.5,
    rsroexp=1.0,
    swrunon=0
)

evaporation = Evaporation(
    cfevappond=1.25,
    swcfbs=0,
    rsoil=30.0,
    swredu=1,
    cofredbl=0.35,
    rsigni=0.5
)

soil_profile = DataFrame(
    {'ISUBLAY': [1, 2, 3, 4],
     'ISOILLAY': [1, 1, 2, 2],
     'HSUBLAY': [10.0, 20.0, 30.0, 140.0],
     'HCOMP': [1.0, 5.0, 5.0, 10.0],
     'NCOMP': [10, 4, 6, 14]}
)

soil_hydraulic_functions = DataFrame({
    'ORES': [0.01, 0.02],
    'OSAT': [0.42, 0.38],
    'ALFA': [0.0276, 0.0213],
    'NPAR': [1.491, 1.951],
    'KSATFIT': [12.52, 12.68],
    'LEXP': [-1.060, 0.168],
    'ALFAW': [0.0542, 0.0426],
    'H_ENPR': [0.0, 0.0],
    'KSATEXM': [12.52, 12.68],
    'BDENS': [1315.0, 1315.0]
})

soilprofile = SoilProfile(
    swsophy=0,
    table_soilprofile=soil_profile,
    swhyst=0,
    tau=0.2,
    table_soilhydrfunc=soil_hydraulic_functions,
    swmacro=0
)

snow = SnowAndFrost(swsnow=0, swfrost=0)

richards = RichardsSettings(swkmean=1, swkimpl=0)

dranage_file = DrainageFile(
    name='swap', path='./data/swap.dra')

lateral_drainage = LateralDrainage(
    swdra=1,
    drfil='swap',
    drainagefile=dranage_file
)

bottom_boundary = BottomBoundary(
    swbbcfile=0,
    swbotb=6
)

heat = HeatFlow(swhea=0)
solute = SoluteTransport(swsolu=0)

model = Model(
    metadata=meta,
    simsettings=simset,
    meteorology=meteo,
    crop=crop,
    irrigation=irrigation,
    soilmoisture=soilmoisture,
    surfaceflow=surfaceflow,
    evaporation=evaporation,
    soilprofile=soilprofile,
    snowandfrost=snow,
    richards=richards,
    lateraldrainage=lateral_drainage,
    bottomboundary=bottom_boundary,
    heatflow=heat,
    solutetransport=solute
)


def main():
    result = model.run()
    return result


if __name__ == '__main__':
    result = model.run()
