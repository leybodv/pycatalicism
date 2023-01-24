###############################################################################
##                                                                           ##
## An example configuration for initial concentration measurement procedure. ##
## Program with this configuration will do following steps:                  ##
## - open CO2, H2 valves, set flow rates to 6, 12 ml/min, respectively       ##
## - purge chromatograph using 'purge' method                                ##
## - gather 3 chromatograms sequentially                                     ##
## - start chromatograph cooldown                                            ##
##                                                                           ##
###############################################################################

# gases used in initial composition measurement
gases = [
        'He', # He mass flow controller
        'CO2', # CO2/O2 mass flow controller
        'H2', # CH4/H2/CO mass flow controller
        ]
# valve states
# gas values must match the ones in config.py for valves configuration
# state values must be 'open' or 'close'
valves = {
            'He'  : 'close',
            'CO2' : 'open',
            'H2'  : 'open',
         }
# mass flow controllers calibrations
# see config.py for details
calibrations = [
                0, # He mass flow controller
                1, # CO2/O2 mass flow controller
                3, # CH4/H2/CO mass flow controller
                ]
# flow rates of gases for measurement
flow_rates = [
            0, # He mass flow controller
            6, # CO2/O2 mass flow controller
            12, # CH4/H2/CO mass flow controller
            ]
# chromatograph instrumental method to use for measurement
chromatograph_method = 'co2-hydrogenation'
# number of measurements
measurements_number = 3
# operator's name
operator = 'best-ever-operator'
