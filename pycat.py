#!/usr/bin/python

"""
Module is a start point for the program. It parses arguments provided by user as command line arguments and executes corresponding functions.
"""

import argparse

import pycatalicism.calc.calc as calc
import pycatalicism.config as config
from pycatalicism.calc.calculatorexception import CalculatorException
from pycatalicism.furnace.owen_protocol import OwenProtocol
from pycatalicism.furnace.owen_tmp101 import OwenTPM101
from pycatalicism.chromatograph.chromatec_control_panel_modbus import ChromatecControlPanelModbus
from pycatalicism.chromatograph.chromatec_analytic_modbus import ChromatecAnalyticModbus
from pycatalicism.chromatograph.chromatec_analytic_modbus import ChromatogramPurpose
from pycatalicism.chromatograph.chromatec_crystal_5000 import ChromatecCrystal5000
from pycatalicism.mass_flow_controller.bronkhorst_f201cv import BronkhorstF201CV

def calculate(args:argparse.Namespace):
    """
    Calculate conversion and/or selectivity (depending on --conversion/--selectivity flag provided by user) vs. temperature for CO oxidation or CO2 hydrogenation reactions, print results to console and export them if path to export directory was provided by user. Plot corresponding graphs if --show-plot argument was provided by user and export them if export directory was provided.
    """
    parser_type = config.raw_data_parser_type
    try:
        calc.calculate(input_data_path=args.input_data_path, initial_data_path=args.initial_data_path, reaction=args.reaction, parser_type=parser_type, calculate_conversion=args.conversion, calculate_selectivity=args.selectivity, products_basis=args.products_basis, output_data_path=args.output_data, show_plot=args.show_plot, output_plot_path=args.output_plot, sample_name=args.sample_name)
    except CalculatorException:
        print('At least one of the flags {--conversion|--selectivity} must be provided to the program')

def furnace_set_temperature(args:argparse.Namespace):
    """
    Set furnace temperature to specified value
    """
    temperature = float(args.temperature)
    furnace_controller.connect()
    furnace_controller.set_temperature(temperature)
    if temperature == 0:
        furnace_controller.set_temperature_control(False)
    else:
        furnace_controller.set_temperature_control(True)

def furnace_print_temperature(args:argparse.Namespace):
    """
    """
    furnace_controller.connect()
    temperature = furnace_controller.get_temperature()
    print(f'Current temperature is {temperature}°C')

def chromatograph_set_method(args:argparse.Namespace):
    """
    Set chromatograph instrument method
    """
    chromatograph.connect()
    chromatograph.set_method(method=args.method)

def chromatograph_start_analysis(args:argparse.Namespace):
    """
    Start chromatograph analysis
    """
    chromatograph.connect()
    chromatograph.start_analysis()

def chromatograph_set_passport(args:argparse.Namespace):
    """
    Set values of chromatogram passport. Should be run after analysis is complete.
    """
    chromatograph.connect()
    if args.purpose == 'analysis':
        purpose = ChromatogramPurpose.ANALYSIS
    elif args.purpose == 'graduation':
        purpose = ChromatogramPurpose.GRADUATION
    else:
        raise Exception(f'Unknown chromatogram purpose: {args.purpose}')
    chromatograph.set_passport(name=args.name, volume=float(args.volume), dilution=float(args.dilution), purpose=purpose, operator=args.operator, column=args.column, lab_name=args.lab_name)

def mfc_set_flow_rate(args:argparse.Namespace):
    """
    Set flow rate of mfc to specified value.
    """
    gas = args.gas
    flow_rate = float(args.flow_rate)
    if gas == 'He':
        mfc_He.connect()
        mfc_He.set_flow_rate(flow_rate)
    elif gas == 'CO2' or gas == 'O2':
        mfc_CO2.connect()
        mfc_CO2.set_flow_rate(flow_rate)
    elif gas == 'H2' or gas == 'CO' or gas == 'CH4':
        mfc_H2.connect()
        mfc_H2.set_flow_rate(flow_rate)
    else:
        raise Exception(f'Unknown gas {gas}!')

