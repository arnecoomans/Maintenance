#!/usr/bin/python3
#
# [MTE] Maintenance Task Execution: Logging processor
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
import datetime

class Logger:
  def __init__(self, core, display_level=5):
    self.storage = []
    self.display_level = display_level
    self.set_display_level(display_level)
  
  def __del__(self):
    # @todo move this to a function
    for row in self.storage:
      if row['importance'] <= self.display_level:
        print(str(row['time']) + " [" + self.get_severity(row['importance']) + "] " + row['data'])
  # Setting display level
  # Display level can be set in a range between 0 and 5. 
  # Allow display level to be set during processing. 
  # Allow display level to be set without errors
  def set_display_level(self, display_level):
    # Display level should be integer. If not:
    if type(display_level) is not int:
      # If False or None are supplied, assume display level 0
      if display_level is False or display_level is None:
        display_level = 0
      # If a different value is given, assume level 5
      else: 
        display_level = 5
    # If an out-of-bounds display level is given, assume closest in-bound value
    elif display_level < 0:
      display_level = 0
    elif display_level > 5:
      display_level = 5
    # Display level has been set, this can be logged
    if self.display_level != display_level:
      self.add("Set log display level to [" + str(display_level) + "]", 4)
      self.display_level = display_level
  
  def add(self, data, importance=5):
    self.storage.append( {'data': data, 
                          'importance': importance, 
                          'time': datetime.datetime.now()
                         } )

  # Log displaying
  def get_severity(self, display_level):
    if display_level == 0:
      severity = 'fatal'
    elif display_level == 1:
      severity = 'critical'
    elif display_level == 2:
      severity = 'error'
    elif display_level == 3:
      severity = 'warning'
    elif display_level == 4:
      severity = 'notice'
    elif display_level == 5:
      severity = 'remark'
    # Ensure displayed severity is exactly 8 characters long
    severity = severity[0:8]
    while len(severity) < 8:
      severity = severity + ' '
    return severity
    