#!/usr/bin/python

import time

import pycatalicism.config as device_config
import pycatalicism.co_oxidation_config as process_config
from pycatalicism.furnace.owen_protocol import OwenProtocol
from pycatalicism.furnace.owen_tmp101 import OwenTPM101
from pycatalicism.mass_flow_controller.bronkhorst_f201cv import BronkhorstF201CV

# initialize furnace controller
furnace_controller_protocol = OwenProtocol(address=device_config.furnace_address, port=device_config.furnace_port, baudrate=device_config.furnace_baudrate, bytesize=device_config.furnace_bytesize, parity=device_config.furnace_parity, stopbits=device_config.furnace_stopbits, timeout=device_config.furnace_timeout, write_timeout=device_config.furnace_write_timeout, rtscts=device_config.furnace_rtscts)
furnace_controller = OwenTPM101(device_name=device_config.furnace_device_name, owen_protocol=furnace_controller_protocol)

# initialize mass flow controllers
mfcs = list()
mfcs.append(BronkhorstF201CV(serial_address=device_config.mfc_He_serial_address, serial_id=device_config.mfc_He_serial_id, calibrations=device_config.mfc_He_calibrations))
mfcs.append(BronkhorstF201CV(serial_address=device_config.mfc_CO2_serial_address, serial_id=device_config.mfc_CO2_serial_id, calibrations=device_config.mfc_CO2_calibrations))
mfcs.append(BronkhorstF201CV(serial_address=device_config.mfc_H2_serial_address, serial_id=device_config.mfc_H2_serial_id, calibrations=device_config.mfc_H2_calibrations))

# connect to devices
furnace_controller.connect()
for mfc in mfcs:
    mfc.connect()

# set mass flow controllers calibrations and flow rates
for mfc, calibration, flow_rate in zip(mfcs, process_config.calibrations, process_config.activation_flow_rates):
    mfc.set_calibration(calibration_num=calibration)
    mfc.set_flow_rate(flow_rate)

# wait system to be purged with gases for 10 minutes
time.sleep(secs=10*60)

# heat furnace to activation temperature, wait until temperature is reached
furnace_controller.set_temperature_control(True)
furnace_controller.set_temperature(process_config.activation_temperature)
while True:
    current_temperature = furnace_controller.get_temperature()
    if current_temperature >= process_config.acrivation_temperature:
        break
    time.sleep(secs=60)

# dwell for activation duration time
time.sleep(secs=process_config.activation_duration*60)

# turn off heating, wait until furnace is cooled down to post_temperature
furnace_controller.set_temperature(0)
furnace_controller.set_temperature_control(False)
while True:
    current_temperature = furnace_controller.get_temperature()
    if current_temperature <= process_config.post_temperature:
        break
    time.sleep(secs=60)

# change gas flow rates to post activation values
for mfc, flow_rate in zip(mfcs, process_config.post_flow_rates):
    mfc.set_flow_rate(flow_rate)
