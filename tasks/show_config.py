#!/usr/bin/python3
# [MTETASK]
#
# [MTE] Maintenance Task: Show Applied Config
# @Description: Display config as loaded into the system
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
sys.path.append(os.path.dirname(os.path.abspath(__file__) + "../.app/"))

import mte_task_dispatcher


class Task(mte_task_dispatcher.Task):
  def __init__(self, core, task_name):
    super().__init__(core, task_name) 

  def execute(self):
    # First, display Core Configuration
    self.core.log.add('# Core configuration', 0)
    for key, value in self.core.storage.items():
      self.core.log.add(" "*2 + key + ": " + str(value), 0)
    # Available tasks
    self.core.log.add('', 0)
    self.core.log.add("# Available tasks", 0)
    for value in self.core.dispatcher.available_tasks:
      self.core.log.add(" "*2 + "- " + value, 0)
    # Then print Arguments
    self.core.log.add('', 0)
    self.core.log.add("# Command Line Arguments", 0)
    for value in sys.argv[1:]:
      self.core.log.add(" "*2 + str(value), 0)
    # Then print Application Configuration
    self.core.log.add('', 0)
    self.core.log.add("# Application Configuration", 0)
    for key, value in self.core.config.storage.items():
      self.core.log.add(" "*2 + key + ": " + str(value) + " (" + str(type(value)) + ")", 0)