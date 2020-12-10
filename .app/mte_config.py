#!/usr/bin/python3
#
# [MTE] Maintenance Task Execution: Configuration loader
# @Description: Loads configuration from yaml files
#
# @Author: Arne Coomans
# @Contact: @arnecoomans on twitter
# @Version: 0.0
# @Date: 01-01-2021
# @Source: https://github.com/arnecoomans/maintenance/
#
#
# Import system modules
import os
import sys
import yaml

class Config:
  def __init__(self, core, configuration_file):
    self.core = core
    self.configuration_files = []
    self.storage = {}
    self.get_contents_of_configuration_file(configuration_file)

  # Storage access functions
  def set_value(self, key, value, prefix=[]):
    # Ensure prefix is a list.
    if type(prefix) is not list:
      prefix = [str(prefix)]
    # If the stored value is a dict, it should be flattened. 
    if type(value) is dict:
      for subkey, subvalue in value.items():
        self.set_value(subkey, subvalue, prefix + [key])
    # Store the (key prefix,) key and value
    else:
      self.storage[".".join(prefix + [key])] = value
    # Done

  def get_value(self, key, prefix=[]):
    if ".".join(prefix + [key]) in self.storage:
      return self.storage[".".join(prefix + [key])]
    else:
      return ''
    
  def has_value(self, key):
    # @todo
    pass
  
  # Read Yaml configuration
  def get_contents_of_configuration_file(self, file):
    # Validate that configuration file is .yml, .yaml or .conf
    if os.path.splitext(file)[1] not in ['.yml', '.yaml', '.conf']:
      self.core.log.add('Could not process configuration file ' + file + '. Extention not supported.', 1)
    else:
      self.configuration_files.append(file)
      # Load yaml configuration file
      with open(file) as configuration_file:
        document = yaml.full_load(configuration_file)
        # Maintenance process configuation should be stored under "maintenance"
        document = document['maintenance']
        # Store each key and value into the configuration storage container
        for key, value in document.items():
          self.set_value(key, value)
    # Done

  # Check if configuration files have been processed. 
  #   Because not processing a configuration file is not fatal, because 
  #   multiple configuration files can be processed, we need to verify that a
  #   configuration file has been processed. The processed configuration files
  #   are accounted for in the self.configuration_files list.
  def has_processed_configuration_files(self):
    if len(self.configuration_files) > 0:
      return True
    else:
      return False