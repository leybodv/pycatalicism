#!/usr/bin/python

"""
Module is a start point for the program. It parses arguments provided by user as command line arguments and executes corresponding functions.
"""

import argparse
import time
import importlib
import importlib.util
import sys
from pathlib import Path
from datetime import date

import pycatalicism.calc.calc as calc
import pycatalicism.config as config
from pycatalicism.calc.calculatorexception import CalculatorException
from pycatalicism.furnace.owen_protocol import OwenProtocol
from pycatalicism.furnace.owen_tmp101 import OwenTPM101
from pycatalicism.chromatograph.chromatec_control_panel_modbus import ChromatecControlPanelModbus
from pycatalicism.chromatograph.chromatec_analytic_modbus import ChromatecAnalyticModbus
from pycatalicism.chromatograph.chromatec_analytic_modbus import ChromatogramPurpose
from pycatalicism.chromatograph.chromatec_crystal_5000 import ChromatecCrystal5000
from pycatalicism.chromatograph.chromatec_control_panel_modbus import WorkingStatus
from pycatalicism.mass_flow_controller.bronkhorst_f201cv import BronkhorstF201CV
from pycatalicism.plotters.process_plotter import DataCollectorPlotter

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
    furnace_controller_protocol = OwenProtocol(address=config.furnace_address, port=config.furnace_port, baudrate=config.furnace_baudrate, bytesize=config.furnace_bytesize, parity=config.furnace_parity, stopbits=config.furnace_stopbits, timeout=config.furnace_timeout, write_timeout=config.furnace_write_timeout, rtscts=config.furnace_rtscts)
    furnace_controller = OwenTPM101(device_name=config.furnace_device_name, owen_protocol=furnace_controller_protocol)
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
    furnace_controller_protocol = OwenProtocol(address=config.furnace_address, port=config.furnace_port, baudrate=config.furnace_baudrate, bytesize=config.furnace_bytesize, parity=config.furnace_parity, stopbits=config.furnace_stopbits, timeout=config.furnace_timeout, write_timeout=config.furnace_write_timeout, rtscts=config.furnace_rtscts)
    furnace_controller = OwenTPM101(device_name=config.furnace_device_name, owen_protocol=furnace_controller_protocol)
    furnace_controller.connect()
    temperature = furnace_controller.get_temperature()
    print(f'Current temperature is {temperature}°C')

def chromatograph_set_method(args:argparse.Namespace):
    """
    Set chromatograph instrument method
    """
    control_panel_modbus = ChromatecControlPanelModbus(modbus_id=config.control_panel_modbus_id, working_status_input_address=config.working_status_input_address, serial_number_input_address=config.serial_number_input_address, connection_status_input_address=config.connection_status_input_address, method_holding_address=config.method_holding_address, chromatograph_command_holding_address=config.chromatograph_command_holding_address, application_command_holding_address=config.application_command_holding_address)
    analytic_modbus = ChromatecAnalyticModbus(modbus_id=config.analytic_modbus_id, sample_name_holding_address=config.sample_name_holding_address, chromatogram_purpose_holding_address=config.chromatogram_purpose_holding_address, sample_volume_holding_address=config.sample_volume_holding_address, sample_dilution_holding_address=config.sample_dilution_holding_address, operator_holding_address=config.operator_holding_address, column_holding_address=config.column_holding_address, lab_name_holding_address=config.lab_name_holding_address)
    chromatograph = ChromatecCrystal5000(control_panel_modbus, analytic_modbus, config.methods)
    chromatograph.connect()
    chromatograph.set_method(method=args.method)

def chromatograph_start_analysis(args:argparse.Namespace):
    """
    Start chromatograph analysis
    """
    control_panel_modbus = ChromatecControlPanelModbus(modbus_id=config.control_panel_modbus_id, working_status_input_address=config.working_status_input_address, serial_number_input_address=config.serial_number_input_address, connection_status_input_address=config.connection_status_input_address, method_holding_address=config.method_holding_address, chromatograph_command_holding_address=config.chromatograph_command_holding_address, application_command_holding_address=config.application_command_holding_address)
    analytic_modbus = ChromatecAnalyticModbus(modbus_id=config.analytic_modbus_id, sample_name_holding_address=config.sample_name_holding_address, chromatogram_purpose_holding_address=config.chromatogram_purpose_holding_address, sample_volume_holding_address=config.sample_volume_holding_address, sample_dilution_holding_address=config.sample_dilution_holding_address, operator_holding_address=config.operator_holding_address, column_holding_address=config.column_holding_address, lab_name_holding_address=config.lab_name_holding_address)
    chromatograph = ChromatecCrystal5000(control_panel_modbus, analytic_modbus, config.methods)
    chromatograph.connect()
    chromatograph.start_analysis()

