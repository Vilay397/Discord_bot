## Discord-bot

Discrod bot to filter messages, built with Python, Discord API, SqLite.


________________________________________________________________________________________________________________________________________


## Installation and Setup Instructions

Clone this repository. You will need python, virtualenv, and Discord API installed on your machine.

### Set up a virtual environment:

`python -m venv venv`

`venv\Scripts\activate`

#### Installation:

`pip install discord.py`
   
________________________________________________________________________________________________________________________________________

### Create bot run (.bat):

`@echo off`

`call %~dp0Discord_bot\venv\Scripts\activate`

`cd %~dp0Discord_bot`

`set TOKEN= <Your Token>`

`python botrun.py`

`pause`
