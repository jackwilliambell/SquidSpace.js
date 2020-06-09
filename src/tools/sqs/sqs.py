#!/usr/bin/env python3
"""              ====== SquiSpace.js SQS ======
SQS is the command runner for the SquidSpace.js tooling. The command format 
is 'sqs.py command <what> [options ...]'. The commands are:

* make     - Generates a Javascript module file from a module.json input file
* build    - Generates code for all module.json files specified with a 
             build.json file
* package  - Peforms a build and creates a distributable package specified 
             with a build.json file
* optimize - Based on the file type and configuration, attempts to optimize a 
             resource file
* pipeline - Processes the asset pipeline specified in a module.json input file
             (also performs optimization on all resource files processed)
* scaffold - Creates a new SquidSpace.js project directory
* serve    - Starts a test web server, 'ctrl-c' to exit
* explain  - Provides a more detailed explanation of a command

In most cases a world module.json file provides the default configuraton used by 
the command. When the command is processing a file containing it's own configuraton,
the local configuraton can override the world file configuration. If a world file 
is not specified and the working directory contains a file named 'world.module.json',
that file is used for the world file.

Commands that process files will attempt to fall back to STDIN if no file name is 
specified, allowing the command to be used with pipes. Mulitple file names and 
file globbing are supported. (For example, '*.module.json' to process all module
files in the current directory.) 

Usage:
  sqs.py make <file>... [--world=<wfl>] [--dir=<path>]
  sqs.py build <file>... [--world=<wfl>] [--dir=<path>]
  sqs.py package <file>... [--world=<wfl>] [--dir=<path>]
  sqs.py optimize <file>... [--world=<wfl>] [--dir=<path>]
  sqs.py pipeline <file>... [--world=<wfl>] [--dir=<path>]
  sqs.py scaffold <project-name> [--world=<wfl>] [--dir=<path>]
  sqs.py serve [--dir=<path>]
  sqs.py explain <command>

Options:
  -h --help     Show this help message
  --version     Show version
  --world <wfl> World module file to use for default configuration
  --dir <path>  Working directory to use instead of current directory
  
"""

from docopt import docopt
from os import chdir
from make import runMake, __doc__ as makeDoc

ver = "sqs v0.0"

if __name__ == '__main__':
    arguments = docopt(__doc__, version=ver)
    
    # Debug.
    #print(arguments)
    
    # Change working directory?
    if arguments['--dir'] != None:
        # TODO: Error handling.
        chdir(arguments['--dir'])
    
    # Get world file configuration.
    worldConfig = {}
    # TODO: Implement
    
    # Process command.
    if arguments['make']:
        runMake(worldConfig, arguments['<file>'])
    elif arguments['build']:
        print("Command 'build' not yet implemented.")
    elif arguments['package']:
        print("Command 'package' not yet implemented.")
    elif arguments['optimize']:
        print("Command 'optimize' not yet implemented.")
    elif arguments['pipeline']:
        print("Command 'pipeline' not yet implemented.")
    elif arguments['scaffold']:
        print("Command 'scaffold' not yet implemented.")
    elif arguments['serve']:
        print("Command 'serve' not yet implemented.")
    elif arguments['explain']:
        if arguments['<command>'] == "make":
            print(makeDoc)
        else:
            print("No valid command supplied.")
    else:
        print("No valid command supplied.")
    
    