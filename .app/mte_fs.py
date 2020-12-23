#!/usr/bin/python3
#
# [MTE] Maintenance Task Execution: Filesystem processor
# @Description: 
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
import pathlib


class Filesystem:
  def __init__(self, core):
    self.core = core

  def create_directory(self, target, task=''):
    # Expect target to be pathlib.PosixPath object.
    # If it is not, create it.
    # If it is, use it.
    if type(target) is not pathlib.PosixPath:
      target = pathlib.Path(target)
    # 
    # Check if directory exists
    if target.exists():
      # Directory already exists, but can I write to it?
      if os.access(target, os.W_OK):
        return True
      else:
        self.core.log.add('Directory [' + str(target.absolute()) + '] already exists, but write access is denied. Please resolve.', 1)
        self.core.panic()
    else:
      # Check if parent exists
      if not  target.parent.exists():
        # Parent directory does not exist, create it before proceeding
        self.create_directory(target.parent, task)
      # Parent now exists.
      # Can I write in parent directory?
      # If yes, i can create the directory
      if os.access(target.parent, os.W_OK):
        # Yes
        self.core.log.add('Creating directory [' + str(target.absolute()) + '].', 4)
        command = 'mkdir ' + str(target.absolute())
        create_process = os.popen(command)
        response = create_process.read().strip().split("\n")
        return True
      else:
        if self.core.use_sudo(task):
          # Create directory using Sudo
          self.core.log.add('Using sudo for creating directory [' + str(target.absolute()) + '] and setting ownership to [' + self.core.get('runtime_user') + '].', 4)
          command = 'sudo mkdir ' + str(target.absolute())
          create_process = os.popen(command)
          response = create_process.read().strip().split("\n")
          # Change ownership of directory to runtime user
          command = 'sudo chown ' + self.core.get('runtime_user_id') + ':' + self.core.get('runtime_group_id') + ' ' + str(target.absolute())
          create_process = os.popen(command)
          response = create_process.read().strip().split("\n")
          return True
        else:
          self.core.log.add('Insufficient user rights to create directory [' + str(target.absolute()) + '].', 1)
          self.core.panic()

  def create_backup(self, source_path, target_path, task='core'):
    self.core.log.add('Creating backup of [' + source_path + '] to [' + target_path + '].', 5)