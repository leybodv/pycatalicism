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
control_panel_modbus_id = 1
working_status_input_address = 0
serial_number_input_address = 2
connection_status_input_address = 17
method_holding_address = 0
chromatograph_command_holding_address = 2
application_command_holding_address = 3
analytic_modbus_id = 2
sample_name_holding_address = 0
chromatogram_purpose_holding_address = 15
sample_volume_holding_address = 17
sample_dilution_holding_address = 21
operator_holding_address = 25
column_holding_address = 40
lab_name_holding_address = 55
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
