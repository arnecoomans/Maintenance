#!/usr/bin/python3
#
# [MTE] Maintenance Task Execution: Task Dispatcher
# @Description: Dispatches Tasks and provides Task framework
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
import importlib

sys.path.append(os.path.dirname(os.path.abspath(__file__) + "../tasks-enabled/"))

class TaskDispatcher:
  def __init__(self, core):
    self.core = core
    self.storage = {}
    self.available_tasks = []
    self.inventorize_tasks()
    
    

  def inventorize_tasks(self):
    # Check for installed tasks on filesystem
    for filename in os.listdir(self.core.get('base_dir') + 'tasks-enabled/'):
      if os.path.splitext(filename)[1] == ".py":
        if self.is_marked_as_task(filename):
          self.available_tasks.append(os.path.splitext(filename)[0])
    
    if len(self.available_tasks) == 0:
      self.core.log.add('No tasks found in tasks-enabled/. Please check documentation in docs/tasks.md to enable tasks.', 1)
    else:
      self.core.log.add("Found available tasks: [" + ", ".join(self.available_tasks) + "].", 5)
  
  def is_marked_as_task(self, filename):
    # Tasks should have "# [MTETASK]" as second line in the file
    # This marks that the file is a task and it should be executed as task.
    # This prevents other files being ran in the task dispatcher.
    f=open(self.core.get('base_dir') + 'tasks-enabled/' + filename)
    lines=f.readlines()
    if len(lines) > 2:
      if lines[1].strip() == "# [MTETASK]":
        f.close()
        return True
    else:
      f.close()
      self.core.log.add("File " + filename + " in tasks-enabled directory is not a task. File should be removed.", 2)
      return False

  def is_task(self, task):
    if task in self.available_tasks:
      return True
    return False
    
  def dispatch(self, task):
    self.core.log.add("Dispatched task: [" + task + "].", 4)
    if self.is_task(task):
      module_task = importlib.import_module(task, package=None)
      task = module_task.Task(self.core, task)
      return True
    else:
      self.core.log.add("Task [" + task + "] not found. Skipping this task.", 1)
      return False

class Task:
  def __init__(self, core, task_name):
    self.core = core
    self.task_name = task_name
    self.storage = {}
    self.queue = []
    self.core.log.add("Loaded task: [" + self.get_task_name() + "].", 5)
    self.execute()
    if self.core.arguments.cleanup:
      self.cleanup()

  def get_task_name(self):
    return self.task_name
  
  def execute(self):
    self.core.log.add('Task execution for task [' + self.get_task_name() + '] called.', 5)
    self.core.log.add('No actions configured for [' + self.get_task_name() + '].', 4)
    pass

  def cleanup(self):
    self.core.log.add('Cleanup for task [' + self.get_task_name() + '] called.', 5)
    self.core.log.add('No cleanup configured for [' + self.get_task_name() + '].', 4)
    pass
  
  

    