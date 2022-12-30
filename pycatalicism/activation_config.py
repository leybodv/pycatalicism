# gases connected to mass flow controllers, these will be shown on plot
gases = [
        'He',
        'CO2',
        'H2',
        ]
# valves states used at different steps
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
         ]
# mass flow controllers calibrations
# see config.py for details
calibrations = [
                [ # 1st step
                 0, # He mass flow controller
                 2, # CO2/O2 mass flow controller
                 2,  # CH4/H2/CO mass flow controller
                ],
                [ # 2nd step
                 0,
                 2,
                 2,
                ],
                [ # 3rd step
                 0,
                 2,
                 2,
                ],
               ]
# flow rates of gases during activation step
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
             ]
# temperature of activation in °C (last step must be 0 to turn off heating)
temperatures = [
                0,   # 1st step
                500, # 2nd step
                0,   # 3rd step
               ]
# activation duration in minutes (last step must be None)
times = [
         30,   # 1st step
         600,  # 2nd step
         None, # 3rd step
        ]
