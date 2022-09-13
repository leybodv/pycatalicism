# gases connected to mass flow controllers
gases = [
        'He',
        'O2',
        'CO',
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
# minimal isothermal dwell time in minutes at each temperature to reach steady-state conditions
isothermal = 30
# list of measurement temperatures
temperatures = []
# name of sample
sample_name = '
# operator's name
operator = '
# catalyst loading
sample_mass = 
