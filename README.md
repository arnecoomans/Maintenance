# [MTE] Maintenance Task Execution: Entry Point
- Author: Arne Coomans
- Contact: twitter @arnecoomans
- Version: 0.2.0

## About

## Installation
* Get application from git, use git clone
* Use example configuration file as template for configuration: copy config/maintenance.example into config/maintenance.yml

## Configuration
Basic application configuration is stored in config/maintenance.yml. It is possible to create additional configuration files and load these via the commandline argument --config.

Configuration files can be imported from a configuration file using import: "config/file1.yml, config/file2.yml" from the maintenance config level.

Additional configuration overwrites previously set configuration. --args is processed last, so this can overwrite configuration.

## Usage

## Available tasks
- pass
- show_config
- backup_mysql
