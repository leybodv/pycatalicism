#################################################################################
##                                                                             ##
## An example configuration of measurement procedure.                          ##
## Program with this configuration will do following steps:                    ##
## - open CO2, H2 valves, set flow rate to 6, 12 ml/min, respectively          ##
## - purge system for 10 min                                                   ##
## - heat to 200, 230 ... 380°C and measure chromatogram after at least 45 min ##
##                                                                             ##
#################################################################################

# gases connected to mass flow controllers (will be shown on plot)
gases = [
        'He',
        'CO2',
        'H2',
        ]
# valve states
# gas values must match the ones in config.py for valves configuration
# state values must be 'open' or 'close'
valves = {
           'He'  : 'close',
           'CO2' : 'open',
           'H2'  : 'open',
         }
# time in minutes to purge the system before heating step
purge_time = 10
# mass flow controllers calibrations
# see config.py for details
calibrations = [
                0, # He mass flow controller
                1, # CO2/O2 mass flow controller
                3, # CH4/H2/CO mass flow controller
                ]
# flow rates of gases for measurement
flow_rates = [
            0,  # He mass flow controller
            6,  # CO2/O2 mass flow controller
            12, # CH4/H2/CO mass flow controller
            ]
# chromatograph instrumental method to use for measurement
chromatograph_method = 'co2-hydrogenation'
# minimal isothermal dwell time in minutes at each temperature to reach steady-state conditions
isothermal = 45
# list of measurement temperatures
temperatures = [200, 230, 260, 290, 320, 350, 380]
# name of sample
sample_name = 'best-ever-sample'
# operator's name
operator = 'best-ever-operator'
# catalyst loading in mg (not used by the program but useful to save it here)
sample_mass = 100500
