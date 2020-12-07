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

class Config:
  def __init__(self, core):
    self.core = core
    
  
  # Value handling
  def set_value(self, key, value):
    pass
  def has_value(self, key):
    pass
  def get_value(self, key):
    pass
  
  # Load configuration file
  def get_contents_of_configuration_file(self, file):
    pass
  def merge_configuration(self, additional_configuration):
    pass
