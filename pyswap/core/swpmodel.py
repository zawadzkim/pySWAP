from .metadata import Metadata
from .meteo import Meteo
import inspect
from .crop import Crop
from .drainage import Drainage
import pandas as pd
from ...utils.utils import open_file, list_to_string, save_file
from pandas import DataFrame
from ...utils import exeptions as exc
from dataclasses import dataclass, field

# External imports
from pathlib import Path
from datetime import datetime as dt

"""
TODO: Consider the parameter estimation. Make it easy to update a subset of parameters with a dictionary from spotpy
TODO: Only call run_swap() method after the update of the dictionary in subsequent iterations of the model.
TODO: save the results in a way they are compatiible with the observations (consider there will be less of obs compared to sim)
TODO: mind all the parameters that are associated with soil layers.
TODO: let's skip the hysteresis for now. Changing crop management and soil water properties.
TODO: read more about the boundary conditions in SWAP
"""


def swp_file_dict():
    return {
        'header': {'params': {}, 'tables': {}},
        'general': {'params': {}, 'tables': {}},
        'meteo': {'params': {}, 'tables': {}},
        'crop': {'params': {}, 'tables': {}},
        'irrigation': {'params': {}, 'tables': {}},
        'soil_water': {'params': {}, 'tables': {}},
        'drainage': {'params': {}, 'tables': {}},
        'bott_bound': {'params': {}, 'tables': {}},
        'heat_flow': {'params': {}, 'tables': {}},
        'solute': {'params': {}, 'tables': {}},
    }


