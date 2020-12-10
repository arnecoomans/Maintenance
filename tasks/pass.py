#!/usr/bin/python3
# [MTETASK]
#
# [MTE] Maintenance Task: Pass
# @Description: Don't do anything. 
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
    pass