def chromatograph_set_passport(args:argparse.Namespace):
    """
    Set values of chromatogram passport. Should be run after analysis is complete.
    """
    control_panel_modbus = ChromatecControlPanelModbus(modbus_id=config.control_panel_modbus_id, working_status_input_address=config.working_status_input_address, serial_number_input_address=config.serial_number_input_address, connection_status_input_address=config.connection_status_input_address, method_holding_address=config.method_holding_address, chromatograph_command_holding_address=config.chromatograph_command_holding_address, application_command_holding_address=config.application_command_holding_address)
    analytic_modbus = ChromatecAnalyticModbus(modbus_id=config.analytic_modbus_id, sample_name_holding_address=config.sample_name_holding_address, chromatogram_purpose_holding_address=config.chromatogram_purpose_holding_address, sample_volume_holding_address=config.sample_volume_holding_address, sample_dilution_holding_address=config.sample_dilution_holding_address, operator_holding_address=config.operator_holding_address, column_holding_address=config.column_holding_address, lab_name_holding_address=config.lab_name_holding_address)
    chromatograph = ChromatecCrystal5000(control_panel_modbus, analytic_modbus, config.methods)
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
    mfc_He = BronkhorstF201CV(serial_address=config.mfc_He_serial_address, serial_id=config.mfc_He_serial_id, calibrations=config.mfc_He_calibrations)
    mfc_CO2 = BronkhorstF201CV(serial_address=config.mfc_CO2_serial_address, serial_id=config.mfc_CO2_serial_id, calibrations=config.mfc_CO2_calibrations)
    mfc_H2 = BronkhorstF201CV(serial_address=config.mfc_H2_serial_address, serial_id=config.mfc_H2_serial_id, calibrations=config.mfc_H2_calibrations)
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
    mfc_He = BronkhorstF201CV(serial_address=config.mfc_He_serial_address, serial_id=config.mfc_He_serial_id, calibrations=config.mfc_He_calibrations)
    mfc_CO2 = BronkhorstF201CV(serial_address=config.mfc_CO2_serial_address, serial_id=config.mfc_CO2_serial_id, calibrations=config.mfc_CO2_calibrations)
    mfc_H2 = BronkhorstF201CV(serial_address=config.mfc_H2_serial_address, serial_id=config.mfc_H2_serial_id, calibrations=config.mfc_H2_calibrations)
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
    mfc_He = BronkhorstF201CV(serial_address=config.mfc_He_serial_address, serial_id=config.mfc_He_serial_id, calibrations=config.mfc_He_calibrations)
    mfc_CO2 = BronkhorstF201CV(serial_address=config.mfc_CO2_serial_address, serial_id=config.mfc_CO2_serial_id, calibrations=config.mfc_CO2_calibrations)
    mfc_H2 = BronkhorstF201CV(serial_address=config.mfc_H2_serial_address, serial_id=config.mfc_H2_serial_id, calibrations=config.mfc_H2_calibrations)
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

