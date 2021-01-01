#!/usr/bin/python3
#
# [MTE] Maintenance Task Execution: Logging processor
# @Description: 
#
# @Author: Arne Coomans
# @Contact: @arnecoomans on twitter
# @Version: 0.2.1
# @Date: 01-01-2021
# @Source: https://github.com/arnecoomans/maintenance/
#
#
# Import system modules
import os
import sys
from datetime import datetime
from colorama import Back, Fore, Style

class Logger:
  def __init__(self, core):
    self.core = core
    # Prepare log line cache
    self.storage = []
    self.welcome = self.get('log.welcome')
    self.header = self.get('log.header')
    # Display Level
    self.display_level = self.get('display_level')
    # Output methods
    self.output_methods = self.get('output_methods')
    # Message Types
    self.types = {
      0: 'content',
      1: 'critical',
      2: 'error',
      3: 'warning',
      4: 'notice',
      5: '-'*8,
    }
    
  def __del__(self):
    # Make sure that the log cache is flushed
    self.flush()

  def update_config(self):
    # Set display level
    self.set_display_level()
    # Set output methods
    self.output_methods = self.get('output_methods')
    if type(self.output_methods) is not list:
      output_methods = self.output_methods.split(',')
      self.output_methods = []
      for row in output_methods:
        self.output_methods.append(row.strip())

  def set_display_level(self, display_level=False):
    # Set display level
    if not display_level:
      # If no display level is supplied; get display level from config
      self.display_level = self.get('log.display_level')
    elif display_level == self.display_level:
      # If log level is not changing by this call, do nothing.
      pass
    elif type(display_level) is int and display_level >= 0 and display_level <= 5:
      # A new log level is supplied.
      self.add('Changed log display level from [' + str(self.display_level) + '] to [' + str(display_level) + '].', 5)
      self.display_level = display_level
    else:
      # Input error
      self.add('Invalid log display value: [' + str(display_level) + ']. Ignoring.', 4)
      


  def add(self, line, level=5, task=''):
    # Add the supplied line to the log cache in the specified format.
    # Enrich log message with date/time
    line = {'message': line,
            'datetime': datetime.now(),
            'time': datetime.now().strftime("%H:%M:%S"),
            'level': int(level),
            'task': task
           }
    self.storage.append(line)


  def flush(self):
    # Welcome message
    if self.welcome:
      if 'screen' in self.output_methods:
        self.print_welcome()
      if 'file' in self.output_methods:
        pass
      if 'db' in self.output_methods:
        pass
      self.welcome = False
    # Header
    if self.header:
      if 'screen' in self.output_methods:
        self.print_header()
      if 'file' in self.output_methods:
        pass
      if 'db' in self.output_methods:
        pass
      self.header = False
    # Loop through the logline cache
    for line in self.storage:
      #print(str(line['level']) + '--->' + str(self.display_level))
      if line['level'] <= self.display_level:
        if 'screen' in self.output_methods:
          self.print_line(line)
        if 'file' in self.output_methods:
          pass
        if 'db' in self.output_methods:
          pass
    self.storage = []
  
  # Output method: Screen
  def print_welcome(self):
    if self.display_level >= 4:
      print(str(self.core))
      print('[' + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + '] User ' + self.core.get('runtime_user') + ' is starting ' + self.core.get('base_dir') + sys.argv[0] + '.')
    if self.display_level >= 5:
      print('Runtime arguments supplied: ' + " ".join(sys.argv[1:]))
    if self.display_level >= 4:
      print('')
  def print_header(self):
    if self.display_level >= 4:
      print('[--TIME--] [--TYPE--] [----MESSAGE----')
  
  def get_importance(self, display_level):
    if display_level in self.types:
      type = self.types[display_level]
    else:
      type = self.types[5]
    # Ensure displayed severity is exactly 8 characters long
    type = type[0:8]
    while len(type) < 8:
      type = type + ' '
    return type[0:8]

  def print_line(self, line):
    output = []
    # Datetime field
    output.append('[' + line['time'] + ']')
    # Importance
    colour = ''
    colour_reset = ''
    if self.get('screen.colourize'):
      if line['level'] == 1:
        colour = Back.RED + Fore.WHITE
      elif line['level'] == 2:
        colour = Fore.RED
      elif line['level'] == 3:
        colour = Fore.MAGENTA
      elif line['level'] == 4:
        colour = Fore.YELLOW
      if line['level'] in [1, 2, 3, 4]:
        colour_reset = Style.RESET_ALL
    output.append('[' + colour + self.get_importance(line['level']) + colour_reset + ']')
    # Message
    output.append(line['message'])
    # Limit line length
    output = " ".join(output)
    while len(output) > self.get('screen.display_width'):
      print(output[0:self.get('screen.display_width')])
      output = " "*22 + output[self.get('screen.display_width'):].strip()
    print(output)

  # Get values from core or config
  def get(self, key):
    if hasattr(self.core, 'config'):
      # Config module has been loaded into core
      return self.core.config.get(key, 'log')
    else:
      # Get config from core storage
      # First check if the key starts with 'log.'.
      if key[:4] != 'log.':
        key = 'log.' + key
      return self.core.get(key)
