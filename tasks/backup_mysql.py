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
    self.command_line_commands = {
      'get_list_of_all_databases': 'mysql -e \'show databases\' -s --skip-column-names',
    }
    super().__init__(core, task_name)
    

  def execute(self):
    self.core.log.add(str(self.remove_ignored_databases_from_list(self.get_list_of_all_databases())), 0)
  
  def get_list_of_all_databases(self):
    return self.core.run_command(self.command_line_commands['get_list_of_all_databases'], self.get_task_name())
  
  def remove_ignored_databases_from_list(self, list):
    result = []
    for database in list:
      if database not in self.core.config.get_value('ignored_databases', [self.get_task_name()]).split(", ") and len(database) > 0:
        result.append(database)
    return result
