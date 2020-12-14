#!/usr/bin/python3
# [MTETASK]
#
# [MTE] Maintenance Task: Backup Config
# @Description: Create a backup of config files if the content
#               has changed since last backup
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
sys.path.append(os.path.dirname(os.path.abspath(__file__) + "../.app/"))

import mte_task_dispatcher

class Task(mte_task_dispatcher.Task):
  def __init__(self, core, task_name):
    # Run template task initiator
    super().__init__(core, task_name) 
    # List backup sources
    self.sources = []
    for item in self.core.config.get('sources', self.get_task_name()).split(","):
      self.sources.append(item.strip())
    

  # Everything that needs to be executed should be called from the
  # execute function. 
  def execute(self):
    pass
