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
  def __init__(self, core, display_level=4):
    self.core = core
    self.storage = []
    self.display_level = display_level
    self.set_display_level(display_level)
    self.add_welcome()
  
  def __del__(self):
    self.display_log()
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
  def content(self, data='', importance=-1):
    self.storage.append( {'data': data, 
                          'importance': importance, 
                          'time': datetime.datetime.now()
                         } )

  def add_welcome(self):
    self.add('User ' + self.core.storage['runtime_user'] + ' is starting ' + self.core.storage['base_dir'] + sys.argv[0] + '.', 5)
    self.add('Arguments: ' + " ".join(sys.argv), 5)
    self.add(str(self.core), 5)
    self.add('',5)


  # Log displaying
  def get_usable_loglines(self):
    usable_log = []
    for row in self.storage:
      if row['importance'] < 0:
        usable_log.append(row['data'])
      elif row['importance'] <= self.display_level:
        usable_log.append(str(row['time']) + " [" + self.get_severity(row['importance']) + "] " + row['data'])
    return usable_log
  def get_header(self):
    return "[  DATE  ] [     TIME    ] [  TYPE  ] [     MESSAGE"


  def display_log(self):
    if self.display_level == 5:
      print(self.get_header())
    # cap row length at set value. Indent to match date and message type
    max_length = 128
    for row in self.get_usable_loglines():
      while len(row) > max_length:
        print(row[0:max_length])
        row = " "*38 + row[max_length:]
      print(row)
  def write_log_to_file(self):
    pass
    # @todo check if file is configured
    # @todo append to file

  def get_severity(self, display_level):
    if display_level == 0:
      severity = 'critical'
    elif display_level == 1:
      severity = 'error'
    elif display_level == 2:
      severity = 'warning'
    elif display_level == 3:
      severity = 'notice'
    elif display_level == 4:
      severity = ''
    else:
      severity = ''
    # Ensure displayed severity is exactly 8 characters long
    severity = severity[0:8]
    while len(severity) < 8:
      severity = severity + ' '
    return severity
    