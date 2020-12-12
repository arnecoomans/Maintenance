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
import getpass


# Add local shared script directory to import path
#  Local function library
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import mte_logging as mte_logging
import mte_config as mte_config
import mte_task_dispatcher as mte_task_dispatcher


class Core:
  def __init__(self):
    # Internal data storage
    self.tasks = []
    self.storage = {}
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
      'runtime_user': getpass.getuser(),
      'has_root_privilage': self.has_root_privilage(),
    }
    # Actual processing
    #   Prepare logging
    self.log = mte_logging.Logger(self)
    #   Load configuration file
    self.config = mte_config.Config(self, self.storage['default_configuration'])
    self.log.set_display_level(self.config.get_value('logging'))
    #   Parse command line arguments
    self.arguments = self.process_parsed_arguments( self.get_parsed_arguments() )
    #   Check if at least some configuration is loaded

    # Prepare Task Dispatcher
    self.dispatcher = mte_task_dispatcher.TaskDispatcher(self)
    self.config.get_runtime_arguments()

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
  

  def get(self, key):
    if key in self.storage:
      return self.storage[key]
    else:
      return False
  
  # SUDO AND ROOT
  def has_root_privilage(self):
    if os.getuid() == 0:
      return True
    else:
      return False

  def get_sudo(self, task=''):
    if (self.config.get_value('can_use_sudo') and 
         (self.config.get_value('run_as_root') or 
          self.config.get_value('run_as_root', ['task', task])) 
        and not self.has_root_privilage()):
      return "sudo "
    return ""
  
  # System command execution
  def run_command(self, command, task):
    command = self.get_sudo(task) + command
    self.log.add('Executing os-level command: [' + command + "].")
    command = os.popen(command)
    return command.read().strip().split("\n")
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
                        action="append",
                        required=True)
    #   Task Arguments
    parser.add_argument("-arg", "--argument",
                        help="Arguments passed to task",
                        )
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
    # Return parsed arguments
    return arguments
  def process_parsed_arguments(self, arguments):
    # Task selection
    #   Task arguments
    if arguments.task is not None:
      self.tasks = arguments.task
    # Target selection
    if arguments.target is not None:
      self.log.add("Command line arguments changed backup target from " + self.config.get_value('backup_target') + " to " + arguments.target + ".", 4)
      self.config.set_value('backup_target', arguments.target)
    # Configuration File selection
    if arguments.config is not None:
      for file in arguments.config:
        self.log.add("Command line arguments added " + file + " to configuration processer.", 4)
        self.config.get_contents_of_configuration_file(file)
    # Logging
    if arguments.logging is not None:
      if arguments.logging is not self.log.display_level:
        self.log.add('Command line arguments changed log display level from ' + str(self.log.display_level) + " to " + str(arguments.logging) + ".", 4)
        self.config.set_value('logging', arguments.logging)
        self.log.set_display_level(arguments.logging)
    return arguments