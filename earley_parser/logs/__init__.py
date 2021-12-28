# Imports
import os
from os import path, remove
import json
import logging.config
# Logging, setup config file
print (os.getcwd())
if path.isfile("./logs.log"):
    remove("./logs.log")
with open("logging_configuration.json", 'r') as logging_configuration_file:
    config_dict = json.load(logging_configuration_file)

logging.config.dictConfig(config_dict)