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


  # Create Directory
  # @requires: target (pathlib.PosixPath object or string)
  # @optional: task
  # Creates the requested directory. If parent does not exist, parent is
  # created before proceeding. If sudo can be used to create directory,
  # the highest to-be-created directory is created using sudo and 
  # ownership is set to the runtime user and group.
  def create_directory(self, target, task=''):
    # Expect target to be pathlib.PosixPath object.
    # If it is not, create it.
    # If it is, use it.
    if type(target) is not pathlib.PosixPath:
      target = pathlib.Path(target)
    # 
    # Check if directory exists
    if target.exists():
      # Directory already exists
      if os.access(target, os.W_OK):
        # Directory is writable for current user.
        return True
      else:
        # Directory is not writable for current user.
        # Do not make changes to existing directories, this is a fatal error.
        self.core.log.add('Directory [' + str(target.absolute()) + '] already exists, but write access is denied. Please resolve.', 1)
        self.core.panic()
    # Directory does not yet exist
    else:
      # Check if parent exists
      if not  target.parent.exists():
        # Parent directory does not exist, create it before proceeding
        self.create_directory(target.parent, task)
      # Parent now exists.
      # Can runtime user write in parent directory?
      # If yes, runtime user can create the directory
      if os.access(target.parent, os.W_OK):
        # Yes
        self.core.log.add('Creating directory [' + str(target.absolute()) + '].', 4)
        command = 'mkdir ' + str(target.absolute())
        create_process = os.popen(command)
        response = create_process.read().strip().split("\n")
        return True
      # If parent directory is not writable for runtime user, 
      # try to create the directory using sudo.
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
    # Done.

  def create_backup(self, source_path, target_path, task='core'):
    self.core.log.add('Creating backup of [' + source_path + '] to [' + target_path + '].', 5)