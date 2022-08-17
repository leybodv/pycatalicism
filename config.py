# parser type used to convert raw data from equipment for gas composition measurement to input data for calculator to calculate conversion/activity/selectivity vs. temperature
#
# chromatec-crystal-composition-copy-paste
#   raw data obtained via copy/paste of composition calculation results from chromatec analytics software
#   data must be in a format:
#   Температура<tab><temperature>
#   <br>
#   Название<tab>Время, мин<tab>Детектор<tab>Концентрация<tab>Ед, измерения<tab>Площадь<tab>Высота
#   <compound-name><tab><retention-time><tab><detector-name><tab><compound-concentration><tab><concentration-units><tab><peak-area><tab><peak-height>
#   [<br>
#   Темп. (газовые часы)<tab><flow-temperature>
#   Давление (газовые часы)<tab><flow-pressure>
#   Поток<tab><flow-rate>]
raw_data_parser_type = 'chromatec-crystal-composition-copy-paste'

# logging levels for different classes/modules
import logging
logging_levels = {
                    'ChromatecCrystalCompositionCopyPasteParser'    :   logging.INFO,
                    'CO2HydrogenationCalculator'                    :   logging.INFO,
                    'CO2HydrogenationProductsBasisCalculator'       :   logging.INFO,
                    'CO2HydrogenationExporter'                      :   logging.INFO,
                    'CO2HydrogenationPlotter'                       :   logging.INFO,
                    'COOxidationCalculator'                         :   logging.INFO,
                    'COOxidationExporter'                           :   logging.INFO,
                    'COOxidationPlotter'                            :   logging.INFO,
                    'RawData'                                       :   logging.INFO,
                    }

## chromatograph configuration ##
# slave id in control panel modbus configuration
control_panel_modbus_id = 1
# register with working status of chromatograph
working_status_input_address = 0
# register with resial number of chromatograph
serial_number_input_address = 2
# register with connection status
connection_status_input_address = 17
# register with current instrumental method
method_holding_address = 0
# register with chromatograph command
chromatograph_command_holding_address = 2
# register with control panel application command
application_command_holding_address = 3
# slave id in analytic modbus configuration
analytic_modbus_id = 2
# register with chromatogram nams
sample_name_holding_address = 0
# register with chromatogram purpose
chromatogram_purpose_holding_address = 15
# register with sample's volume
sample_volume_holding_address = 17
# register with sample's dilution
sample_dilution_holding_address = 21
# register with operator's name
operator_holding_address = 25
# register with column name
column_holding_address = 40
# register with lab name
lab_name_holding_address = 55
# list of methods with their order number at control panel software
methods = {
        '20220415_O2-N2-CO2-CO-C1,5HxAlkanes_2levels'	:		0,
        'co2-hydrogenation'								:		1,
        'co-oxidation'									:		2,
        'crm'											:		3,
        'Marusya method'								:		4,
        'NaX-conditioning'								:		5,
        'NaX-HaesepN-conditioning'						:		6,
        'purge'											:		7,
        'purge-overnight'								:		8,
        'zero'											:		9,
        'Водка-Маруся'									:		10,
        }

## furnace configuration (only used by co2-hydrogenation.py right now ##
## for pycat.py use furnace_config.py for configuration ##
import serial

# Dictionary of logging levels of corresponding classes
logging_levels = {
                'FurnaceData'               :    logging.INFO,
                'Owen_TPM101_Controller'    :    logging.INFO,
                'SimpleTempTimeExporter'    :    logging.INFO,
                'SimpleTempTimePlotter'     :    logging.INFO
                }

# Furnace controller type
controller_type = 'Owen_TPM101'
# Furnace controller port name and corresponding port parameters (baudrate, bytesize, parity, stopbits) which must be the same as configured on controller device
furnace_port = 'COM6'
furnace_baudrate = 19200
furnace_bytesize = serial.EIGHTBITS
furnace_parity = serial.PARITY_NONE
furnace_stopbits = serial.STOPBITS_ONE
# Time in seconds to wait for the response from the device
furnace_timeout = 0.1
# Time in seconds to wait while message is sent to the device
furnace_write_timeout = None
# Enable/disable hardware flow control
furnace_rtscts = False
# Address of Owen TRM101 device
furnace_address = 0
# Time interval between message was sent to the device and controller was sent the answer in ms
furnace_rsdl = 20
# Address length in bits. Can be 8 or 11 bits, however only 8 bits is supported now
furnace_address_len = 8

# Type of plotter to plot temperature vs. time data
plotter_type = 'simple_temp_time_plotter'
# Resolution of figure
fig_dpi = 96
# Width of figure in inches
fig_width = 800 / fig_dpi
# Height of figure in inches
fig_height = 600 / fig_dpi

# Type of exporter to save temperature vs. time data
exporter_type = 'simple_temp_time_exporter'
