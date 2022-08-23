#!/usr/bin/python

import time

import pycatalicism.config as device_config
from pycatalicism.furnace.owen_protocol import OwenProtocol
from pycatalicism.furnace.owen_tmp101 import OwenTPM101
from pycatalicism.mass_flow_controller.bronkhorst_f201cv import BronkhorstF201CV
from pycatalicism.chromatograph.chromatec_control_panel_modbus import ChromatecControlPanelModbus
from pycatalicism.chromatograph.chromatec_analytic_modbus import ChromatecAnalyticModbus
from pycatalicism.chromatograph.chromatec_crystal_5000 import ChromatecCrystal5000

# initialize furnace controller
furnace_controller_protocol = OwenProtocol(address=device_config.furnace_address, port=device_config.furnace_port, baudrate=device_config.furnace_baudrate, bytesize=device_config.furnace_bytesize, parity=device_config.furnace_parity, stopbits=device_config.furnace_stopbits, timeout=device_config.furnace_timeout, write_timeout=device_config.furnace_write_timeout, rtscts=device_config.furnace_rtscts)
furnace = OwenTPM101(device_name=device_config.furnace_device_name, owen_protocol=furnace_controller_protocol)

# initialize mass flow controllers
mfcs = list()
mfcs.append(BronkhorstF201CV(serial_address=device_config.mfc_He_serial_address, serial_id=device_config.mfc_He_serial_id, calibrations=device_config.mfc_He_calibrations))
mfcs.append(BronkhorstF201CV(serial_address=device_config.mfc_CO2_serial_address, serial_id=device_config.mfc_CO2_serial_id, calibrations=device_config.mfc_CO2_calibrations))
mfcs.append(BronkhorstF201CV(serial_address=device_config.mfc_H2_serial_address, serial_id=device_config.mfc_H2_serial_id, calibrations=device_config.mfc_H2_calibrations))

# initialize chromatograph
control_panel_modbus = ChromatecControlPanelModbus(modbus_id=device_config.control_panel_modbus_id, working_status_input_address=device_config.working_status_input_address, serial_number_input_address=device_config.serial_number_input_address, connection_status_input_address=device_config.connection_status_input_address, method_holding_address=device_config.method_holding_address, chromatograph_command_holding_address=device_config.chromatograph_command_holding_address, application_command_holding_address=device_config.application_command_holding_address)
analytic_modbus = ChromatecAnalyticModbus(modbus_id=device_config.analytic_modbus_id, sample_name_holding_address=device_config.sample_name_holding_address, chromatogram_purpose_holding_address=device_config.chromatogram_purpose_holding_address, sample_volume_holding_address=device_config.sample_volume_holding_address, sample_dilution_holding_address=device_config.sample_dilution_holding_address, operator_holding_address=device_config.operator_holding_address, column_holding_address=device_config.column_holding_address, lab_name_holding_address=device_config.lab_name_holding_address)
chromatograph = ChromatecCrystal5000(control_panel_modbus, analytic_modbus, device_config.methods)

# connect to devices
furnace.connect()
for mfc in mfcs:
    mfc.connect()
chromatograph.connect()

chromatograph.set_method('purge')

for mfc, calibration, flow_rate in zip(mfcs, process_config.calibrations, process_config.flow_rates):
    mfc.set_calibration(calibration_num=calibration)
    mfc.set_flow_rate(flow_rate)

furnace.set_temperature_control(True)
furnace.set_temperature(temperature=process_config.temperatures[0])
while True:
    current_temperature = furnace.get_temperature()
    if current_temperature >= process_config.temperatures[0]:
        break
    time.sleep(60)

while True:
    chromatograph_is_ready = chromatograph.is_ready_for_analysis()
    if chromatograph_is_ready:
        break
    time.sleep(60)

chromatograph.start_analysis()
while True:
    chromatograph_working_status = chromatograph.get_working_status()
    if chromatograph_working_status is not WorkingStatus.ANALYSIS:
        chromatograph.set_passport(name=f'{date}_purge', volume=0.5, dilution=1, purpose=ChromatogramPurpose.ANALYSIS, operator=args.operator, column='HaesepN/NaX', lab_name='Inorganic Nanomaterials')
        break
    time.sleep(60)

while True:
    chromatograph_working_status = chromatograph.get_working_status()
    if chromatograph_working_status is WorkingStatus.PREPARATION or chromatograph_working_status is WorkingStatus.READY_FOR_ANALYSIS:
        chromatograph.set_method('co-oxidation')
        break
    time.sleep(60)

for temperature in process_config.temperatures[1:]:
    while True:
        if chromatograph.is_ready_for_analysis():
            break
        time.sleep(60)
    current_temperature = furnace.get_temperature()
    chromatograph.start_analysis()
    furnace.set_temperature(temperature=temperature)
    while True:
        current_temperature = furnace.get_temperature()
        if current_temperature >= temperature:
            break
        time.sleep(60)
    isothermal_start = # current time in secs
    while True:
        chromatograph_working_status = chromatograph.get_working_status()
        if chromatograph_working_status is not WorkingStatus.ANALYSIS:
            chromatograph.set_passport(name=f'{date}_{process_config.sample_name}_{current_temperature}', volume=0.5, dilution=1, purpose=ChromatogramPurpose.ANALYSIS, operator=process_config.operator, column='HaesepN/NaX', lab_name='Inorganic Nanomaterials')
            break
        time.sleep(60)
    current_time = # current time in secs
    if current_time - isothermal_start < 30 * 60:
        time.sleep(30 * 60 - (current_time - isothermal_start))

furnace.set_temperature(0)
furnace.set_temperature_control(False)
while True:
    chromatograph_working_status = chromatograph.get_working_status()
    if chromatograph_working_status is WorkingStatus.PREPARATION or chromatograph_working_status is WorkingStatus.READY_FOR_ANALYSIS:
        chromatograph.set_method('cooling') # NB: make this method in Control Panel, add it to config.py
        break
    time.sleep(60)
