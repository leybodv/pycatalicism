#!/usr/bin/python

import pycatalicism.config as device_config
from pycatalicism.furnace.owen_protocol import OwenProtocol
from pycatalicism.furnace.owen_tmp101 import OwenTPM101
from pycatalicism.mass_flow_controller.bronkhorst_f201cv import BronkhorstF201CV

# initialize furnace controller
furnace_controller_protocol = OwenProtocol(address=device_config.furnace_address, port=device_config.furnace_port, baudrate=device_config.furnace_baudrate, bytesize=device_config.furnace_bytesize, parity=device_config.furnace_parity, stopbits=device_config.furnace_stopbits, timeout=device_config.furnace_timeout, write_timeout=device_config.furnace_write_timeout, rtscts=device_config.furnace_rtscts)
furnace_controller = OwenTPM101(device_name=device_config.furnace_device_name, owen_protocol=furnace_controller_protocol)

# initialize mass flow controllers
mfc_He = BronkhorstF201CV(serial_address=device_config.mfc_He_serial_address, serial_id=device_config.mfc_He_serial_id, calibrations=device_config.mfc_He_calibrations)
mfc_CO2 = BronkhorstF201CV(serial_address=device_config.mfc_CO2_serial_address, serial_id=device_config.mfc_CO2_serial_id, calibrations=device_config.mfc_CO2_calibrations)
mfc_H2 = BronkhorstF201CV(serial_address=device_config.mfc_H2_serial_address, serial_id=device_config.mfc_H2_serial_id, calibrations=device_config.mfc_H2_calibrations)

# connect to devices
furnace_controller.connect()
mfc_He.connect()
mfc_CO2.connect()
mfc_H2.connect()

mfc_He.set_calibration(calibration_num=0)

