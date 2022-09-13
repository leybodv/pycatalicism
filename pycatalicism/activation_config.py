# gases connected to mass flow controllers
gases = [
        'He',
        'O2',
        'H2',
        ]
# mass flow controllers calibrations
# see config.py for details
calibrations = [
                0, # He mass flow controller
                2, # CO2/O2 mass flow controller
                2  # CH4/H2/CO mass flow controller
                ]
# flow rates of gases during activation step
activation_flow_rates = [
                        0, # He mass flow controller
                        0, # CO2/O2 mass flow controller
                        36 # CH4/H2/CO mass flow controller
                        ]
# temperature of activation in °C
activation_temperature = 300
# activation duration in minutes
activation_duration = 60
# after the activation furnace is turned off and below this temperature gas flow rates will be changed to post_flow_rates values
post_temperature = 100
# flow rates of gases after the activation is over
post_flow_rates = [
                0, # He mass flow controller
                0, # CO2/O2 mass flow controller
                3  # CH4/H2/CO mass flow controller
                ]
