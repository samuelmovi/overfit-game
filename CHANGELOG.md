# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- figure out way to spy on test classes
- allow certs.py to create required folders if non-existing
- add logic for client trying to connect to non-existent server

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

