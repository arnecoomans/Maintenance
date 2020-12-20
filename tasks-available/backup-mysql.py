#!/usr/bin/python3
# [MTETASK]
#
# [MTE] Maintenance Task: Pass
# @Description: Don't do anything. 
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
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__) + "../.app/"))

import mte_task_dispatcher


class Task(mte_task_dispatcher.Task):
  def __init__(self, core, task_name):
    self.command_line_commands = {
      'get_list_of_all_databases': 'mysql -e \'show databases\' -s --skip-column-names',
      'dump_database': 'mysqldump %database% %gzip% > %target%%filename%'
    }
    super().__init__(core, task_name)
    

  def execute(self):
    # Creating a backup of all databases
    self.core.log.add('Getting list of databases to be backed up', 4)
    databases = self.remove_ignored_databases_from_list(self.get_list_of_all_databases())
    self.core.log.add('Found databases: [' + ', '.join(databases) + '].', 5)
    for database in databases:
      self.dump_database(database)  
  def get_list_of_all_databases(self):
    return self.core.run_command(self.command_line_commands['get_list_of_all_databases'], self.get_task_name())
  
  def remove_ignored_databases_from_list(self, list):
    result = []
    for database in list:
      if database not in self.core.config.get('ignored_databases', self.get_task_name()).split(", ") and len(database) > 0:
        result.append(database)
    return result
  
  def dump_database(self, database):
    # process command
    gzip = ''
    command = self.command_line_commands['dump_database']
    command = command.replace('%database%', database)
    if self.core.get_gzip(self.get_task_name()):
      gzip = '| gzip '
    command = command.replace('%gzip%', gzip)
    command = command.replace('%target%', self.core.get_target(self.get_task_name()))
    # Filename
    filename = database
    
    # Check if task configuration holds date_time_format
    if self.core.config.get('date_time_format', self.get_task_name()):
      filename += '_'
      filename += self.core.get_date_time(self.get_task_name())
    filename += '.sql'
    if self.core.get_gzip(self.get_task_name()):
      filename += '.tar.gz'
    command = command.replace('%filename%', filename)
    self.core.log.add('Backing up [' + database + '] to [' + self.core.get_target(self.get_task_name()) + filename + ']', 4)
    self.core.run_command(command, self.get_task_name())
    
