# Puchimine

## Overview

Puchimine is the web client for redmine.

 - view the list of projects
 - view all tickets in one project
 - create a new ticket
 - update a ticket
 - change the status of a ticket.

Puchimine is designed to manage the  ticket casually. So puchimine displays and edits only the necessary information i think.

## Sample
### The summary of tickets
![The summary of tickets](https://hupn2w-ch3302.files.1drv.com/y2pvKJCviaG0egAIcts6IlHnB0If7XY4FYlKCLYqvn7_2UbymJSH-Ajy3CxAn-kp27EFdkLcN8JeRl6LKHm7UBnDTtjN9BPwnF4tuQYsM2dn0k/puchimine_demo_1.png?psid=1)

### The detail of a ticket
![The detail of a ticket](https://4nwesq-ch3302.files.1drv.com/y2pxTBjRypHWF75oRw8fhucWy1oyJtHjacxxRc4kHdq-UaDEKHI0QEBbR3MddNYkM167BFmXxXlrnZO13yFaJAs2iVoHaL2fbpuWy0rcxFzaHI/puchimine_demo_2.png?psid=1)

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
