#!/usr/bin/python3
# [MTETASK]
#
# [MTE] Maintenance Task: Pass
# @Description: Doesn't do anything. Great for testing and 
#  to use as task template.
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

  # Everything that needs to be executed should be called from the
  # execute function. 
  def execute(self):
    for line in self.core.run_command('git pull', self.get_task_name()):
      self.core.log.add('Self-update: ' + line, 4)
