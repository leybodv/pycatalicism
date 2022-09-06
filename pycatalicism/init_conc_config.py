# gases used in initial composition measurement
gases = [
        'He', # He mass flow controller
        'O2', # CO2/O2 mass flow controller
        'CO', # CH4/H2/CO mass flow controller
        ]
# mass flow controllers calibrations
# see config.py for details
calibrations = [
                0, # He mass flow controller
                2, # CO2/O2 mass flow controller
                4, # CH4/H2/CO mass flow controller
                ]
# flow rates of gases for measurement
flow_rates = [
            30, # He mass flow controller
            4, # CO2/O2 mass flow controller
            2, # CH4/H2/CO mass flow controller
            ]
# chromatograph instrumental method to use for measurement
chromatograph_method = 'co-oxidation'
# number of measurements
measurement_number = 5
# operator's name
operator = 
