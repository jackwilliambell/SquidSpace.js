#!/usr/bin/env python3
"""                ====== SquiSpace.js SQS ======
SQS is the command runner for the SquidSpace.js tooling. The command format 
is 'sqs.py command <what> [options ...]'. The commands are:

* generate - Generates a Javascript module file from a module.json input file
* build    - Generates code for all module.json files specified with a 
             build.json file
* package  - Performs a build and creates a distributable package specified 
             with a build.json file
* filter   - Based on the file extension and configuration, runs a resource file 
             through zero to many a pre-built filtering functions; file input and
             output locations are configurable
* pipeline - Processes the asset pipeline specified by a module.json input file,
             including resource filtering and cacheing
* scaffold - Creates a new SquidSpace.js project directory with default content
* serve    - Starts a test web server, 'ctrl-c' to exit
* explain  - Explains a commond in more detail.

In most cases a separate 'config' module.json file provides the default configuraton
used by the command. When the command is processing a file containing it's own 
configuraton, the local configuraton can override any values in the default 
configuration. If a default configuration is not specified and the working directory 
contains a file named 'world.module.json', that file is automatically used for the 
default configuration. If you do not want to use the world file for the default,
make certain to specify a different configuration file.

Commands that process files will attempt to fall back to STDIN if no file name is 
specified, allowing the command to be used with pipes. Mulitple file names are 
supported. (For example, 'foo.module.json bar.module.json' to process two files.) 
Shell file globbing is also supported. (For example, '*.module.json' to process  
all module files in the current directory.) 

Usage:
  sqs.py generate <file>... [--config=<cfg>] [--dir=<path>]
  sqs.py build <file>... [--config=<cfg>] [--dir=<path>]
  sqs.py package <file>... [--config=<cfg>] [--dir=<path>]
  sqs.py filter <file>... [--config=<cfg>] [--dir=<path>]
  sqs.py pipeline <file>... [--config=<cfg>] [--dir=<path>]
  sqs.py scaffold <project-name> [--config=<cfg>] [--dir=<path>]
  sqs.py serve [--dir=<path>]
  sqs.py explain <command>
  sqs.py --help
  sqs.py --version

Options:
  -h --help      Show this help message
  --version      Show version
  --config <cfg> Module file to use for default configuration
  --dir <path>   Working directory to use instead of current directory
  
"""


copyright = """SquidSpace.js, the associated tooling, and the documentation are copyright 
Jack William Bell 2020 except where noted. All other content, including HTML files and 3D 
assets, are copyright their respective authors."""


from os import chdir, path
import sys
import json
from docopt import docopt
from generate import runGenerate, __doc__ as generateDoc
from serve import runServer, __doc__ as serveDoc

ver = "sqs v0.0"


if __name__ == '__main__':
    arguments = docopt(__doc__, version=ver)
    
    # Debug.
    #print(arguments)
    
    # Change working directory?
    if arguments['--dir'] != None:
        # TODO: Error handling.
        chdir(arguments['--dir'])
    
    # Get default configuration.
    # TODO: Determine fall-through defaults. (Defaults of the defaults?)
    defaultConfig = {} 
    configFileName = arguments['--config']
    argFileName = True
    if configFileName == None:
        configFileName = "world.module.json"    
        argFileName = False
    if path.isfile(configFileName):
        try:
            configFile = open(configFileName)
            defaultConfig = json.load(configFile)["config"]
            # Debug.
            #print(defaultConfig)
        except json.JSONDecodeError:
            print("Error loading Configuration Module File:", sys.exc_info()[1])
            sys.exit(1)
    elif argFileName:
        print("Error loading Configuration Module File: '" + configFileName + "' does not exist.")
        sys.exit(1)
    
    # Process command.
    # TODO: Error handling.
    if arguments['generate']:
        runGenerate(defaultConfig, arguments['<file>'])
    elif arguments['build']:
        print("Command 'build' not yet implemented.")
    elif arguments['package']:
        print("Command 'package' not yet implemented.")
    elif arguments['filter']:
        print("Command 'filter' not yet implemented.")
    elif arguments['pipeline']:
        print("Command 'pipeline' not yet implemented.")
    elif arguments['scaffold']:
        print("Command 'scaffold' not yet implemented.")
    elif arguments['serve']:
        runServer()
    elif arguments['explain']:
        cmd = arguments['<command>'].lower()
        if cmd == 'generate':
            print(generateDoc)
        elif cmd == 'serve':
            print(serveDoc)
        else:
            print("No valid command supplied. Try 'sqs.py -h'.")
            sys.exit(1)
    else:
        print("No valid command supplied. Try 'sqs.py -h'.")
        sys.exit(1)