def mfc_set_calibration(args:argparse.Namespace):
    """
    Set calibration for mass flow controller.
    """
    gas = args.gas
    calibration_num = int(args.calibration_number)
    if gas == 'He':
        mfc_He.connect()
        mfc_He.set_calibration(calibration_num=calibration_num-1)
    elif gas in ['CO2', 'O2']:
        mfc_CO2.connect()
        mfc_CO2.set_calibration(calibration_num=calibration_num-1)
    elif gas in ['H2', 'CO', 'CH4']:
        mfc_H2.connect()
        mfc_H2.set_calibration(calibration_num=calibration_num-1)
    else:
        raise Exception(f'Unknown gas {gas}!')

def mfc_print_flow_rate(args:argparse.Namespace):
    """
    Print current flow rate.
    """
    gas = args.gas
    if gas == 'He':
        mfc_He.connect()
        print(f'{mfc_He.get_flow_rate()} nml/min')
    elif gas in ['CO2', 'O2']:
        mfc_CO2.connect()
        print(f'{mfc_CO2.get_flow_rate()} nml/min')
    elif gas in ['H2', 'CO', 'CH4']:
        mfc_H2.connect()
        print(f'{mfc_H2.get_flow_rate()} nml/min')
    else:
        raise Exception(f'Unknown gas {gas}!')

# initialize furnace controller
furnace_controller_protocol = OwenProtocol(address=config.furnace_address, port=config.furnace_port, baudrate=config.furnace_baudrate, bytesize=config.furnace_bytesize, parity=config.furnace_parity, stopbits=config.furnace_stopbits, timeout=config.furnace_timeout, write_timeout=config.furnace_write_timeout, rtscts=config.furnace_rtscts)
furnace_controller = OwenTPM101(device_name=config.furnace_device_name, owen_protocol=furnace_controller_protocol)

# initialize chromatograph
control_panel_modbus = ChromatecControlPanelModbus(modbus_id=config.control_panel_modbus_id, working_status_input_address=config.working_status_input_address, serial_number_input_address=config.serial_number_input_address, connection_status_input_address=config.connection_status_input_address, method_holding_address=config.method_holding_address, chromatograph_command_holding_address=config.chromatograph_command_holding_address, application_command_holding_address=config.application_command_holding_address)
analytic_modbus = ChromatecAnalyticModbus(modbus_id=config.analytic_modbus_id, sample_name_holding_address=config.sample_name_holding_address, chromatogram_purpose_holding_address=config.chromatogram_purpose_holding_address, sample_volume_holding_address=config.sample_volume_holding_address, sample_dilution_holding_address=config.sample_dilution_holding_address, operator_holding_address=config.operator_holding_address, column_holding_address=config.column_holding_address, lab_name_holding_address=config.lab_name_holding_address)
chromatograph = ChromatecCrystal5000(control_panel_modbus, analytic_modbus, config.methods)

# initialize mass flow controllers
mfc_He = BronkhorstF201CV(serial_address=config.mfc_He_serial_address, serial_id=config.mfc_He_serial_id, calibrations=config.mfc_He_calibrations)
mfc_CO2 = BronkhorstF201CV(serial_address=config.mfc_CO2_serial_address, serial_id=config.mfc_CO2_serial_id, calibrations=config.mfc_CO2_calibrations)
mfc_H2 = BronkhorstF201CV(serial_address=config.mfc_H2_serial_address, serial_id=config.mfc_H2_serial_id, calibrations=config.mfc_H2_calibrations)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(required=True)

calc_parser = subparsers.add_parser('calc', help='calculate conversion and selectivity vs. temperature')
calc_parser.set_defaults(func=calculate)
calc_parser.add_argument('input_data_path', metavar='input-data-path', help='path to directory with files from concentration measurement device')
calc_parser.add_argument('initial_data_path', metavar='initial-data-path', help='path to file with data about initial composition of gas')
calc_parser.add_argument('reaction', choices=['co-oxidation', 'co2-hydrogenation'], help='reaction for which to calculate data')
calc_parser.add_argument('--conversion', action='store_true', help='calculate conversion for the specified reaction')
calc_parser.add_argument('--selectivity', action='store_true', help='calculate selectivities for the specified reaction')
calc_parser.add_argument('--output-data', default=None, help='path to directory to save calculated data')
calc_parser.add_argument('--show-plot', action='store_true', help='whether to show data plot or not')
calc_parser.add_argument('--output-plot', default=None, help='path to directory to save plot')
calc_parser.add_argument('--products-basis', action='store_true', help='calculate conversion based on products concentration instead of reactants')
calc_parser.add_argument('--sample-name', help='sample name will be added to results data files and as a title to the result plots')

