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
import pprint

class Config:
  def __init__(self, core, configuration_file):
    self.core = core
    self.storage = {}
    self.get_contents_of_configuration_file(configuration_file)
    print()
    pprint.pprint(self.storage)

  # Storage access functions
  def set_value(self, key, value, prefix=[]):
    if type(prefix) is not list:
      prefix = [prefix]
    if type(value) is dict:
      for subkey, subvalue in value.items():
        self.set_value(subkey, subvalue, prefix + [key])
    else:
      self.storage[".".join(prefix + [key])] = value

  def get_value(self, key):
    pass
  
  def has_value(self, key):
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



    #self.config = self.get_contents_of_configuration_file(self.core.data['base_dir'] + 
    #                                                      core.data['default_configuration'])
    #print("STORAGE:")
    #print(self.storage)
  
  # Value handling
  #def set_value(self, key, value, key_prefix=[]):
  #  print(key_prefix)
  #  key_prefix.append(key)
  #  print(".".join(key_prefix) + ": " + str(value))
  #  if type(value) is dict:
  #    for subkey, subvalue in value.items():
  #      self.set_value(subkey, subvalue, key_prefix)
  #  else:
  #    self.storage[".".join(key_prefix)] = value

  #def has_value(self, key):
  #  pass
  #def get_value(self, key):
  #  pass
  
  # Load configuration file
  #def get_contents_of_configuration_file(self, file):
  #  print('reading configuration from ' + file)
    # Validate that configuration file is .yml, .yaml or .conf
    # @todo
    # Load yaml configuration file
  #  with open(file) as configuration_file:
  #    document = yaml.full_load(configuration_file)
      # Maintenance process configuation should be stored under "maintenance"
  #    document = document['maintenance']
  #    print("YAML")
  #    print(yaml.dump(document))
  #    for key, value in document.items():
  #      print ("Storing " + key + ": " + str(value))
  #      self.set_value(key, value, [])
      #  if type(value) is dict:
      #    print(key + " has dict as value")
      #  print(str(type(key)) + " " + key + ": " + str(type(value)) + " " + str(value))
    #with open(os.path.dirname(os.path.abspath(__file__)) + configuration_file) as file:
    #  documents = yaml.full_load(file)
    #  for key, value in documents.items():
    #    if key == 'maintenance':
    #      self.values = value
    #      **/
  
  #def merge_configuration(self, additional_configuration):
  #  pass