def activate(args:argparse.Namespace):
    """
    Activate catalyst using parameters defined in configuration file, provided as argument. Configuration file is file with several variables created using python syntax. Use activation_config.py as an example. Method initializes furnace controller, mass flow controllers and connects to the devices. It sets mass flow controllers with proper calibrations and flow rates (corresponding valves must be opened prior this method is called). It waits 10 minutes for system to be purged with gases, heats furnace to activation temperature and holds it at that temperature for activation time. It then turns off heating, waits until furnace is cooled down and sets gas flow rates to the specified in configuration file values. NB: valves cannot be opened or closed automatically.
    """
    # import configuration variables
    config_path = Path(args.config)
    config_spec = importlib.util.spec_from_file_location('process_config', config_path)
    if config_spec is None:
        raise Exception(f'Cannot read config file at {args.config}')
    config_loader = config_spec.loader
    if config_loader is None:
        raise Exception(f'Cannot read config file at {args.config}')
    config_module = importlib.util.module_from_spec(config_spec)
    sys.modules['process_config'] = config_module
    config_loader.exec_module(config_module)
    process_config = importlib.import_module('process_config')
    # initialize furnace controller
    furnace_controller_protocol = OwenProtocol(address=config.furnace_address, port=config.furnace_port, baudrate=config.furnace_baudrate, bytesize=config.furnace_bytesize, parity=config.furnace_parity, stopbits=config.furnace_stopbits, timeout=config.furnace_timeout, write_timeout=config.furnace_write_timeout, rtscts=config.furnace_rtscts)
    furnace_controller = OwenTPM101(device_name=config.furnace_device_name, owen_protocol=furnace_controller_protocol)
    # initialize mass flow controllers
    mfcs = list()
    mfcs.append(BronkhorstF201CV(serial_address=config.mfc_He_serial_address, serial_id=config.mfc_He_serial_id, calibrations=config.mfc_He_calibrations))
    mfcs.append(BronkhorstF201CV(serial_address=config.mfc_CO2_serial_address, serial_id=config.mfc_CO2_serial_id, calibrations=config.mfc_CO2_calibrations))
    mfcs.append(BronkhorstF201CV(serial_address=config.mfc_H2_serial_address, serial_id=config.mfc_H2_serial_id, calibrations=config.mfc_H2_calibrations))
    # connect to devices
    furnace_controller.connect()
    for mfc in mfcs:
        mfc.connect()
    # set mass flow controllers calibrations and flow rates
    for mfc, calibration, flow_rate in zip(mfcs, process_config.calibrations, process_config.activation_flow_rates):
        mfc.set_calibration(calibration_num=calibration)
        mfc.set_flow_rate(flow_rate)
    # start plotter
    # plotter = DataCollectorPlotter(process='activation', furnace_controller=furnace_controller, mass_flow_controllers=mfcs)
    # plotter.run()
    # wait system to be purged with gases for 10 minutes
    time.sleep(10*60)
    # heat furnace to activation temperature, wait until temperature is reached
    furnace_controller.set_temperature_control(True)
    furnace_controller.set_temperature(process_config.activation_temperature)
    while True:
        current_temperature = furnace_controller.get_temperature()
        if current_temperature >= process_config.activation_temperature:
            break
        time.sleep(60)
    # dwell for activation duration time
    time.sleep(process_config.activation_duration*60)
    # turn off heating, wait until furnace is cooled down to post_temperature
    furnace_controller.set_temperature(0)
    furnace_controller.set_temperature_control(False)
    while True:
        current_temperature = furnace_controller.get_temperature()
        if current_temperature <= process_config.post_temperature:
            break
        time.sleep(60)
    # change gas flow rates to post activation values
    for mfc, flow_rate in zip(mfcs, process_config.post_flow_rates):
        mfc.set_flow_rate(flow_rate)
    # print('Hit enter to stop plotter')
    # input()
    # plotter.stop()

