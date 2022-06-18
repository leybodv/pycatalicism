import logging
import serial

# Dictionary of logging levels of corresponding classes
logging_levels = {
                'FurnaceData'               :    logging.INFO,
                'Owen_TPM101_Controller'    :    logging.DEBUG,
                'SimpleTempTimeExporter'    :    logging.INFO,
                'SimpleTempTimePlotter'     :    logging.INFO
                }

# Furnace controller type
controller_type = 'Owen_TPM101'
# Furnace controller port name and corresponding port parameters (baudrate, bytesize, parity, stopbits) which must be the same as configured on controller device
port = '/dev/ttyUSB0'
baudrate = 19200
bytesize = serial.EIGHTBITS
parity = serial.PARITY_NONE
stopbits = serial.STOPBITS_ONE
# Time in seconds to wait for the response from the device
timeout = 0.1
# Time in seconds to wait while message is sent to the device
write_timeout = None
# Enable/disable hardware flow control
rtscts = False
# Address of Owen TRM101 device
address = 0
# Time interval between message was sent to the device and controller was sent the answer in ms
rsdl = 20
# Address length in bits. Can be 8 or 11 bits, however only 8 bits is supported now
address_len = 8

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
