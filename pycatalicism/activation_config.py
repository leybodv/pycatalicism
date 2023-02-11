############################################################################
##                                                                        ##
## An example configuration of activation procedure.                      ##
## Program with this configure will do following step:                    ##
## - open H2 valve, set H2 flow rate to 36 ml/min, wait for 30 min        ##
## - heat furnace to 500°C, wait for 600 min                              ##
## - change H2 flow rate to 3 ml/min, cool down furnace to 100°C          ##
## - open CO2 valve, set flow rate to 3 ml/min CO2 and 6 ml/min H2        ##
##                                                                        ##
############################################################################

# gases connected to mass flow controllers, these will be shown on plot
gases = [
        'He',
        'CO2',
        'H2',
        ]
# valves states used at different steps
# gas values must match the ones in config.py for valves configuration
# state values must be 'open' or 'close'
valves = [
          { # 1st step
           'He'  : 'close',
           'CO2' : 'close',
           'H2'  : 'open',
          },
          { # 2nd step
           'He'  : 'close',
           'CO2' : 'close',
           'H2'  : 'open',
          },
          { # 3rd step
           'He'  : 'close',
           'CO2' : 'close',
           'H2'  : 'open',
          },
          { # 4th step
           'He'  : 'close',
           'CO2' : 'open',
           'H2'  : 'open',
          },
         ]
# mass flow controllers calibrations
# see config.py for details
calibrations = [
                [ # 1st step
                 0, # He mass flow controller
                 1, # CO2/O2 mass flow controller
                 3,  # CH4/H2/CO mass flow controller
                ],
                [ # 2nd step
                 0,
                 1,
                 3,
                ],
                [ # 3rd step
                 0,
                 1,
                 3,
                ],
                [ # 4th step
                 0,
                 1,
                 3,
                ],
               ]
# flow rates of gases in ml/min during activation step
flow_rates = [
              [ # 1st step
               0, # He mass flow controller
               0, # CO2/O2 mass flow controller
               36, # CH4/H2/CO mass flow controller
              ],
              [ # 2nd step
               0,
               0,
               36,
              ],
              [ # 3rd step
               0,
               0,
               3,
              ],
              [ # 4th step
               0,
               3,
               6,
              ],
             ]
# temperature of activation in °C (last step must be 0 to turn off heating)
temperatures = [
                0,   # 1st step
                500, # 2nd step
                100, # 3rd step
                0,   # 4th step
               ]
# activation duration in minutes (last step must be None)
times = [
         30,   # 1st step
         600,  # 2nd step
         0,    # 3rd step
         None, # 4th step
        ]