def measure(args:argparse.Namespace):
    """
    Gather chromatograms at different measurement temperatures defined in a config file provided as an argument. Configuration file is a file with several variables defined using python syntax. Use measurement_config.py as an example of configuration. Method initializes devices and connects to them. It sets chromatograph method to 'purge', sets mass flow controller calibrations and flow rates. Heats furnace to the first measurement temperature and waits until target temperature is reached. Starts chromatograph purge, waits until purge is over and sets chromatograph method to the one specified in a config. Then, for each measurement temperature, method waits until chromatograph is ready for analysis, starts measurement, heats furnace to the next temperature. Finally, it turns off furnace and starts chromatograph cool down.
    """
    # import configuration variables
    config_path = Path(args.config)
    config_spec = importlib.util.spec_from_file_location('process_config', config_path)
    if config_spec is None:
        raise Exception(f'Cannot read config file at {args.config}')
    config_loader = config_spec.loader
    if config_loader is None:
        raise Exception(f'Cannot read config file at {args.config}')
    config_module = importlib.util.module_from_spec(config_spec)
    sys.modules['process_config'] = config_module
    config_loader.exec_module(config_module)
    process_config = importlib.import_module('process_config')
    # what is the date today?
    today = date.today()
    # initialize furnace controller
    furnace_controller_protocol = OwenProtocol(address=config.furnace_address, port=config.furnace_port, baudrate=config.furnace_baudrate, bytesize=config.furnace_bytesize, parity=config.furnace_parity, stopbits=config.furnace_stopbits, timeout=config.furnace_timeout, write_timeout=config.furnace_write_timeout, rtscts=config.furnace_rtscts)
    furnace = OwenTPM101(device_name=config.furnace_device_name, owen_protocol=furnace_controller_protocol)
    # initialize mass flow controllers
    mfcs = list()
    mfcs.append(BronkhorstF201CV(serial_address=config.mfc_He_serial_address, serial_id=config.mfc_He_serial_id, calibrations=config.mfc_He_calibrations))
    mfcs.append(BronkhorstF201CV(serial_address=config.mfc_CO2_serial_address, serial_id=config.mfc_CO2_serial_id, calibrations=config.mfc_CO2_calibrations))
    mfcs.append(BronkhorstF201CV(serial_address=config.mfc_H2_serial_address, serial_id=config.mfc_H2_serial_id, calibrations=config.mfc_H2_calibrations))
    # initialize chromatograph
    control_panel_modbus = ChromatecControlPanelModbus(modbus_id=config.control_panel_modbus_id, working_status_input_address=config.working_status_input_address, serial_number_input_address=config.serial_number_input_address, connection_status_input_address=config.connection_status_input_address, method_holding_address=config.method_holding_address, chromatograph_command_holding_address=config.chromatograph_command_holding_address, application_command_holding_address=config.application_command_holding_address)
    analytic_modbus = ChromatecAnalyticModbus(modbus_id=config.analytic_modbus_id, sample_name_holding_address=config.sample_name_holding_address, chromatogram_purpose_holding_address=config.chromatogram_purpose_holding_address, sample_volume_holding_address=config.sample_volume_holding_address, sample_dilution_holding_address=config.sample_dilution_holding_address, operator_holding_address=config.operator_holding_address, column_holding_address=config.column_holding_address, lab_name_holding_address=config.lab_name_holding_address)
    chromatograph = ChromatecCrystal5000(control_panel_modbus, analytic_modbus, config.methods)
    # connect to devices
    furnace.connect()
    for mfc in mfcs:
        mfc.connect()
    chromatograph.connect()
    # set chromatograph instrumental method to 'purge'. chromatograph will start to prepare itself
    chromatograph.set_method('purge')
    # set flow rates and calibrations of mass flow controllers
    for mfc, calibration, flow_rate in zip(mfcs, process_config.calibrations, process_config.flow_rates):
        mfc.set_calibration(calibration_num=calibration)
        mfc.set_flow_rate(flow_rate)
    # wait 10 minutes to purge the system
    time.sleep(10*60)
    # heat furnace to first measurement temperature, wait until temperature is reached
    furnace.set_temperature_control(True)
    furnace.set_temperature(temperature=process_config.temperatures[0])
    while True:
        current_temperature = furnace.get_temperature()
        if current_temperature >= process_config.temperatures[0]:
            break
        time.sleep(60)
    # wait until chromatograph is ready for analysis, start chromatograph purge afterwards
    while True:
        chromatograph_is_ready = chromatograph.is_ready_for_analysis()
        if chromatograph_is_ready:
            break
        time.sleep(60)
    chromatograph.start_analysis()
    # wait until analysis is actually started
    while True:
        chromatograph_working_status = chromatograph.get_working_status()
        if chromatograph_working_status is WorkingStatus.ANALYSIS:
            break
        time.sleep(60)
    # wait until chromatograph analysis is over, set passport values
    while True:
        chromatograph_working_status = chromatograph.get_working_status()
        if chromatograph_working_status is not WorkingStatus.ANALYSIS:
            chromatograph.set_passport(name=f'{today.strftime("%Y%m%d")}_purge', volume=0.5, dilution=1, purpose=ChromatogramPurpose.ANALYSIS, operator=process_config.operator, column='HaesepN/NaX', lab_name='Inorganic Nanomaterials')
            break
        time.sleep(60)
    # wait until chromatograph starts to prepare itself, change instrumental method to corresponding instrumental method
    while True:
        chromatograph_working_status = chromatograph.get_working_status()
        if chromatograph_working_status is WorkingStatus.PREPARATION or chromatograph_working_status is WorkingStatus.READY_FOR_ANALYSIS:
            chromatograph.set_method(process_config.chromatograph_method)
            break
        time.sleep(60)
    # for each temperature in measurement temperatures list:
        # wait until chromatograph is ready for analysis
        # read current furnace temperature
        # start chromatograph measurement
        # heat furnace to the next temperature
        # wait until temperature is reached
        # mark current time
        # wait until chromatograph analysis is over
        # set passport values
        # wait until isothermal dwell at measurement temperature is more than 30 minutes
    for temperature in process_config.temperatures[1:]:
        while True:
            if chromatograph.is_ready_for_analysis():
                break
            time.sleep(60)
        chromatogram_temperature = furnace.get_temperature()
        chromatograph.start_analysis()
        furnace.set_temperature(temperature=temperature)
        while True:
            current_temperature = furnace.get_temperature()
            if current_temperature >= temperature:
                break
            time.sleep(60)
        isothermal_start = time.time()
        while True:
            chromatograph_working_status = chromatograph.get_working_status()
            if chromatograph_working_status is not WorkingStatus.ANALYSIS:
                chromatograph.set_passport(name=f'{today.strftime("%Y%m%d")}_{process_config.sample_name}_{chromatogram_temperature:.1f}', volume=0.5, dilution=1, purpose=ChromatogramPurpose.ANALYSIS, operator=process_config.operator, column='HaesepN/NaX', lab_name='Inorganic Nanomaterials')
                break
            time.sleep(60)
        current_time = time.time()
        if current_time - isothermal_start < process_config.isothermal * 60:
            time.sleep(process_config.isothermal * 60 - (current_time - isothermal_start))
    # measure chromatogram at final temperature
    while True:
        if chromatograph.is_ready_for_analysis():
            break
        time.sleep(60)
    chromatogram_temperature = furnace.get_temperature()
    chromatograph.start_analysis()
    # wait until analysis is actually started
    while True:
        chromatograph_working_status = chromatograph.get_working_status()
        if chromatograph_working_status is WorkingStatus.ANALYSIS:
            break
        time.sleep(60)
    # turn off heating
    furnace.set_temperature(0)
    furnace.set_temperature_control(False)
    # set final chromatogram passport values
    while True:
        chromatograph_working_status = chromatograph.get_working_status()
        if chromatograph_working_status is not WorkingStatus.ANALYSIS:
            chromatograph.set_passport(name=f'{today.strftime("%Y%m%d")}_{process_config.sample_name}_{chromatogram_temperature:.1f}', volume=0.5, dilution=1, purpose=ChromatogramPurpose.ANALYSIS, operator=process_config.operator, column='HaesepN/NaX', lab_name='Inorganic Nanomaterials')
            break
        time.sleep(60)
    # start chromatograph cooldown
    while True:
        chromatograph_working_status = chromatograph.get_working_status()
        if chromatograph_working_status is WorkingStatus.PREPARATION or chromatograph_working_status is WorkingStatus.READY_FOR_ANALYSIS:
            chromatograph.set_method('cooling')
            break
        time.sleep(60)

if (__name__ == '__main__'):
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

    activation_parser = subparsers.add_parser('activate', help='activate catalyst using parameters provided in configuration file')
    activation_parser.set_defaults(func=activate)
    activation_parser.add_argument('--config', required=True, help='configuration file with activation parameters')

    measurement_parser = subparsers.add_parser('measure', help='gather chromatograms at different temperatures')
    measurement_parser.set_defaults(func=measure)
    measurement_parser.add_argument('--config', required=True, help='configuration file with measurement parameters')

    args = parser.parse_args()
    args.func(args)
