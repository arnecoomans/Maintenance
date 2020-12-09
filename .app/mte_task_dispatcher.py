#!/usr/bin/python3
#
# [MTE] Maintenance Task Execution: Task Dispatcher
# @Description: Dispatches Tasks and provides Task framework
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

class TaskDispatcher:
  def __init__(self, core):
    self.core = core
    self.storage = {}

class Task:
  def __init__(self, core):
    self.core = core
    self.storage = {}
    self.queue = []
    self.core.log.add("Dispatched task " + self.get_task_name(), 4)
    
  def get_task_name(self):
    return "test"
    # @todo
    #return self.core.dispatcher.get_task()