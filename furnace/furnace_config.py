import logging
logging_levels = {
                'FurnaceData'               :    logging.INFO,
                'Owen_TPM101_Controller'    :    logging.INFO,
                'SimpleTempTimeExporter'    :    logging.INFO,
                'SimpleTempTimePlotter'     :    logging.INFO
                }

controller_type = ''
port = ''
baudrate = 
bytesize = 
parity = 
stopbits = 
timeout = 
write_timeout = 
rtscts = 
address = 
rsdl = 
address_len = 

plotter_type = ''
fig_dpi = 96
fig_width = 800 / fig_dpi
fig_height = 600 / fig_dpi

exporter_type = ''
