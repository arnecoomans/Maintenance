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

import sqlite3

import hashlib

sys.path.append(os.path.dirname(os.path.abspath(__file__) + "../.app/"))

import mte_task_dispatcher

class Task(mte_task_dispatcher.Task):
  def __init__(self, core, task_name):
    self.db = None
    self.cursor = None
    self.dbtable = 'files'
    # List backup sources
    self.sources = []
    for item in core.config.get('sources', task_name).split(","):
      self.sources.append(item.strip())
    self.queries = {
      'create_table': 'CREATE TABLE ' + self.dbtable + ' (file text, hash text, date text)',
      'select_file': 'SELECT hash, date FROM ' + self.dbtable + ' WHERE file="?" ORDER BY rowid;',
      'insert_file': 'INSERT INTO ' + self.dbtable + '(?, ?, ?)'
    }
    # Run template task initiator
    super().__init__(core, task_name) 

    

    #self.core.log.add(self.get_file_signature('maintenance.py'))
  
  def __del__(self):
    #self.close_connection()
    pass


  # Everything that needs to be executed should be called from the
  # execute function. 
  def execute(self):
    self.core.log.add('datetime: ' + self.get_date_format())
    self.core.log.add('hash: ' + self.get_hash_type())
    for source in self.sources:
      self.core.log.add('Processing [' + source + '].', 4)
      self.parse_source(source)
      #self.process_source(source)
  

  # Data Getters
  # Get date format
  def get_date_format(self):
    if self.core.config.get('date_time_format', self.get_task_name(), True):
      return self.core.config.get('date_time_format', self.get_task_name(), True)
    else:
      return ''
  
  # Get Hash Type
  def get_hash_type(self):
    if self.core.config.get('hash_type', self.get_task_name(), True):
      return self.core.config.get('hash_type', self.get_task_name(), True)
    else:
      return ''
  
  # Hashing
  def get_file_hash(self, file):
    # Source: https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
            sha1.update(data)
    if self.get_hash_type().lower() == 'md5':
      return md5.hexdigest()
    elif self.get_hash_type().lower() == 'sha1':
      return sha1.hexdigest()
    else:
      self.core.log.add('Quitting: Unsupported hash_type configured for ' + self.get_task_name() + '. Please see documentation for supported hash types.', 1)
      sys.exit()
  
  # Stored hash
  def get_stored_hash(self, file):
    if self.core.config.get('status_storage', self.get_task_name()) == 'sqlite':
      self.get_cursor().execute(self.queries['select_file'], file)


    return {'hash':'80985646f3f355355cca7596c05d41a7ad59addf2', 'date':'yesterday'}

  def store_hash(self, file, hash):
    pass


  # Source parsing
  def parse_source(self, source):
    # Check if recursive sourcing should be applied.
    # lines ending with "[r]" are marked as recursive, and should be 
    # processed one more level deep.
    if source[-3:] == '[r]':
      recursive = True
      source = source[:-3]
    else:
      recursive = False
    # At this time, recursive is either set to True or False
    # Check if a file is supplied
    if os.path.isfile(source):
      self.compare_file_hash(source)
    elif os.path.isdir(source):
      self.core.log.add('directory found')

  # Compare file hash with stored hash
  def compare_file_hash(self, file):
    self.core.log.add('Checking hash for ' + file, 5)
    # Get current hash
    current_hash = self.get_file_hash(file)
    # get stored_hash
    stored_hash = self.get_stored_hash(file)
    if current_hash == stored_hash['hash']:
      self.core.log.add('Hashes match')
    else:
      self.core.log.add('New version of [' + file + '] found. Last known version date is: [' + stored_hash['date'] + '].', 4)
      self.store_hash(file, current_hash)
    #self.core.log.add('Current hash: ' + current_hash)
    self.core.log.add('Stored hash:  ' + stored_hash['hash'])



# DATABASE FUNCTIONS
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
  
  











  #def process_source(self, source):
    
    # Loop through sources. Sources can contain files or directories.
    # If the source is a file:
  #  if os.path.isfile(source):
#      self.core.log.add('This source is actually a file:' + source )
#      self.compare_file(source)
    # If the source is a directory, process the contents
  #  if os.path.isdir(source):
      # 
  #    if source[-1:] != '/':
  #      source += '/'
  #    for file in os.listdir(source):
  #      file = source + file
  #      if os.path.isfile(file):
  #        self.core.log.add(file + ' found') 
  #      elif os.path.isdir(file):
  #        self.core.log.add(file + ' is a dir?')
  #      else:
  #        self.core.log.add('whats up with ' + file)

#  def compare_file2(self, file):
#    self.core.log.add('Comparing ' + file)
#    if self.core.config.get('status_storage', self.get_task_name()) == 'sqlite':
#      self.core.log.add(self.queries['select_file'])
#      #self.get_cursor().execute(self.queries['select_file'], file)
#      self.get_cursor().execute('SELECT * FROM files WHERE file=? ORDER BY DATE', (file,))
#      self.core.log.add('fetched: ' + str(self.get_cursor().fetchall()))
#  
#  def store_file_hash(self, file):
#    self.core.log('Storing hash for ' + file)#


  # Storage functions
 
    


