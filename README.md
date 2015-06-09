# screeps-script-caddy
Python script for uploading/downloading scripts to/from the game Screeps

***NOTE:*** Use at your own risk! Make backups of all your files! Exclamation!

# Pre-requisites

1. Python3
1. pip

# Installation

**NOTE**: virtualenv is strongly recommended. These instructions assume you are already in a virtualenv environment.

1. Clone this repo into the folder of your choosing (we'll call it "INSTALL FOLDER")
1. `cd INSTALL FOLDER`
1. `pip install -r requirements.txt`

# Usage

**NOTE**: These instructions assume you are already in the "INSTALL FOLDER".

## General
You must provide your screeps username and password. This can be done through the *arguments*:

	--user

	--password

for username and password respectively.

Alternately, you can define the equivalent *environment variables*:

	SCREEPS_USER

	SCREEPS_PASSWORD

Before executing the script.

## Retrieval

To retrieve a script from screeps:

`python3 manage.py from_game some_folder`

This will retrieve all your script modules from the game and place them in the folder named "some_folder".

If files exist in this folder, the operation will fail with an error message. Specify the argument:

	--force

to override this safety check.

## Sending

To send a collection of script modules to screeps:

`python3 manage.py to_game some_folder`

This will send all your script modules (*.js) to your screeps account.

For each .js file a module of the same name (minus the extension) will be created.

