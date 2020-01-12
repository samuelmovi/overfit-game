# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- figure out way to spy on test classes
- allow certs.py to create required folders if non-existing
- add logic for client trying to connect to non-existent server
- major server overhaul:
    - server landing page
    - server info and stats
    - add sqlite server backend
- client changes for new client
    - only send data on state change


## 2010-01-12
### Changed
- name of game package to client package
- name of zmq_connector modules to zmq_client and zmq_server for differentiation
- `PullPubServer` substituted by new `Server`

### Added
- Database class for database management (`db_connector.py`)
- Added `models` module for player model


## 2019-10-23
### Fixed
- maximum recursion depth issue in controller's acquire targets method
 

## 2019-10-22
### Added
- __init__ files to test folders to automate testing
- test class for player

### Changed
- renamed game.py to start.py
- moved some controller code into the models
- timeout implementation for online broker
- improved folder structure for server sub-project
- refactored server sub-project code
- refactored controller, now only one while loop in whole class

### Broke
- fatal regression in explosion, after controller refactoring

### Fixed
- some test regressions due to folder structure change

## 2019-10-19
### Changed
- new folder structure for game source files

## 2019-10-18
### Added
- test classes for model, to be completed

### Changed
- changed game.py to allow for better MVC pattern injection
- moved test folder inside game to separate from server tests
- controller.load_external_resources() now static method

