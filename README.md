# Puchimine

## Overview

Puchimine is the web client for redmine.

 - view the list of projects
 - view all tickets in one project
 - create a new ticket
 - update a ticket
 - change the status of a ticket.

Puchimine is designed to manage the  ticket casually. So puchimine displays and edits only the necessary information i think.

## Requirement
 - Python3
 - Bottle
 - Jinja2
 - requests

## Installation
 0. Enable the API of your redmine.
 1. on your PC.

    git clone  
    cd puchimine  

 2. change "config.json.sample" to "config.json"
 3. open "config.json" and edit the sample code to your real parameter.

## Usage
 1. cd puchimine
 2. python index.py
 3. open your web browser and access to http://localist:8082/puchimine/
