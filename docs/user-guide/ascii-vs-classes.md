# SWAP model settings

To run the SWAP model, you need to provide various parameters defined in several ASCII files. The main file, with a `.swp` extension, must always accompany the SWAP executable. Depending on the settings in this file, additional files might be required, such as `.crp` files for crop growth model settings. Each file contains key-value settings or tabular data, often grouped into sections representing different model components. In `pyswap`, these groups of variables are represented as classes.

=== "Classic SWAP"

    ```txt
    * Part 8: Snow and frost

    * Switch, calculate snow accumulation and melt:
      SWSNOW = 1                 ! 0 = no simulation of snow
                                ! 1 = simulation of snow accumulation and melt

    * If SWSNOW = 1, specify:
      SNOWINCO = 22.0            ! Initial snow water equivalent [0..1000 cm, R]
      TEPRRAIN = 2.0             ! Temperature above which all precipitation is rain[ 0..10 degree C, R]
      TEPRSNOW = -2.0            ! Temperature below which all precipitation is snow[-10..0 degree C, R]
      SNOWCOEF = 0.3             ! Snowmelt calibration factor [0...10 -, R]

    * Switch, in case of frost reduce soil water flow:
      SWFROST = 1                ! 0 = no simulation of frost
                                ! 1 = simulation of reduction soil water flow due to frost

    * If SWFROST = 1, then specify soil temperature range in which soil water flow is reduced
      TFROSTSTA = 0.0            ! Soil temperature where reduction of water fluxes starts [-10.0,5.0, degree C, R]
      TFROSTEND = -1.0           ! Soil temperature where reduction of water fluxes ends [-10.0,5.0, degree C, R]

    **********************************************************************************
    ```

=== "pyswap class"

    ``` py
    import pyswap as psp

    snow = psp.components.soilwater.SnowAndFrost(  # (1)!
      swsnow=1, snowinco=22.0, teprrain=2.0, teprsnow=-2.0, 
      snowcoef=0.3, swfrost=1, tfroststa=0.0, tfrostend=-1.0,
    )
    ```

    1.  When using a code editor like VS Code or PyCharm you start typing the names of the modules, you will get type hints and module documentation, that will help you navigate thorugh the package.



Classes generally act as "containers" for variables, but some also include functionality specific to their section, such as reading and formatting meteorological data from CSV files. The class definitions offer validation, type hinting, and built-in documentation that most code editors can utilize. This is especially helpful if you're just starting with the model, making it easier to understand and work with the parameters. Classes are explained in more details in the next section. If you are looking for more information about the input files visit the [wiki section](/wiki/).