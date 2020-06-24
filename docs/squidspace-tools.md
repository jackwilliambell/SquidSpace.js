# SquidSpace.js Tools

The SquidSpace.js tools are a set of utilities for working with [SquidSpace.js Module Files](squidspace-modulefiles.md), providing services ranging from code generation and asset pipeline management to building and packaging runtime files. There are two basic ways to use the SquidSpace.js Tools:

1. From the command line using the sqs command runner; see Command Line Use below

2. From your own Python code, importing the SquidSpace.js Tools you need and using them directly; see Using the SQS Tools as Components below

The SQS Tools are broken down into 'commands' and the commands are further broken down into functions which can execute all or part of a command. See SQS Commands below.

The SquidSpace.js tools use module.json files for basic configuration and  module.json files or build.json files as input to control how they work. See Command Configuration below. See also, the [SquidSpace.js Module Files Reference](squidspace-modulefiles.md) and the [SquidSpace.js Build Files Reference](squidspace-buildfiles.md).

## Dependencies

The SquidSpace.js tools are written in Python 3 and require a Python 3 Interpreter; the basic SQS tools have no external code dependencies. However, some tools allow external 'Filter Module' plugins and those filters may have their own dependencies. See Filter Modules below.

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
	  --profile <prf> Name of a filter profile to use instead of default for file type

TODO: Implement commands to list filters and get filter doc strings.

## SQS Commands

SQS Tools provide the following commands (explained in more detail below):

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

### Command Configuration

For any tools that process an input file, the following rules apply:

1. In most cases a separate 'config' module.json file provides the default configuration used by the command

2. When the command is processing a file containing it's own configuration, the local configuration  can override any values in the default configuration 

3. If a default configuration is not specified and the working directory contains a file named 'world.module.json', that file is automatically used for the default configuration 
   - IMPORTANT! If you do not want to use the world file for the default, make certain to specify a different configuration file.

The configuration values themselves are detailed in the [SquidSpace.js Module Files R](squidspace-modulefiles.md).

### generate Command

The SquidSpace.js 'generate' command reads in a 'module' file containing JSON data meeting the 
Module File Specification and using the SquidSpace.js Module File extensions. Then, with 
that data, it generates a Javascript module containing the everything specified in the module
file, including external data files 'packed' into the Javascript module.

TODO: Insert binary file support with BASE-64 conversion.

TODO: Support binary strings and expression strings.

TODO: Support events and mods.

TODO: Support filters

TODO: More detail and examples

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

The SquidSpace.js 'serve' command creates a web server for static files in the current working directory using the address 'http://localhost:8000/'. The server will run until you force it to quit by pressing 'ctrl-C'.

TODO: More detail with examples.

### explain Command

TODO: Document with examples.

## Extending the SQS Tools with Filter Functions

TODO: Document with examples.

## Using the SQS Tools as Components

TODO: Document with examples.


## Filter Modules

Filter Modules are used by the filter, generate, and pipeline commands to process files in various ways by passing them through one or more filter operations. There are 'built-in' Filter Modules provided as part of the SQS tool, but it is also possible to implement your own 'plugin' Filter Modules, which are loaded at runtime.

TODO: Plugin filters not currently implemented.

Filter Modules consist of Python modules exporting two required functions:

* filterFileExtensions(options, data) – Returns a tuple of (in-extension, out-extension) based on the filter implementation and the parameters

* filter(pathIn, pathOut, options, data) – Performs the filtering operation based on the filter implementation and parameters and returns 'true' if the operation is successful or 'false' if the operation failed

Filter Modules specify valid input and output file extensions via the filterFileExtensions() function. What extension used for the output file may be different from the input file if the filter changes the file type during it's operation. If the expected input extension is provided as 'None', then any file type is allowed. If the output file extension is provided as 'None', then the output file extension must be the same as the input file extension. 

For Filter Modules that can accept different input file types and/or write out different file types a common pattern is to allow "in-ext" and "out-ext" in the filter options, which may be specified by the user, and then process them as similar to the following:

	def filterFileExtensions(options, data):
	    inExt = None
	    outExt = None
	    if "in-ext" in options:
	        inExt = options["in-ext"]
	    if "out-ext" in options:
	        outExt = options["out-ext"]
    
	    return (inExt, outExt)

 Filter Modules do the actual filtering operation via the filter() function. How the function works and what information it requires in it's options and data values are implementation dependent. But, in all cases, the filter function must read in the file specified with the path in and write out a file as specified with the path out. If the filter operation is successful the function must return 'true'. Otherwise it must return 'false', whether or not data is written to the output file.
 
### Built-In Filter Modules
 
 The Filter Function modules provided with SQS include:
 
 * cleanbabylon – Removes unhelpful or unneeded data sections from .babylon files
 
 * shellexec – Passes a file to a shell command for filtering using a template command
 
#### cleanbabylon Filter Module

Removes unhelpful or unneeded data sections from .babylon files. 

Besides the standard filter() and filterFileExtensions() functions there are 
two API functions:

* cleanData(data) - Cleans a Python dictionary containing a parsed .babylon file

* processDirectory(pathIn, pathOut, recurse) - Cleans all .babylon files in 
  the directory specified with pathIn, writing the files out to pathOut. If
  pathIn and pathOut are the same it will operate destructively, overwriting
  the files.

Options: None.

Data: None.

File Extensions:

* in – .babylon

* out – .babylon

#### shellexec Filter Module

Passes a file to a shell command for filtering. The filter options must contain a value
named 'command-template' consisting of a template string with the command to execute. 
The options may also contain a value named 'command-arguments' consisting of a JSON object
with named argument values to apply to the template.

The template string is a standard Python string.format() template with two specified 
template values: '{pathIn}' and '{pathOut}', which are replaced by the pathIn and
pathOut parameters. If 'command-arguments' is also supplied, any names from that value
may also be used as template values.

The expectation of any command used as a filter is as follows: the shell command will
read in pathIn, make changes to it, and write the result out to pathOut. Shell commands which 
do not support this paradigm are not usable as filters.

There is no direct support for mapping the pathIn and pathOut parameters to STDIN 
and STDOUT for commands supporting that usage. However, it is possible to map them in the
template string using redirection. It is also possible to support multiple commands in a 
single command template using pipes.

No attempt is made to suppress STDOUT and STDERR output from the command, so command output
will be written to the terminal during execution unless redirected in the template string.

If the command completes with a '0' exit status the filter returns True. Otherwise the filter 
prints the exit status and returns False.

Options: 

* "in-ext" – [optional, string] Specifies the expected input file extension; do not use if
  the input file type is determined by its extension 

* "out-ext" – [optional, string] Specifies the expected output file extension; do not use if
  the output file type will be the same as the input file type 

* "command-template" [required, string] Specifies the command template string as described above

* "command-arguments" [optional, string] Specifies command arguments which may be replaced 
  by name in the command template string as described above

Data: None.

File Extensions: Determined by option values.

### Plug-In Filter Modules

TODO: Implement.

