#!/usr/bin/python3
#
# [MTE] Maintenance Task Execution: Configuration loader
# @Description: 
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
import pprint #@todo remove debugging feature 

class Config:
  def __init__(self, configuration_file):
    self.storage = {}
    self.get_contents_of_configuration_file(configuration_file)
    # @todo remove following debugging lines
    #print()
    #pprint.pprint(self.storage)

  # Storage access functions
  def set_value(self, key, value, prefix=[]):
    if type(prefix) is not list:
      prefix = [prefix]
    if type(value) is dict:
      for subkey, subvalue in value.items():
        self.set_value(subkey, subvalue, prefix + [key])
    else:
      self.storage[".".join(prefix + [key])] = value
    return True

  def get_value(self, key):
    # @todo
    pass
  
  def has_value(self, key):
    # @todo
    pass
  
  # Read Yaml configuration
  def get_contents_of_configuration_file(self, file):
    # Validate that configuration file is .yml, .yaml or .conf
    # @todo
    # Load yaml configuration file
    with open(file) as configuration_file:
      document = yaml.full_load(configuration_file)
      # Maintenance process configuation should be stored under "maintenance"
      document = document['maintenance']
  #    print("YAML")
  #    print(yaml.dump(document))
      for key, value in document.items():
        self.set_value(key, value)
