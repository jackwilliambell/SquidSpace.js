# SquidSpace.js Tools

The SquidSpace.js tools are a set of utilities for working with [SquidSpace.js Module Files](squidspace-modulefiles.md), providing services ranging from code generation and asset pipeline management to building and packaging runtime files. There are two basic ways to use the SquidSpace.js Tools:

1. From the command line using the sqs command runner; see Command Line Use below

2. From your own Python code, importing the SquidSpace.js Tools you need and using them directly; see Using the SQS Tools as Components below

The SQS Tools are broken down into 'commands' and the commands are further broken down into functions which can execute all or part of a command. See SQS Commands below.

The SquidSpace.js tools use module.json files for basic configuration and  module.json files or build.json files as input to control how they work. See Command Configuration below. See also, the [SquidSpace.js Module Files Reference](squidspace-modulefiles.md) and the [SquidSpace.js Build Files Reference](squidspace-buildfiles.md).

## Dependencies

The SquidSpace.js tools are written in Python 3 and require a Python 3 Interpreter; the basic SQS tools have no code dependencies. However, some tools allow external 'filter' plugins and those filters may have their own dependencies. See Extending the SQS Tools with Filter Functions below.

## Command Line Use

Currently the SQS tools are not being packaged, so you will need to execute it on the command line using a command like the following:

    > python3 path-to-tools/sqs.py -h

If you make the sqs.py file executable you can leave off the 'python3' portion of the command. If you add the path to your system path ($PATH) you can also leave off 'path-to-tools/'.

At this time the most common use pattern is to copy the entire tools/sqs directory to your SquidSpace.js project directory and use it there. 

### SQS Help

The following command produces the SQS Help text:

    > python3 path-to-tools/sqs.py -h

Result:

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


## SQS Commands

SQS Tools provide the following commands (explained in more detail below):

* generate Generates a SquidSpace.js Javascript module file from a module.json input file

* build - Generates code for all module.json files specified with a build.json file

* package - Performs a build and creates a distributable package specified with a build.json file

* filter - Based on the file extension and configuration, runs a resource file through zero to many a pre-built filtering functions; file input and output locations are configurable

* pipeline - Processes the asset pipeline specified by a module.json input file, including resource filtering and cacheing

* scaffold - Creates a new SquidSpace.js project directory with default content

* serve - Starts a test web server

* explain - Explains a command in more detail

### Command Configuration

For any tools that process an input file, the following rules apply:

1. In most cases a separate 'config' module.json file provides the default configuration used by the command

2. When the command is processing a file containing it's own configuration, the local configuration  can override any values in the default configuration 

3. If a default configuration is not specified and the working directory contains a file named 'world.module.json', that file is automatically used for the default configuration 
   - IMPORTANT! If you do not want to use the world file for the default, make certain to specify a different configuration file.

The configuration values themselves are detailed in the [SquidSpace.js Module Files R](squidspace-modulefiles.md).

### generate Command

The SquidSpace.js 'generate' command reads in a 'module' file containing JSON data meeting the Module File Specification and using the SquidSpace.js Module File extensions. Then, with that data, it generates a Javascript module containing the everything specified in the module file, including external data files 'packed' into the Javascript module. 

TODO: More detail with examples.

### build Command

TODO: Document with examples.

### package Command

TODO: Document with examples.

### filter Command

TODO: Document with examples.

### pipeline Command

The pipeline command reads in a 'module' file containing JSON data meeting the Module File Specification and using the SquidSpace.js Module File extensions. Then, with that data, it manages an asset pipeline for files used during code generation and runtime. 

TODO: More detail with examples.

### scaffold Command

TODO: Document with examples.

### serve Command

The SquidSpace.js 'serve' command creates a web server for static files in the current working directory using the address 'http://localhost:8080/'. The server will run until you force it to quit by pressing 'ctrl-C'.

TODO: More detail with examples.

### explain Command

TODO: Document with examples.

## Extending the SQS Tools with Filter Functions

TODO: Document with examples.

## Using the SQS Tools as Components

TODO: Document with examples.
