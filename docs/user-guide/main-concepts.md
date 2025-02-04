# Main concepts

## SWAP model settings

A SWAP model requires a number of input variables in several different files. Traditionally, those variables are groupped into distinct sections and section parts in the input file templates. Below is an example of the :

```txt
**********************************************************************************
* Part 8: Snow and frost

* Switch, calculate snow accumulation and melt:
  SWSNOW = {{SWSNOW}}        ! 0 = no simulation of snow
                             ! 1 = simulation of snow accumulation and melt

{{#SWITCH_SWSNOW_OPTION_1}}
* If SWSNOW = 1, specify:
  SNOWINCO = {{SNOWINCO}}    ! Initial snow water equivalent [0..1000 cm, R]
  TEPRRAIN = {{TEPRRAIN}}    ! Temperature above which all precipitation is rain[ 0..10 oC, R]
  TEPRSNOW = {{TEPRSNOW}}    ! Temperature below which all precipitation is snow[-10..0 oC, R]
  SNOWCOEF = {{SNOWCOEF}}    ! Snowmelt calibration factor [0...10 -, R]

{{/SWITCH_SWSNOW_OPTION_1}}
* Switch, in case of frost reduce soil water flow:
  SWFROST = {{SWFROST}}      ! 0 = no simulation of frost
                             ! 1 = simulation of frost reduce soil water flow

{{#SWITCH_SWFROST_OPTION_1}}
* If SWFROST = 1, then specify soil temperature to start end end flux-reduction
  TFROSTSTA = {{TFROSTSTA}}  ! Soil temperature (oC) where reduction of water fluxes starts [-10.0,5.0, oC, R]
  TFROSTEND = {{TFROSTEND}}  ! Soil temperature (oC) where reduction of water fluxes ends [-10.0,5.0, oC, R]

{{/SWITCH_SWFROST_OPTION_1}}
**********************************************************************************

```

## pySWAP Generic classes

In pySWAP, the specific settings are groupped into **generic classes**. Each class, just like the section/section part, collects related settings together. An example of a class for snow and frost snow settings is presented below:

```py
class SnowAndFrost(PySWAPBaseModel):
    """Snow and frost settings for the model.

    Attributes:
        swsnow (Literal[0, 1]): Switch for calculation of snow accumulation and melt.
        swfrost (Literal[0, 1]): Switch,  in case of frost reduce soil water flow
        snowinco (Optional[float]): Initial snow water equivalent
        teprrain (Optional[float]): Temperature above which all precipitation is rain
        teprsnow (Optional[float]): Temperature below which all precipitation is snow
        snowcoef (Optional[float]): Snowmelt calibration factor
        tfroststa (Optional[float]): Soil temperature (oC) where reduction of water fluxes starts
        tfrostend (Optional[float]): Soil temperature (oC) where reduction of water fluxes ends

    """

    swsnow: Literal[0, 1]
    swfrost: Literal[0, 1]
    snowinco: Optional[float] = None
    teprrain: Optional[float] = None
    teprsnow: Optional[float] = None
    snowcoef: Optional[float] = None
    tfrostst: Optional[float] = None
    tfrostend: Optional[float] = None
```

Some classes have additional methods, but some just serve as "containers" for the variables. The purpose of that simple structure is mostly giving the model creation script a structure and validation.
