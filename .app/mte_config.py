#!/usr/bin/python3
#
# [MTE] Maintenance Task Execution: Configuration loader
# @Description: Loads configuration from yaml files
#
# @Author: Arne Coomans
# @Contact: @arnecoomans on twitter
# @Version: 0.2.0
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
  def set(self, key, value, prefix=[]):
    # Ensure prefix is a list.
    if type(prefix) is not list:
      prefix = [str(prefix)]
    # If the stored value is a dict, it should be flattened. 
    if type(value) is dict:
      for subkey, subvalue in value.items():
        self.set(subkey, subvalue, prefix + [key])
    # Store the (key prefix,) key and value
    else:
      if type(value) == str:
        value = value.strip()
      self.storage[".".join(prefix + [key])] = value
    # Done

  def get(self, key, prefix=[], exact=False):
    # First ensure that prefix is a list.
    if type(prefix) is not list:
      prefix = [prefix]
    # Ensure key is all lowercase.
    key = key.lower()
    # if no prefix is supplied, try for an exact match
    if len(prefix) == 0:
      if key in self.storage:
        return self.storage[key]
      elif key in self.core.storage:
        # Check if key is in core storage (hardcoded fallback configuration)
        return self.core.storage[key]
      else:
        return ''
    else:
      # A prefix is supplied.
      # Check if [prefix.key] exists
      if '.'.join(prefix + [key]) in self.storage:
        return self.storage['.'.join(prefix + [key])]
      elif '.'.join(['task'] + prefix + [key]) in self.storage:
        return self.storage['.'.join(['task'] + prefix + [key])]
      elif not exact and key in self.storage:
        return self.storage[key]
      elif not exact and key in self.core.storage:
        # Check if key is in core storage (hardcoded fallback configuration)
        return self.core.storage[key]
      else:
        return ''
    
  
  # Read Yaml configuration
  def get_contents_of_configuration_file(self, file):
    self.core.log.add('Parsing configuration file: [' + file + '].', 5)
    file = self.core.get('base_dir') + file
    # Validate that file actually exists
    if not os.path.isfile(file):
      self.core.log.add('Could not locate configuration file [' + file + ']. Skipping this file.', 3)
    # Validate that configuration file is .yml, .yaml or .conf
    elif os.path.splitext(file)[1] not in ['.yml', '.yaml', '.conf']:
      self.core.log.add('Could not process configuration file [' + file + ']. Extention not supported.', 1)
    else:
      self.configuration_files.append(file)
      # Load yaml configuration file
      with open(file) as configuration_file:
        document = yaml.full_load(configuration_file)
        # Maintenance process configuation should be stored under "maintenance"
        document = document['maintenance']
        # Store each key and value into the configuration storage container
        for key, value in document.items():
          if key == "import":
            value = value.split(",")
            for file in value:
              self.get_contents_of_configuration_file(file.strip())
          self.set(key, value)
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

  def get_runtime_arguments(self):
    # Check if runtime arguments are supplied for this task
    if self.core.arguments.argument is not None:
      # Arguments are supplied as a continious string. Split this into key/value pairs
      arguments = self.core.arguments.argument.split(",")
      # Walk through each argument-pair
      for argument in arguments:
        task = ''
        # I made the mistake of using = and : to assign, meaning i couldn't choose.
        # I think : is preferred, so let's replace = by : to allow both characters.
        argument.replace('=',':')
        argument = argument.split(':')
        argument[0] = argument[0].strip()
        # If the key contains a ., assume this is to assign sub-keys for a task.
        if '.' in argument[0]:
          task = argument[0].split('.')[0]
          argument[0] = 'task.' + argument[0]
        # If the string value True or False are parsed, change to the apropriate 
        # bool values
        if argument[1].lower() == "true":
          argument[1] = True
        elif argument[1].lower() == "false":
          argument[1] = False
        elif argument[1].lower() == "none":
          argument[1] = None
        elif str(int(argument[1])) == argument[1]:
          argument[1] = int(argument[1])
        else:
          argument[1] = argument[1].strip()
        # Store the command line supplied configuration
        if task == '':
          self.core.log.add("Command line argument supplied: ["+ str(argument[0]) + ": " + str(argument[1]) + "].", 4)
          self.set(argument[0], argument[1])
        elif task in self.core.dispatcher.available_tasks:
          self.core.log.add("Command line argument supplied: [" + str(argument[0]) + ": " + str(argument[1]) + "].", 4)
          self.set(argument[0], argument[1])
