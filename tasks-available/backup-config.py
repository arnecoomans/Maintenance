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
# @info https://docs.python.org/3/library/sqlite3.html
#
# Import system modules
import os
import sys
from datetime import datetime

import sqlite3

import hashlib
import pathlib


sys.path.append(os.path.dirname(os.path.abspath(__file__) + "../.app/"))

import mte_task_dispatcher

class Task(mte_task_dispatcher.Task):
  def __init__(self, core, task_name):
    self.db = None
    self.cursor = None
    self.dbtable = 'files'
    # List backup sources
    self.sources = []
    self.hashes = {}
    for item in core.config.get('backup_sources', task_name).split(","):
      self.sources.append(item.strip())
    self.queries = {
      'create_table': 'CREATE TABLE ' + self.dbtable + ' (file text, hash text, date timestamp, backup_location text)',
      'select_file': 'SELECT * FROM ' + self.dbtable + ' WHERE file=? ORDER BY rowid DESC',
      'insert_file': 'INSERT INTO ' + self.dbtable + ' VALUES (?, ?, ?, ?)',
      'update_file': 'update files set backup_location = ? where hash = ?',
    }
    # Run template task initiator
    super().__init__(core, task_name) 

  def execute(self):
    for source in self.sources:
      self.core.log.add('Processing [' + source + '].', 4, self.get_task_name())
      self.process(source)
      self.core.log.flush()




  # Process backup locations
  def process(self, source, recursive=False, base=None):
    # Check type of input
    if type(source) is not pathlib.PosixPath:
      source = pathlib.Path(source)
    # Process Recursive Marker
    if recursive:
      self.core.log.add('[r] Processing [' + str(source).replace(str(base), '') + ']', 4, self.get_task_name())
    if source.stem == '[r]':
      self.core.log.add(' Recursive marker found. Processing', 5, self.get_task_name())
      recursive = True
      source = source.parent
    # Check if source location can be read
    #if not os.access(source, os.R_OK):
    #  self.core.log.add('No read access in [' + str(source.parent) + ']. See documentation for more info. For now, please run script as root.', 1)
    #  self.core.panic()
    # Check if source is a file
    #elif source.is_file():
    if self.core.fs.is_file(source, self.get_task_name()):  
      # Core backup process handles the usage of sudo when the
      # source is not accessible for the current user.
      self.create_backup(source, base)
    #if source.is_dir():
    elif self.core.fs.is_dir(source, self.get_task_name()):
      # Process base
      if base is None:
        base = source
      #for child in source.iterdir():
      for child in self.core.fs.iterdir(source, self.get_task_name()):
        if self.core.fs.is_dir(child, self.get_task_name()):
          if not self.is_ignored(child):
            self.process(child, recursive, base)
        #elif child.is_file():
        elif self.core.fs.is_file(child, self.get_task_name()):
          self.create_backup(child, base)
    else:
      self.core.log.add('Location [' + str(source) + '] is neither file or directory. Skipping. ' + str(self.core.fs.is_dir(source, self.get_task_name())), 4, self.get_task_name())

  def create_backup(self, source, base):
    # Check type of input
    if type(source) is not pathlib.PosixPath:
      source = pathlib.Path(source)
    # Check if file is not ignored
    if not self.is_ignored(source):
      # Check if file hash is not known
      if not self.hashes_match(source):
        target = self.get_target_filename(source, base)
        target = self.core.fs.create_backup(source, target, self.get_task_name()) 
        self.store_hash(source, self.get_file_hash(source), target)
  
  def hashes_match(self, source):
    # Check type of input
    if type(source) is not pathlib.PosixPath:
      source = pathlib.Path(source)
    source_hash = self.get_file_hash(source)
    stored_hash = self.get_stored_hash(source)
    if stored_hash is not None and source_hash == stored_hash[1]:
      self.core.log.add('[' + str(source) + '] last change: [' + stored_hash[2] + '].', 5, self.get_task_name())
      if not self.core.fs.file_exists(stored_hash[3], self.get_task_name()):
        self.core.log.add('Backup of [' + str(source) + '] not found. Creating new backup.', 4, self.get_task_name())
        return False
      return True
    else:
      return False
    



      

  def is_ignored(self, file):
    ignored = []
    if type(file) is not pathlib.PosixPath:
      file = pathlib.Path(file)
    for item in self.core.config.get('ignored', self.get_task_name()).split(','):
      ignored.append(item.strip())
    if file.name in ignored:
      return True
    return False


  def get_target_filename(self, source, base):
    source = str(source)
    if base is None:
      base = ''
    elif type(base) is pathlib.PosixPath:
      base = str(base)
    if source[0:len(base)] == base:
      source = [base, source[len(base):]]
    else:
      source = ['', source]
    target  = self.core.config.get('backup_target', self.get_task_name())
    if target[:-1] != '/':
      target += '/'
    target += self.core.config.get('target_subdirectory', self.get_task_name())
    if target[:-1] != '/':
      target += '/'
    target += source[0].replace('/', '_') + '/' + source[1].replace('/', '_')
    #self.core.log.add('T: ' + target)
    return target
  

  # HASHING
  # Get Hash Type
  def get_hash_type(self):
    if self.core.config.get('hash_type', self.get_task_name()):
      return self.core.config.get('hash_type', self.get_task_name())
    else:
      return ''
  # Get file hash
  def get_file_hash(self, file):
    if file in self.hashes:
      return self.hashes[file]
    else:
      # Source: https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
      # BUF_SIZE is totally arbitrary, change for your app!
      BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
      md5 = hashlib.md5()
      sha1 = hashlib.sha1()
      try:
        with open(file, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
                sha1.update(data)
      except PermissionError:
        if self.core.use_sudo(self.get_task_name()):
          #self.core.log.add('Get hash via commandline with sudo')
          hash = ''
          if self.get_hash_type().lower() == 'md5':
            hash = self.core.run_command('sudo md5sum '  + str(file), self.get_task_name())
          elif self.get_hash_type().lower() == 'sha1':
            hash = self.core.run_command('sudo sha1sum '  + str(file), self.get_task_name())
          if hash != '':
            hash = hash[0]
            hash = hash.split(' ')
            self.hashes[file] = hash[0]
            return hash[0]
        else:
          self.core.log.add('Insufficient rights to calculate ' + self.get_hash_type() + ' hash for [' + str(file) + ']. Consider changing user, allowing sudo or running this script as root.', 2)
        
        
      if self.get_hash_type().lower() == 'md5':
        self.hashes[file] = md5.hexdigest()
        return self.hashes[file]
      elif self.get_hash_type().lower() == 'sha1':
        self.hashes[file] = sha1.hexdigest()
        return self.hashes[file]
      else:
        self.core.log.add('Quitting: Unsupported hash_type configured for ' + self.get_task_name() + '. Please see documentation for supported hash types.', 1)
        self.core.panic()
  # Get stored hash from persistent data storage
  def get_stored_hash(self, file):
    if self.core.config.get('status_storage', self.get_task_name()) == 'sqlite':
      self.get_cursor().execute(self.queries['select_file'], (str(file),))
      return self.get_cursor().fetchone()
  # Store hash in persistent data storage
  def store_hash(self, file, hash, location=''):
    if self.core.config.get('status_storage', self.get_task_name()) == 'sqlite':
      self.get_cursor().execute(self.queries['insert_file'], (str(file), hash, datetime.now(), location))
      self.get_db_connection().commit()



  # DATABASING
  def get_db_connection(self):
    if not self.db:
      if self.core.config.get('status_storage', self.get_task_name()) == 'sqlite':
        # Check if database is present. If the database is not present, tables should be created
        if not os.path.isfile(self.core.get('base_dir') + 'data/' + self.get_task_name() + '.db'):
          self.core.log.add('SQlite database not present. Creating database data/' + self.get_task_name() + '.db', 5)
          new = True
        else:
          new = False
        self.db = sqlite3.connect(self.core.get('base_dir') + 'data/' + self.get_task_name() + '.db')
        if new == True:
          self.core.log.add('Creating table ' + self.dbtable + ' in database.', 5)
          self.get_cursor().execute(self.queries['create_table'])
          self.get_db_connection().commit()
    return self.db

  def get_cursor(self):
    if not self.cursor:
      self.cursor = self.get_db_connection().cursor()
    return self.cursor

  def close_connection(self):
    if self.db:
      self.get_db_connection().commit()
      self.get_db_connection.close()
  
  