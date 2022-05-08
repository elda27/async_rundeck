# Asynchronous rundeck API client
This is a rundeck API client implemeneted by aio-http.

## Installation
```bash
pip install async-rundeck
```

## Features
The items checked in the following list are implemented.

- [ ] System Info
- [ ] List Metrics
  - [ ] Metrics Links
  - [ ] Metrics Data
  - [ ] Metrics Healthcheck
  - [ ] Metrics Threading
  - [ ] Metrics Ping
- [ ] User Profile
- [ ] Log Storage
- [ ] Execution Mode
- [ ] Cluster Mode
- [ ] ACLs
- [ ] Jobs
  - [x] List job
  - [x] Run job
  - [x] Import job from file
  - [x] Export job from file
- [ ] Executions
  - [x] Get Executions for a Job
  - [ ] Delete all Executions for a Job
  - [x] Listing Running Executions
  - [ ] Execution Info
  - [ ] List Input Files for an Execution
  - [x] Delete an Execution
  - [ ] Bulk Delete Executions
  - [ ] Execution Query
  - [ ] Execution State
  - [ ] Execution Output
  - [ ] Execution Output with State
  - [ ] Aborting Executions
- [ ] Adhoc
- [ ] Key Storage
  - [ ] Upload keys
  - [ ] List keys
  - [ ] Get Key Metadata
  - [ ] Get Key Contents
  - [ ] Delete Keys
- [ ] Projects
  - [x] Listing Projects
  - [x] Project Creation
  - [x] Getting Project Info
  - [x] Project Deletion
  - [x] Project Configuration
  - [x] Project Configuration Keys
  - [ ] Project Archive Export
  - [ ] Project Archive Export Async
  - [ ] Project Archive Export Status
  - [ ] Project Archive Import
  - [ ] Updating and Listing Resources for a Project
  - [ ] Project Readme File
  - [ ] Project ACLs
- [ ] Listing History
- [ ] Resources/Nodes
- [ ] SCM
