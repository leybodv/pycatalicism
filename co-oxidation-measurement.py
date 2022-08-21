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