furnace_parser = subparsers.add_parser('furnace', help='control furnace')
furnace_subparser = furnace_parser.add_subparsers(required=True)
furnace_settemperature_parser = furnace_subparser.add_parser('set-temperature', help='set furnace temperature')
furnace_settemperature_parser.set_defaults(func=furnace_set_temperature)
furnace_settemperature_parser.add_argument('temperature', help='temperature in °C')
furnace_printtemperature_parser = furnace_subparser.add_parser('print-temperature', help='print current temperature in °C')
furnace_printtemperature_parser.set_defaults(func=furnace_print_temperature)

chromatograph_parser = subparsers.add_parser('chromatograph', help='commands to control chromatograph')
chromatograph_subparser = chromatograph_parser.add_subparsers(required=True)
chromatograph_setmethod_parser = chromatograph_subparser.add_parser('set-method', help='set instrumental method of chromatograph')
chromatograph_setmethod_parser.set_defaults(func=chromatograph_set_method)
chromatograph_setmethod_parser.add_argument('method', help='method name')
chromatograph_start_analysis_parser = chromatograph_subparser.add_parser('start-analysis', help='start analysis by chromatograph')
chromatograph_start_analysis_parser.set_defaults(func=chromatograph_start_analysis)
chromatograph_set_passport_parser = chromatograph_subparser.add_parser('set-passport', help='set chromatogram passport parameters (should be run after the analysis is over)')
chromatograph_set_passport_parser.set_defaults(func=chromatograph_set_passport)
chromatograph_set_passport_parser.add_argument('--name', required=True, help='name of chromatogram')
chromatograph_set_passport_parser.add_argument('--volume', default=0.5, help='sample volume')
chromatograph_set_passport_parser.add_argument('--dilution', default=1, help='sample dilution')
chromatograph_set_passport_parser.add_argument('--purpose', default='analysis', choices=['analysis', 'graduation'], help='purpose of chromatogram')
chromatograph_set_passport_parser.add_argument('--operator', required=True, help='operator\'s name')
chromatograph_set_passport_parser.add_argument('--column', required=True, help='column\'s name')
chromatograph_set_passport_parser.add_argument('--lab-name', default='Inorganic Nanomaterials', help='lab name')

mfc_parser = subparsers.add_parser('mfc', help='commands to control mass flow controllers')
mfc_subparser = mfc_parser.add_subparsers(required=True)
mfc_set_flow_parser = mfc_subparser.add_parser('set-flow-rate', help='set gas flow rate')
mfc_set_flow_parser.set_defaults(func=mfc_set_flow_rate)
mfc_set_flow_parser.add_argument('--gas', required=True, choices=['He', 'CO2', 'O2', 'H2', 'CO', 'CH4'], help='which gas to set flow rate for')
mfc_set_flow_parser.add_argument('--flow-rate', required=True, help='flow rate in nml/min')
mfc_set_calibration_parser = mfc_subparser.add_parser('set-calibration', help='set calibration')
mfc_set_calibration_parser.set_defaults(func=mfc_set_calibration)
mfc_set_calibration_parser.add_argument('--gas', required=True, choices=['He', 'CO2', 'O2', 'H2', 'CO', 'CH4'], help='which gas to set calibration for')
mfc_set_calibration_parser.add_argument('--calibration-number', required=True, help='number of calibration as written in calibraion document')
mfc_print_flow_rate_parser = mfc_subparser.add_parser('print-flow-rate', help='print current flow rate')
mfc_print_flow_rate_parser.set_defaults(func=mfc_print_flow_rate)
mfc_print_flow_rate_parser.add_argument('--gas', required=True, choices=['He', 'CO2', 'O2', 'H2', 'CO', 'CH4'], help='which gas to print flow rate for')

if (__name__ == '__main__'):
    args = parser.parse_args()
    args.func(args)