@dataclass()
class Model:

    """
    The main parent class. Stores information used throughout child classes and child classes' instances.

    To instantiate this class, project name, swap version and author's details are needed. That information is used
    in child classes. Furthermore, some parameters of the MlSetup class are dedicated to store instances of child
    classes. This approach was chosen to simplify working on multiple models at the same time, improving integrity of
    models' parameters.
    """

    metadata: Metadata = field(repr=False)
    swp_file: dict = field(default_factory=swp_file_dict, repr=False)
    meteo: Meteo = field(default=None, repr=False)
    crop: Crop = field(default=None, repr=False)
    drainge: Drainage = field(default=None, repr=False)

    def __repr__(self):
        return f'SwapModel({self.metadata.project_name}, ' \
               f'swap_ver={self.metadata.swap_ver}, ' \
               f'author={self.metadata.author})'

    def __post_init__(self):

        self._set_header()

    def get_args_dict(self,
                      locals_dict: dict) -> dict:

        # Get the calling method from the call stack
        calling_frame = inspect.stack()[1]
        calling_method = calling_frame.function

        # Get the class of the calling method
        calling_class = self.__class__

        # Get the method signature and parameters
        signature = inspect.signature(getattr(calling_class, calling_method))
        parameters = signature.parameters

        # Filter the locals_dict to only include the method parameters
        filtered_locals = {key: locals_dict[key] for key in parameters}

        # Create dictionaries for params and tables
        excluded_types = [DataFrame, Meteo, Crop, Drainage]
        params = {key.upper(): value for key, value in filtered_locals.items() if
                  not any(isinstance(value, t) for t in excluded_types)}
        tables = {key.upper(): value for key, value in filtered_locals.items()
                  if isinstance(value, pd.DataFrame)}

        params.pop('SELF', None)
        tables.pop('SELF', None)

        return {'params': params, 'tables': tables}

    def update_parameters(self,
                          params: dict,
                          section: str) -> None:

        self.swp_file[section]['params'].update(
            {k: v for k, v in params['params'].items() if v is not None})

    def update_tables(self,
                      tables: dict,
                      section: str) -> None:

        self.swp_file[section]['tables'].update(
            {k: v for k, v in tables['tables'].items() if v is not None})

    def _set_header(self) -> None:
        """
        Sets the header section of a SWAP file.

        This method sets the author, institution, email, project name, SWAP version, and comment for a SWAP file.
        It also updates the dictionary that represents the .swp file with the corresponding values. _set_header() is
        called within the post_init method.

        Args:
            head (Metadata): A Header object that contains the metadata for the SWAP file.
        Returns:
            None.
        """

        # The keys below correspond to the tags in .swp file.
        heder_params = {'params': {'PROJECT': self.metadata.project_name,
                                   'FILENAME': self.metadata.project_name + '.swp',
                                   'SWAPVER': self.metadata.swap_ver,
                                   'TIMESTAMP': dt.now().strftime("%Y-%m-%d %H:%M:%S"),
                                   'AUTHOR': self.metadata.author,
                                   'INSTITUTION': self.metadata.institution,
                                   'EMAIL': self.metadata.email,
                                   'COMMENT': self.metadata.comment}}

        self.update_parameters(heder_params, 'general')

    def print_section_params(self,
                             section: str) -> None:
        """
        Prints settings of a specified section of the .swb file.

        Args:
            section (str): Name of the section in the .swp file whose settings are to be printed.

        Returns:
            None
        """

        for tag, value in self.swp_file[section]['params'].items():
            print(f"{tag.upper():20} = {value}")

        for tag, value in self.swp_file[section]['tables'].items():
            print(value)

    def set_environment(self,
                        pathwork: str = '.\\',
                        pathatm: str = '.\\',
                        pathcrop: str = '.\\',
                        pathdrain: str = '.\\',
                        swscre: int = 0,
                        swerror: bool = False) -> None:
        """
        Defines working environment and paths to atmospheric, crop and drainage data files.

        Args:

            pathwork (str): current working environment (default is '.\\').
            pathatm (str): file containing weather data (default is '.\\').
            pathcrop (str): file containing info about crops (default is '.\\').
            pathdrain (str): file containing info about drainage (default is '.\\').

        Returns:
            None

        Raises:
            None

        Sets the path information into the 'general' section of the swp_file dictionary,
        replacing the corresponding tags in the 'general' section's string.

        """

        self.update_parameters(self.get_args_dict(locals()), 'general')

    def set_simulation_period(self,
                              start: str,
                              end: str) -> None:
        """
        Sets the simulation period of the model.

        Args:
            start (str): The beginning of the simulation in YYYY-MM-DD format.
            end (str): The end of the simulation in YYYY-MM-DD format.

        Returns:
            None

        Raises:
            None

        Updates the '{TSTART}' and '{TEAND}' tags in the 'general' section of the swp_file dictionary with the provided
        start and end dates, and calls the 'update_section' method with the 'general' section to reflect the changes.
        """

        self.update_parameters(self.get_args_dict(locals()), 'general')

    def set_output_dates(self,
                         nprintday: int,  # Always provide
                         swmonth: bool,  # Always provide
                         swyrvar: bool,  # Always provide
                         period: int | None = None,
                         swres: bool | None = None,
                         swodat: bool | None = None,
                         outdatin: list | None = None,
                         datefix: str | None = None,
                         outdat: list | None = None) -> None:
        """
        Set the dates or frequency of the model's output.

        Args:
            nprintday (int): range 1-1440. Number of output times during a day (default is 1).
            swmonth (bool): Output state variables and fluxes each month (default is True).
            period (int): range 0-366, 0 = ignore. Only if swmonth = 0. Fixed output interval (default is 1).
            swres (bool): Only if swmonth = 0. Reset output interval counter each year (default is False).
            swodat (bool): Only if swmonth = 0. Extra output dates are given in a table (default is False).
            outdatin (list): format 'YYYY-MM-DD'. Only if swodat = True. Specify dates in an ASCII table
                             (Default is ['2022-01-01', '2022-06-01']).
            swyrvar (bool): Output times for overall water and solute balances in *.BAL and *.BLC file
                            at different dates each year (default is False).
            datefix (str): format 'dd mm'. Only if swyrvar = False. Specify a fixed date (Default is '21 11').
            outdat (list): format 'YYYY-MM-DD'. Only if swyrvar = True. Specify dates in an ASCII table
                           (Default is ['2022-01-01', '2022-06-01']).

        Notes:
            The for all 'sw%' parameters ('switches'), the model require integer values of 0 or 1. In Python, it is more
            intuitive to use bool values instead. Therefore, boolean inputs are automatically converted to int.

            The essential parameters are nprintday and swmonth. The rest is required depending on the further settings.

        Returns:
            None
        """

        # Error handling
        exc.check_range(nprintday, 1, 1440, left='closed', right='open')
        exc.check_type(nprintday, int)

        if not swmonth:

            if period is None and not swodat:
                message = 'If SWMONTH is not provided, either PERIOD or SWODAT has to be provided'
                raise exc.ErrorMissingParameter(message)  # can't all be empty

            if period is not None and period > 0:
                exc.check_range(period, 1, 366, 'closed', 'open')

            if swodat:
                if outdatin is None:
                    raise exc.ErrorMissingParameter(
                        'When SWODAT is True, OUTDATIN has to be provided.')
                else:
                    outdatin = DataFrame({'date': outdatin}).to_string(
                        header=False, index=False)

        if not swyrvar:
            if datefix is None:
                raise exc.ErrorMissingParameter(
                    'If SWYRWAR is False, DATEFIX has to be specified.')
        else:
            if outdat is None:
                raise exc.ErrorMissingParameter(
                    'If SWYRVAR is True, OUTDAT has to be specified.')
            else:
                outdat = DataFrame({'date': outdat}).to_string(
                    header=False, index=False)

        self.update_parameters(self.get_args_dict(locals()), 'general')

    def set_output_files(self,
                         outfil: str = 'result',
                         swheader: bool = False,
                         swwba: bool = False,
                         swend: bool = False,
                         swvap: bool = True,
                         swbal: bool = False,
                         swblc: bool = True,
                         swsba: bool = True,
                         swate: bool = False,
                         swbma: bool = False,
                         swdrf: bool = False,
                         swswb: bool = False,
                         swini: bool = False,
                         swinc: bool = True,
                         swcrp: bool = False,
                         swstr: bool = False,
                         swirg: bool = False,
                         swcsv: bool = False,
                         inlist_csv: list[str] = None,
                         swcsv_tz: bool = False,
                         inlist_csv_tz: list[str] = None,
                         swafo: int = 0,
                         swaun: int = 0,
                         critdevmasbal: float = None,
                         swdiscrvert: bool = False,
                         numnodnew: int = None,
                         dznew: list[float] = None) -> None:
        """
        Sets the output files and their parameters for the model run.

        Args:
            outfil (str): The name of the output file (default 'result').
            swheader (bool): Print header at the start of each balance period (default False).
            swwba (bool): Output cumulative water balance (default False).
            swend (bool): Output end-conditions (default False).
            swvap (bool): Output soil profiles of moisture, solute and temperature (default True).
            swbal (bool): Output file with yearly water balance (default False).
            swblc (bool): Output file with detailed yearly water balance (default True).
            swsba (bool): Output file of cumulative solute balance (default True).
            swate (bool): Output file with soil temperature profiles (default False).
            swbma (bool): Output file with water fluxes, only for macropore flow (default False).
            swdrf (bool): Output of drainage fluxes, only for extended drainage (default False).
            swswb (bool): Output surface water reservoir, only for extended drainage (default False).
            swini (bool): Output of initial SoilPhysParam and HeatParam (default False).
            swinc (bool): Output of water balance increments (default True).
            swcrp (bool): Output of simple or detailed crop growth model (default False).
            swstr (bool): Output of stress values for wetness, drought, salinity and frost (default False).
            swirg (bool): Output of irrigation gifts (default False).
            swcsv (bool): Write output to a CSV file (default False).
            inlist_csv (list[str]): A list of variables to include in the CSV file (default ['rain', 'irrig', 'interc',
                               'runoff', 'drainage', 'dstor', 'epot', 'eact', 'tpot', 'tact', 'qbottom', 'gwl']).
            swcsv_tz (bool): Write output to a CSV file (with timezone information??) (default False).
            inlist_csv_tz (list[str]): A list of variables to include in the CSV file (default ['wc', 'h', 'conc']).
            swafo (bool): Output file with formatted hydrological data (default False).
            swaun (bool): Output file with unformatted hydrological data (default False).
            critdevmasbal (float): Range 0.0-1.0 cm. Critical Deviation in water balance during PERIOD
                                   (default 0.00001).
            swdiscrvert (bool): Convert vertical discretization (default False).
            numnodnew (int): Range 1-macp (Not sure what this is). The number of new nodes (default 6).
                             note: boundaries of soil layers may not change, which implies that the sum of thicknesses
                             within a soil layer must be equal to the thickness of the soil layer. See also:
                             SoilWaterSection, Part4: Vertical discretization of soil profile.
            dznew (list[float]): Range 0.000001-500.0 cm. A list of new node thicknesses (default [10.0, 10.0, 10.0,
                                                                                                   20.0, 30.0, 50.0]).

        Returns:
            None
            TODO: NUMNODENEW seems to be linked to DZNEW. Would be good to do a check o aoutocalculateion of either.
        """

        if swcsv:
            if inlist_csv is None:
                raise exc.ErrorMissingParameter(
                    'If SWCSV is True, INLIST_CSV has to be provided.')
            else:
                exc.check_type(inlist_csv, list)
                inlist_csv = list_to_string(inlist_csv,
                                            newline=False,
                                            separator=', ')

        if swcsv_tz:
            if inlist_csv_tz is None:
                raise exc.ErrorMissingParameter(
                    'If SWCSV_TZ is True, INLIST_CSV_TZ has to be provided.')
            else:
                exc.check_type(inlist_csv_tz, list)
                inlist_csv_tz = list_to_string(inlist_csv_tz,
                                               newline=False,
                                               separator=', ')

        exc.check_range(swafo, 0, 2, left='closed', right='closed')
        exc.check_range(swaun, 0, 2, left='closed', right='closed')

        if swafo > 0 or swaun > 0:
            if critdevmasbal is None or swdiscrvert is None:
                message = 'If SWAFO or SWAUN are 1 or 2, CRITMASBAL and SWDISCRVERT must be privided'
                raise exc.ErrorMissingParameter(message)
            else:
                exc.check_type(critdevmasbal, float)
                exc.check_type(swdiscrvert, bool)
                exc.check_range(critdevmasbal, 0.0, 1.0,
                                left='closed', right='closed')

        if swdiscrvert:
            if numnodnew is None:
                message = 'If SWDISCRVERT is True, NUMNODNEW is required.'
                raise exc.ErrorMissingParameter(message)
            if dznew is None:
                message = 'If SWDISCRVERT is True, DZNEW is required.'
                raise exc.ErrorMissingParameter(message)
            else:
                exc.check_type(dznew, list)
                dznew = list_to_string(dznew,
                                       newline=False,
                                       separator=' ')

        self.update_parameters(self.get_args_dict(locals()), 'general')

    def set_crop(self,
                 swcrop: bool,
                 rds: float = None,
                 croprotation: DataFrame = None,
                 crop: dict | None = None) -> None:
        """
        Sets crop parameters in the SWMM input file.

        Args:
            swcrop (bool, optional): Flag to indicate whether crop parameters are included in the SWMM input file.
            rds (float, optional): Radius of the depression storage. Default is 200.0.
            crop_rotation_data (DataFrame, optional): DataFrame containing crop rotation data. The dataframe HAS TO
            contain the following header: ['INITCROP', 'CROPSTART', 'CROPEND', 'CROPNAME', 'CROPFIL', 'CROPTYPE'], where
                CROPSTART - date of crop emergence [YYYY-MM-DD]
                CROPEND - date of crop harvest [YYYY-MM-DD]
                CROPFIL - name of file with crop input parameters without extension .CRP, [A40]
                CROPTYPE - growth module: 1 = simple; 2 = detailed, WOFOST general; 3 = detailed, WOFOST grass

            If None, a default crop rotation table will be loaded. Default is None.

        Returns:
            None.
        """

        if swcrop:
            if rds is None or croprotation is None:
                message = 'if SWCROP is True, RDS and crop table have to be provided'
                raise exc.ErrorMissingParameter(message)
            else:
                exc.check_type(rds, float)
                exc.check_range(rds, 1, 5000, left='closed', right='closed')

        self.crop = crop

        self.update_parameters(self.get_args_dict(locals()), 'crop')
        self.update_tables(self.get_args_dict(locals()), 'crop')

    def set_irrigation(self,
                       swirfix: bool,
                       schedule: bool,
                       swirgfil: bool | None = None,
                       irgfil: str | None = None,
                       irigevents: DataFrame | None = None,
                       startirr: str | None = None,
                       endirr: str | None = None,
                       cirrs: float | None = None,
                       isuas: int | None = None,
                       phFieldCapacity: float | None = None,
                       tcs: int | None = None,
                       phormc: int | None = None,
                       swcirrthres: bool | None = None,
                       cirrthres: float | None = None,
                       perirrsurp: float | None = None,
                       irgthreshold: float | None = None,
                       tcsfix: int | None = None,
                       dcrit: float | None = None,
                       irgdayfix: int | None = None,
                       dvs_tc1: DataFrame | None = None,
                       dvs_tc2: DataFrame | None = None,
                       dvs_tc3: DataFrame | None = None,
                       dvs_tc4: DataFrame | None = None,
                       dvs_tc5: DataFrame | None = None):
        """
        Sets the irrigation parameters in the SWAP input file.

        Args:
            swirfix (bool, optional): If True, fixed irrigation will be activated. Defaults to True.
            schedule (bool, optional): If True, scheduled irrigation will be activated. Defaults to False.
            swirgfil (bool, optional): If True, an irrigation file will be used. Defaults to False.
            irgfil (str, optional): The name of the irrigation file to be used. Defaults to 'testirri'.
            irigevents (pandas.DataFrame, optional): A DataFrame containing the irrigation events. Defaults to None.
            startirr (str, optional): The start date of the irrigation period (DD MM). Defaults to '30 3'.
            endirr (str, optional): The end date of the irrigation period (DD MM). Defaults to '31 12'.
            cirrs (float, optional): Range 0-100. Solute concentration of irrigation water (mg/cm3). Defaults to 0.0.
            isuas (int, optional): If 0, sprinkling irrigation, if 1 surface irrigation. Defaults to 1.
            phFieldCapacity (float, optional):  Range Soil water pressure head at field capacity (cm). Defaults to -100.0.
            tcs (int, optional): Irrigation timing options:
                              1 = Ratio actual/potential transpiration (Default)
                              2 = Depletion of Readily Available Water
                              3 = Depletion of Totally Available Water
                              4 = Depletion of absolute Water Amount
                              5 = Pressure head or moisture content
                              6 = Fixed weekly irrigation, bring root zone back to field capacity
            phormc (int, optional): use either pressure head (PHORMC = 0) or water content (PHORMC = 1)
            swcirrthres (bool, optional): Apply over-irrigation (Default is False)
            cirrthres (float, optional): Threshold salinity conc above which over-irrigation occurs [0..100 mg/cm3, R]
            perirrsurp (float, optional): The percentage of surplus irrigation water that will be stored in the soil (0-100%). Defaults to 10.0.
            irgthreshold (float, optional): Threshold value for weekly irrigation; only irrigate when soil water deficit is larger than threshold [0..20 mm, R]
            tcsfix (int, optional): Define minimum time interval between irrigation applications
            dcrit (float, optional): Depth of the sensor [-100..0 cm, R]
            irgdayfix (int, optional): Minimum number of days between irrigation applications [1..366 d, I]
            dvs_tc1 (pandas.DataFrame, optional): mimimum of ratio actual/potential transpiration Trel [0..1 -, R] as function of crop development stage (maximum 7 records)
            dvs_tc2 (pandas.DataFrame, optional): specify minimum fraction of readily available water RAW [0..1 -, R] as function of crop development stage (maximum 7 records)
            dvs_tc3 (pandas.DataFrame, optional): pecify minimal fraction of totally available water TAW [0..1 -, R] as function of crop development stage (maximum 7 records)
            dvs_tc4 (pandas.DataFrame, optional): specify maximum amount of water depleted below field capacity DWA [0..500 mm, R] as function of crop development stage (maximum 7 records)
            dvs_tc5 (pandas.DataFrame, optional): Also specify critical pressure head [-1d6..-100 cm, R] or moisture content [0..1 cm3/cm3, R] as function of crop development stage

        Raises:
            None.

        Returns:
            None.
        TODO: irigevents overlooked. Do not cause errors with the current settings.
        """

        # PART 1: FIXED IRRIGATION
        if swirfix:
            if swirgfil is None:
                raise exc.ErrorMissingParameter(
                    'If SWIRGFIX is True, SWIRGFIL cannot be empty.')
            elif swirgfil:  # if True, then irgfil has to be provided
                if irgfil is None:
                    message = 'If SWIRGFIL is True, IRGFIL has to be provided.'
                    raise exc.ErrorMissingParameter(message)
            else:  # otherwise, the irigevents have to be provided
                if irigevents is None:
                    message = 'If SWIRGFIL is False, irrigation events table has to be provided.'
                    raise exc.ErrorMissingParameter(message)

        # PART 2: SCHEDULED IRRIGATION
        if schedule:
            required = [startirr, endirr, cirrs, isuas, phFieldCapacity, tcs]
            if any(element is None for element in required):
                message = f'All of the following elements are required when scheduled irrigation is selected: \n ' \
                          f'[startirr, endirr, cirrs, isuas, phFieldCapacity, tcs]'

                raise exc.ErrorMissingParameter(message)
            else:
                exc.check_type(cirrs, float)
                exc.check_range(cirrs, 0, 100, left='closed', right='closed')
                exc.check_range(isuas, 0, 1, left='closed', right='closed')
                exc.check_type(phFieldCapacity, float)
                exc.check_range(phFieldCapacity, -1000, 0,
                                left='closed', right='closed')
                exc.check_range(tcs, 1, 6, left='closed', right='closed')

            if tcs == 1:
                dvs_tc1 = pd.DataFrame({'dvs_tc1': [0.0, 2.0],
                                        'Trel': [0.95, 0.95]})
            elif tcs == 2:
                dvs_tc2 = pd.DataFrame({'dvs_tc2': [0.0, 2.0],
                                        'RAW': [0.95, 0.95]})
            elif tcs == 3:
                dvs_tc3 = pd.DataFrame({'dvs_tc3': [0.0, 2.0],
                                        'TAW': [0.50, 0.50]})
            elif tcs == 4:
                dvs_tc4 = pd.DataFrame({'dvs_tc4': [0.0, 2.0],
                                        'DWA': [0.40, 0.40]})
            elif dvs_tc5 == 5:
                required = [phormc, dcrit, swcirrthres]
                if any(element is None for element in required is None):
                    message = 'If TCS is 5, at leasr PHORMC, DCRIT and SWCIRRTHRES have to be specified'
                    exc.ErrorMissingParameter(message)
                else:
                    dvs_tc5 = pd.DataFrame({'dvs_tc5': [0.0, 2.0],
                                            'Value_tc5': [-1000.0, -1000.0]})
                    if swcirrthres:
                        exc.check_type(cirrthres, float)
                        exc.check_range(cirrthres, 0, 100,
                                        left='closed', right='closed')
                        exc.check_type(perirrsurp, float)
                        exc.check_range(perirrsurp, 0, 100,
                                        left='closed', right='closed')

            elif tcs == 6:
                exc.check_type(irgthreshold, float)
                exc.check_range(irgthreshold, 0, 20,
                                left='closed', right='closed')
                exc.check_type(tcsfix, int)

                if tcsfix == 1:
                    exc.check_type(irgdayfix, int)
                    exc.check_range(irgdayfix, 1, 366,
                                    left='closed', right='closed')

        self.update_parameters(self.get_args_dict(locals()), 'irrigation')
        self.update_tables(self.get_args_dict(locals()), 'irrigation')

    def set_meteo(self,
                  swetr: bool,  # use P-M?
                  meteo_data: Meteo,
                  altw: float | None = None,
                  angstroma: float | None = None,
                  angstromb: float | None = None,
                  # apply P-M for distribution? else use crop factors.
                  swdivide: bool | None = None,
                  swmetdetail: bool | None = None,
                  nmetdetail: int | None = None,
                  # only required with swetr = False, but model does not run without it
                  swetsine: bool = False,
                  swrain: int = 0,  # same as swetsine
                  rainfil: str | None = None,
                  rainflux: DataFrame | None = None):
        """
        Sets the evapotranspiration input method.

        Two methods can be chosen: Penman-Monteith method and reference evapotranspiration. Prior to execution of
        this function, one has to create a Meteo object as it is a required argument of the function.

        Station coordinates are drawn from the Meteo object. Kwargs mostly are required when p-m method is chosen.

        :param et_method: Select between use of Penman-Monteith method and supplying reference evapotranspiration.
                            keywords are: 'penman-monteith' or 'reference'
        :param meteo_data: Meteo object containing information about the meteorological data file.

        :keyword lat: Latitude of meteo station [-90..90 degrees, R, North = +]
        :keyword lon: Longitude of meteo station [-90..90 degrees, R]
        :keyword alt: Altitude of meteo station [-400..3000 m, R]
        :keyword altw: Height of wind speed measurement above soil surface (10 m is default) [0..99 m, R]
        :keyword angstroma: Fraction of extraterrestrial radiation reaching the earth on overcast days [0..1 -, R]
        :keyword angstromb: Additional fraction of extraterrestrial radiation reaching the earth on clear days [0..1 -, R]
        :keyword swdivide: Whether the distribution of E & T is based on crop and soil factors or direct application
                            of Penman-Monteith method.
        :keyword swmetdetail: specify time interval of evapotranspiration and rainfall weather data:
                                0 = time interval is equal to one day
                                1 = time interval is less than one day
        :keyword nmetdetail: In case of detailed meteorological weather records (SWMETDETAIL = 1), specify the
                                number of weather data records each day [1..96 -, I]
        :keyword swetsine: In case of daily meteorological weather records (only if SWETR = 1): distribute daily
                            Tp and Ep according to sinus wave.
        :keyword swrain: use the actual rainfall intensity (only if SWETR = 1)
        :keyword rainflux: If SWRAIN = 1, then specify mean rainfall intensity [0.d0..1000.d0 mm/d, R] as function
                            of time TIME [0..366 d, R], maximum 30 records
        :keyword rainfil: If SWRAIN = 3, then specify file name of file with detailed rainfall data. File name of
                            detailed rainfall data without extension .YYY
        """

        self.meteo: Meteo = meteo_data

        if swetr:  # if P-M method is to be used:
            required = [altw, angstroma, angstromb, swdivide, swmetdetail]
            if any(element is None for element in required):
                message = 'If P-M method is used, all of the following parameters have to be filled: \n' \
                          '[altw, angstroma, angstromb, swdivide, swmetdetail]'
                raise exc.ErrorMissingParameter(message)

            exc.check_range(
                meteo_data.met_file_params['{ALT}'], -400, 3000, left='closed', right='closed')
            exc.check_range(altw, 0, 99, left='closed', right='closed')
            exc.check_range(angstroma, 0, 1, left='closed', right='closed')
            exc.check_range(angstromb, 0, 1, left='closed', right='closed')

            if swmetdetail:
                if nmetdetail is None:
                    message = 'If SWMETDETAIL is True, NMETDETAIL has to be provided'
                    raise exc.ErrorMissingParameter(message)
                else:
                    exc.check_range(nmetdetail, 1, 96,
                                    left='closed', right='closed')

        else:
            required = [swetsine, swrain]
            if any(element is None for element in required):
                message = 'if SWETR is False, SWETSIE and SWRAIN have to be provided'
                raise exc.ErrorMissingParameter(message)
            else:
                exc.check_range(swrain, 0, 3, left='closed', right='closed')

                if swrain == 1:
                    if rainflux is None:
                        message = 'If SWRAIN is 1, RAINFLUX has to be provided.'
                        raise exc.ErrorMissingParameter(message)
                    # TODO: check the length of the RAINFLUX table

                elif swrain == 3:
                    if rainfil is None:
                        message = 'If SWRAIN is 3, RAINFIL has to be provided.'
                        raise exc.ErrorMissingParameter(message)

        meteo_params = {'params': {'METFIL': f"meteo_{meteo_data.met_file_params['{FILENAME}']}.met",
                                   'LAT': meteo_data.met_file_params['{LAT}'],
                                   'LON': meteo_data.met_file_params['{LON}'],
                                   'ALT': meteo_data.met_file_params['{ALT}']}}

        self.update_parameters(self.get_args_dict(locals()), 'meteo')
        self.update_parameters(meteo_params, 'meteo')
        self.update_tables(self.get_args_dict(locals()), 'meteo')

    # soil-water section
    def set_init_soil_moisture(self,
                               swinco: str,
                               head_soildepth: DataFrame | None = None,
                               gwli: int | None = None,
                               inifil: str | None = None):
        """

        :param swinco: type of initial soil moisture condition:
                        ! 1 = pressure head as function of soil depth
                        ! 2 = pressure head of each compartment is in hydrostatic equilibrium with initial groundwater level
                        ! 3 = read final pressure heads from output file of previous Swap simulation
        :keyword zi_h: If SWINCO = 1, specify soil depth ZI [-1.d5..0 cm, R] and initial
                        soil water pressure head H [-1.d10..1.d4 cm, R]
        :keyword gwli: If SWINCO = 2, specify initial groundwater level [-10000..100 cm, R]
        :keyword inifil: If SWINCO = 3, specify output file with initial values for current run
                            (*.END filewhich contains initial values)
        """
        if swinco == 1:
            if head_soildepth is None:
                message = 'if SWINCO is 1, specify soil depth ZI and initial soil water pressure head are required'
                raise exc.ErrorMissingParameter(message)
            else:
                exc.check_type(head_soildepth, DataFrame)
        elif swinco == 2:
            if gwli is None:
                message = 'if SWINCO is 2, GWLI has to be provided.'
                raise exc.ErrorMissingParameter(message)
            else:
                exc.check_type(gwli, float)
                exc.check_range(gwli, -10000, 100, left='close', right='close')
        elif swinco == 3:
            if inifil is None:
                message = 'If SWINCO is 3, INIFIL has to be provided'
                raise exc.ErrorMissingParameter(message)

        self.update_parameters(self.get_args_dict(locals()), 'soil_water')
        self.update_tables(self.get_args_dict(locals()), 'soil_water')

    # TODO: add docstring and error handling
    def set_surface_flow(self,
                         swpondmx: int,
                         swrunon: bool,
                         pondmx: float | None = None,
                         rsro: float | None = None,
                         rsroexp: float | None = None,
                         rufil: str | None = None,
                         mxpondtb: DataFrame | None = None):

        self.update_parameters(self.get_args_dict(locals()), 'soil_water')
        self.update_tables(self.get_args_dict(locals()), 'soil_water')

    # TODO: add docstring and error handling
    def set_soil_evap(self,
                      swcfbs: bool,
                      swredu: int,
                      cfevappond: float | None = None,
                      cfbs: float | None = None,
                      rsoil: float | None = None,
                      cofredbl: float | None = None,
                      rsigni: float | None = None,
                      cofredbo: float | None = None,):

        self.update_parameters(self.get_args_dict(locals()), 'soil_water')

    # TODO: add docstring and error handling
    def set_soil_profile(self,
                         soilprofile: pd.DataFrame):

        self.update_tables(self.get_args_dict(locals()), 'soil_water')

    # TODO: add docstring and error handling
    def set_soil_parameters(self,
                            swsophy: bool,
                            swhyst: int,
                            swmacro: bool,
                            filenamesophy: str | None = None,
                            tau: float | None = None,
                            soilhydrfunc: DataFrame | None = None,):

        self.update_parameters(self.get_args_dict(locals()), 'soil_water')
        self.update_tables(self.get_args_dict(locals()), 'soil_water')

    # TODO: add docstring and error handling
    def set_snow_frost(self,
                       swsnow: bool,
                       swfrost: bool,
                       snowinco: float | None = None,
                       teprrain: float | None = None,
                       teprsnow: float | None = None,
                       snowcoef: float | None = None,
                       tfroststa: float | None = None,
                       tfrostend: float | None = None,):

        self.update_parameters(self.get_args_dict(locals()), 'soil_water')

    # TODO: add docstring and error handling
    def set_richards_params(self,
                            dtmin: float,
                            dtmax: float,
                            gwlconv: float,
                            critdevh1cp: float,
                            critdevh2cp: float,
                            critdevponddt: float,
                            maxit: int,
                            maxbacktr: int,
                            swkmean: int,
                            swkimpl: bool,):

        self.update_parameters(self.get_args_dict(locals()), 'soil_water')

    # TODO: add docstring and error handling
    def set_drainage(self,
                     swdra: bool = False,
                     drainage: Drainage = None):

        self.drainge = drainage

        self.update_parameters(self.get_args_dict(locals()), 'drainage')

    # TODO: add docstring and error handling
    def set_bottom_boundary(self,
                            swbbcfile: bool,
                            swbotb: int,
                            sw2: int | None = None,
                            sinave: float | None = None,
                            sinamp: float | None = None,
                            sinmax: float | None = None,
                            swbotb3resvert: int | None = None,
                            swbotb3impl: int | None = None,
                            shape: float | None = None,
                            hdrain: float | None = None,
                            rimlay: float | None = None,
                            sw3: int | None = None,
                            aqave: float | None = None,
                            aqamp: float | None = None,
                            aqtmax: float | None = None,
                            aqper: float | None = None,
                            sw4: int | None = None,
                            swqhbot: int | None = None,
                            cofqha: float | None = None,
                            cofqhb: float | None = None,
                            cofqhc: float | None = None,
                            bbcfil: str | None = None,
                            swbotbtb1: DataFrame | None = None,
                            swbotbtb2: DataFrame | None = None,
                            swbotbtb3a: DataFrame | None = None,
                            swbotbtb3b: DataFrame | None = None,
                            swbotbtb4: DataFrame | None = None,
                            swbotbtb5: DataFrame | None = None,):

        self.update_parameters(self.get_args_dict(locals()), 'bott_bound')
        self.update_tables(self.get_args_dict(locals()), 'bott_bound')

    # TODO: add docstring and error handling
    def set_heatflow(self,
                     swhea: bool,
                     swcalt: int | None = None,
                     tampli: float | None = None,
                     tmean: float | None = None,
                     timref: float | None = None,
                     ddamp: float | None = None,
                     swtopbhea: int | None = None,
                     tsoilfile: str | None = None,
                     swbotbhea: int | None = None,
                     soiltextures: DataFrame | None = None,
                     initsoil: DataFrame | None = None,
                     bbctsoil: DataFrame | None = None,):

        self.update_parameters(self.get_args_dict(locals()), 'heat_flow')
        self.update_tables(self.get_args_dict(locals()), 'heat_flow')

    # TODO: add docstring and error handling

    def set_solute_settings(self,
                            swsolu: bool,
                            cpre: float | None = None,
                            cdrain: float | None = None,
                            swbotbc: int | None = None,
                            cseep: float | None = None,
                            ddif: float | None = None,
                            tscf: float | None = None,
                            swsp: bool | None = None,
                            frexp: float | None = None,
                            cref: float | None = None,
                            swdc: bool | None = None,
                            gampar: float | None = None,
                            rtheta: float | None = None,
                            bexp: float | None = None,
                            swbr: bool | None = None,
                            daquif: float | None = None,
                            poros: float | None = None,
                            kfsat: float | None = None,
                            decsat: float | None = None,
                            cdraini: float | None = None,
                            cseeparrtb: DataFrame | None = None,
                            inissoil: DataFrame | None = None,
                            miscellaneous: DataFrame | None = None,):

        self.update_parameters(self.get_args_dict(locals()), 'solute')
        self.update_tables(self.get_args_dict(locals()), 'solute')

    def concat_swp_file(self):
        # for json it is necessary that there are keys in the dictionary. I'll hve to get rid of them when
        # writing the swp file
        swp_file_complete = {'params': {}, 'tables': {}}
        for item, value in self.swp_file.items():
            swp_file_complete['params'].update(value['params'])
            swp_file_complete['tables'].update(value['tables'])

        return swp_file_complete

    @staticmethod
    def format_parameters(swp_file_complete: dict):
        swp_file_complete['params'].update(
            {k: int(v) for k, v in swp_file_complete['params'].items() if isinstance(v, bool)})
        swp_file_complete['params'].update({k: f"'{v}'" for k, v in swp_file_complete['params'].items() if
                                            isinstance(v, str) and not v[0].isdigit()})

        swp_file_complete['tables'].update({k: v.to_string(index=False) for k, v in swp_file_complete['tables'].items()
                                            if isinstance(v, DataFrame)})

        return swp_file_complete

    def compile_swp_file(self,
                         path=None,
                         save=False):
        """
        Formatting the dictionary of parameters and tables into the swp file format.
        """

        swp_file_complete = self.format_parameters(self.concat_swp_file())

        file_text: str = ''

        for param, param_value in swp_file_complete['params'].items():
            file_text += f"{param} = {param_value} \n"
        for table, table_value in swp_file_complete['tables'].items():
            file_text += f"{table_value} \n"

        if save:
            save_file(string=file_text,
                      extension='swp',
                      fname='swap',
                      path=path,
                      mode='w',
                      encoding='ascii')

        return file_text

    async def model_to_db(self):

        """saves model settings to the sqlite database"""
        # Set up the Django environment

        # Construct the absolute path to your project directory

        import sys
        import os
        from django import setup
        from django.db import IntegrityError
        import io
        import pyarrow as pa
        from pyarrow.feather import write_feather

        sys.path.append(
            'C:/Users/zawad/PycharmProjects/pySWAP_django/djangoSWAP')
        os.environ['DJANGO_SETTINGS_MODULE'] = 'djangoSWAP.djangoSWAP.settings'
        setup()

        # import is with the reference to the sys path defined above
        # change of name was necessary to avoid conflict of names with the django model
        from view_models.models import SWAPModel as my_model  # noqa
        from asgiref.sync import sync_to_async

        buf = io.BytesIO()

        table = pa.Table.from_pandas(self.meteo.meteodata)
        write_feather(table, buf)
        buf.seek(0)

        # Read the content of the buffer as bytes
        met_data = buf.getvalue()

        # Create a new instance of the model with the required data
        new_swap_model = my_model(
            name=self.metadata.project_name,
            swp=self.format_parameters(self.concat_swp_file()),
            drainage=self.drainge.file,
            crop=self.crop.files,
            met=met_data
        )

        # using await and async is necessary here because the function is async.
        try:
            await sync_to_async(new_swap_model.save)()
            print(
                f"Model '{self.metadata.project_name}' was successfully added to the database.")
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e):
                print(
                    f"Warning: {e}. The model '{self.metadata.project_name}' already exists in the database.")
            else:
                print(
                    f"Warning: IntegrityError occurred while saving the model to the database. Error details: {e}")
