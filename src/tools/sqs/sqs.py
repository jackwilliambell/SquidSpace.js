#!/usr/bin/env python3
"""## SquidSpace.js SQS Command Runner

SQS is the command runner for the SquidSpace.js tooling. The command format 
is 'sqs.py command <what> [options ...]'. The commands are:

* generate - Generates a Javascript module files from module.json input files
* build    - Generates code for all module.json files specified with a 
             build.json file
* package  - Performs a build and creates a distributable package specified 
             with a build.json file
* filter   - Based on the filter profile and the configuration, runs input files
             through zero to many pre-built filtering functions and writes the 
             output to the output directory with the same file names
* pipeline - Processes the asset pipeline specified by module.json input files,
             including resource filtering and caching
* scaffold - Creates a new SquidSpace.js project directory with default content
* serve    - Starts a test web server, 'ctrl-c' to exit
* explain  - Explains a command in more detail

In most cases a separate 'config' module.json file provides the default configuraton
used by the command. When the command is processing a file containing it's own 
configuraton, the local configuraton can override any values in the default 
configuration. If a default configuration is not specified and the working directory 
contains a file named 'world.module.json', that file is automatically used for the 
default configuration. If you do not want to use the world file for the default,
make certain to specify a different configuration file.

Commands that process files will attempt to fall back to STDIN if no file name is 
specified, allowing the command to be used with pipes. Mulitple file names are 
supported. (For example, 'foo.module.json bar.module.json' to process two files
in the current directory.) Shell file globbing is also supported. (For example, 
'*.module.json' to process all module files in the current directory.) 

Usage:
  sqs.py generate <file>... [--config=<cfg>] [--dir=<path>]
  sqs.py build <file>... [--config=<cfg>] [--dir=<path>] 
  sqs.py package <file>... [--config=<cfg>] [--dir=<path>]
  sqs.py filter <output_directory> <filter_profile> <file>... [--config=<cfg>] [--dir=<path>]
  sqs.py pipeline <file>... [--config=<cfg>] [--dir=<path>]
  sqs.py scaffold <project-name> [--config=<cfg>] [--dir=<path>]
  sqs.py serve [--dir=<path>]
  sqs.py explain <command>
  sqs.py --help
  sqs.py --version

Options:
  -h --help       Show this help message
  --version       Show version
  --config <cfg>  Module file to use for default configuration
  --dir <path>    Working directory to use instead of current directory

"""


copyright = """SquidSpace.js, the associated tooling, and the documentation are copyright 
Jack William Bell 2020 except where noted. All other content, including HTML files and 3D 
assets, are copyright their respective authors."""


import sys
from os import chdir, path
#import pprint;pprint.pprint(sys.path)
import json
from docopt import docopt
from sqslogger import initSqsLogger
from generate import runGenerate, __doc__ as generateDoc
from filterfile import runFilter, __doc__ as filterDoc
from pipeline import runPipeline, __doc__ as pipelineDoc
from serve import runServer, __doc__ as serveDoc

ver = "sqs v0.0"


if __name__ == '__main__':
    arguments = docopt(__doc__, version=ver)
    
    # TODO: Support command line options for log level and log file.
    #       For log level maybe just have options for 'silent' and 'verbose'?
    #       Maybe always make log file verbose? May need to change initSqsLogger().
    #logger = initSqsLogger(True, True, None)
    logger = initSqsLogger(False, False, None)
    
    logger.debug("SQS starting. Args: \n{args}".format(args = arguments))
    
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
            logger.debug("SQS default config: {0}".format(defaultConfig))
        except json.JSONDecodeError:
            logger.exception("Failed to load Configuration Module File:", sys.exc_info()[1])
            sys.exit(1)
    elif argFileName:
        logger.error("Failed to load Configuration Module File: '" + configFileName + "' does not exist.")
        sys.exit(1)
    
    # Process command.
    # TODO: Error handling.
    if arguments['generate']:
        runGenerate(defaultConfig, arguments['<file>'])
    elif arguments['build']:
        logger.warning("Command 'build' not yet implemented.")
    elif arguments['package']:
        logger.warning("Command 'package' not yet implemented.")
    elif arguments['filter']:
        runFilter(defaultConfig, arguments['<resource_type>'], arguments['<filter_profile>'],
                  arguments['<output_directory>'], arguments['<file>'])
    elif arguments['pipeline']:
        runPipeline(defaultConfig, arguments['<file>'])
    elif arguments['scaffold']:
        logger.warning("Command 'scaffold' not yet implemented.")
    elif arguments['serve']:
        runServer()
    elif arguments['explain']:
        cmd = arguments['<command>'].lower()
        if cmd == 'generate':
            print(generateDoc)
        elif cmd == 'filter':
            print(filterDoc)
        elif cmd == 'pipeline':
            print(pipelineDoc)
        elif cmd == 'serve':
            print(serveDoc)
        else:
            logger.warning("No valid command supplied. Try 'sqs.py -h'.")
            sys.exit(1)
    else:
        logger.warning("No valid command supplied. Try 'sqs.py -h'.")
        sys.exit(1)