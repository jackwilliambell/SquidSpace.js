"""## shellexec.py – SQS Filter Module that executes a shell command

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

File Extensions: Determined by option values."""


copyright = """SquidSpace.js, the associated tooling, and the documentation are copyright 
Jack William Bell 2020 except where noted. All other content, including HTML files and 3D 
assets, are copyright their respective authors."""


import subprocess
from sqslogger import logger


def filterFileExtensions(options, data):
    inExt = None
    outExt = None
    if "in-ext" in options:
        inExt = options["in-ext"]
    if "out-ext" in options:
        outExt = options["out-ext"]
    
    return (inExt, outExt)
    

def filter(pathIn, pathOut, options, data):
    #logger.debug("shellexec.filter() - Processing pathIn: {pathIn} pathOut: {pathOut} options: %{options}.".format(
    #        pathIn=pathIn, pathOut=pathOut, options=options))
    
    # TODO: Determine if we want to verify the path in/out file extensions based on the result 
    #       from filterFileExtensions().
    
    # Create the command to execute.
    command = None
    if "command-template" in options:
        command = options["command-template"]
        # TODO: Verify "command-arguments" is a dict or not there.
        if "command-arguments" in options:
            command = command.format(pathIn=pathIn, pathOut=pathOut, **options["command-arguments"])
        else:
            command = command.format(pathIn=pathIn, pathOut=pathOut)
    
    # Do we have a command?
    if command == None or len(command) <= (len(pathIn) + len(pathOut)):
        logger.error("shellexec.filter() - Command '{0}' is invalid.".format(command))
        return False
    
    # Execute the command.
    try:
        retcode = subprocess.call(command, shell=True)
        if retcode < 0:
            logger.error("shellexec.filter() - Command '{0}' was terminated by a signal. Return code: {1}.".format(
                    command, -retcode))
        elif retcode != 0:
            logger.error("shellexec.filter() - Command '{0}' was terminated by a signal. Return code: {1}.".format(
                    command, retcode))
    except OSError:
            logger.exception("shellexec.filter() - Command '{0}' failed with an exception.".format(command))
    
    # Done!
    return retcode == 0