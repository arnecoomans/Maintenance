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
    self.core.log.content('# Core configuration')
    for key, value in self.core.storage.items():
      self.core.log.content(" "*2 + key + ": " + str(value))
    # Available tasks
    self.core.log.content()
    self.core.log.content("# Available tasks")
    for value in self.core.dispatcher.available_tasks:
      self.core.log.content(" "*2 + "- " + value)
    # Then print Arguments
    self.core.log.content()
    self.core.log.content("# Command Line Arguments")
    for value in sys.argv[1:]:
      self.core.log.content(" "*2 + str(value))
    # Then print Application Configuration
    self.core.log.content()
    self.core.log.content("# Application Configuration")
    for key, value in self.core.config.storage.items():
      self.core.log.content(" "*2 + key + ": " + str(value))