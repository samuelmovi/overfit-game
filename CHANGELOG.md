# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- figure out way to spy on test classes
- allow certs.py to create required folders if non-existing
- add logic for client trying to connect to non-existent server
- client changes for new revision:
    - only send data on state change
    - manage zmq client auth failing 
- redo unittests for server and client
- on successful save of settings data, go to start page
- check that client in available_players aren't expired
- go to landing page when leaving online game

## 2020-01-16
### Added
- when returning to online_setup screen send QUIT message and WELCOME message to server
- add event listener while connecting
- add event listener while finding matches
- new opponent dictionary specification
    
### Changed
- send landing data by default to client not on online_players
- new formatting to message printouts with timestamp

### Fixed
- Server using outdated message protocol
- client forgot to load json data before using
- crash after pressing ESC twice on waiting screen
- setting player.online as necessary for proper match negotiating
- order of methods in loop for "find_online_mach", listener is last now
- opponent's info not displaying on board
- multiplayer online game working well

## 2020-01-15
### Fixed
- Client and server communicating correctly
- sqlalchemy backend working

### Added
- view landing page code
- method to add dummy data to db if empty
- event listener for landing page

## 2020-01-13
### Changed
- removed unused code form zmq connector modules, only relevant methods left in client and server
- some modification to README for new changes, more to do
- communication protocol

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

