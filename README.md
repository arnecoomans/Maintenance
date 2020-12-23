# [MTE] Maintenance Task Execution: Entry Point
- Author: Arne Coomans
- Contact: twitter @arnecoomans
- Version: 0.2.0

## About

## Installation
### Download application
The best way to get the application to your environment is to clone it from Github. This will allow the appication to receive updates in the form of more safe or efficiënt code, new features or new tasks.
```
$ git clone https://github.com/arnecoomans/maintenance . 
```

### Create configuration file
The application comes with an example configuration file. Use this as a basis for your personalized configuration. Read more about configuration options and customisability as soon as that documentation is written.
```
$ cp config/maintenance.example config/maintenance.yml
```

### Create symlink to tasks you want available.
By default, no tasks are enabled. In order to enable tasks, you need to place the tasks into the tasks-enable/ directory. The easiest way is to create symlinks, that also ensure updates are pushed.
```
$ cd tasks-enabled/
$ ln -s ../tasks-available/* .
```

### Optional: make application executable
If you want to run ./maintenance.py instead of python3 maintenance.py, you can choose to make the file executable.
```
chmod +x maintenance.py
```

In the following instructions, whenever it mentions python3 maintenance.py you can type ./maintenance.py.


## Configuration
Basic application configuration is stored in config/maintenance.yml. It is possible to create additional configuration files and load these via the commandline argument --config.

Configuration files can be imported from a configuration file using import: "config/file1.yml, config/file2.yml" from the maintenance config level.

Additional configuration overwrites previously set configuration. --args is processed last, so this can overwrite configuration.

## Usage
Use python to execute the application. Supply the --task directive and give a task to be executed.
### Test if the application is working
```
$ python3 maintenance.py --task pass
```
### See what the application is doing
```
$ python3 maintenance.py --task pass --logging 5
```

## Available tasks
### System tasks
- pass - do nothing. Great for testing.
- show-config - show config as is applied in the application.
- self-update
### Maintenance tasks
- backup-config - create backup of file if content differs from last known backup.
- backup-mysql - create mysql dump of specified databases.

