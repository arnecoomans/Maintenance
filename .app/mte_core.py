#!/usr/bin/python3
#
# [MTE] Maintenance Task Execution: Core Module
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
import time
import argparse


# Add local shared script directory to import path
#  Local function library
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import mte_config as mte_config

class Core:
  def __init__(self):
    # Internal data storage
    self.storage = {
      # Application details
      'name': '[MTE] Maintenance Task Execution',
      'tagline': 'Centralized management of maintenance tasks.',
      'help_url': 'https://github.com/arnecoomans/maintenance',
      'version': '0.0.0',
      'author': 'Arne Coomans',
      # Runtime details
      'start_time': time.time(),
      'base_dir': os.path.split(os.path.dirname(os.path.abspath(__file__)))[0] + '/',
      'default_configuration': 'config/maintenance.yml',
    }
    # Actual processing
    #   Load configuration file
    self.config = mte_config.Config(self, self.storage['default_configuration'])
    #   Parse command line arguments
    self.arguments = self.get_parsed_arguments()
    
  #
  #
  # Display Core information
  def __str__(self):
    return self.get_description()
  def get_version(self):
    return self.storage['version']
  def get_description(self):
    return self.storage['name'] + " v" + self.get_version() + ". "
  def get_tagline(self):
    return self.storage['tagline']
  def calculate_script_duration(self):
    return time.time() - self.storage['start_time']
  def get_script_duration(self):
    # Uses the start time defined in core.__init__ and current time to calculate running time.
    # Rounds output to 4 digits behind comma.
    return str(round(self.calculate_script_duration(), 4)) + " seconds"
  
  #
  #
  # Parse Command Line Arguments
  def get_parsed_arguments(self):
    # Set welcome text when displaying help text
    parser = argparse.ArgumentParser(description=self.get_description() + self.get_tagline(), 
                                     epilog="By " + self.storage['author'] + ". Have an issue or request? Use " + self.storage['help_url'])
    # List Arguments
    #   Task Selection
    parser.add_argument("-t", "--task",
                        help="* Select task to be executed.",
                        required=True)
    #   Task Arguments
    parser.add_argument("-arg", "--argument",
                        help="Arguments passed to task")
    #   Target Selection
    #   Overrides target defined by configuration module.
    parser.add_argument("--target", 
                        help="Override backup target directory")
    # Configuration File
    #   Add a configuration file to be loaded that overrides previous configuration. 
    #   Default configuration is still processed.
    parser.add_argument("--config", 
                        help="Override config file (yml)",
                        action="append")
    # Logging
    #   Define the amount of data that should be processed by the logging module. Overrides
    #   the value in configuration.
    parser.add_argument("-l", "--logging", 
                        help="Override logging level, [none] 0 -- 5 [all]", 
                        type=int, 
                        choices=[0,1,2,3,4,5])
    # Parse arguments
    arguments = parser.parse_args()
    # Process parsed arguments
    # Return parsed arguments
    return arguments