"""## filters.shellexec.py – SQS Filter Module that executes a shell command

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

Besides the standard filterFile() functions there is one API function:

1. shellExec(pathIn, pathOut, options, logger) – Executes a shell command 

### Filter File function

Options: 

* "in-ext" [optional, string] Specifies the allowed input file extension

* "out-ext" [optional, string] Specifies the output file extension to use

* "command-template" [required, string] Specifies the command template string as described above

* "command-arguments" [optional, string] Specifies command arguments which may be replaced 
  by name in the command template string as described above

File Extensions: Determined by option values."""


copyright = """SquidSpace.js, the associated tooling, and the documentation are copyright 
Jack William Bell 2020 except where noted. All other content, including HTML files and 3D 
assets, are copyright their respective authors."""


import os
import subprocess
from common import forceFileExtension

def shellExec(pathIn, pathOut, options, logger):
    """Executes a shell command and returns True if the command can be executed and 
    results in a return code of zero, otherwise returns false. The options argument is a  
    dictionary which must contain the named value 'command-template' and may optionally 
    contain the named value 'command-arguments'. The command template may contain template 
    values for pathIn, pathOut and any named values in the 'command-arguments' dictionary."""
    logger.debug("shellexec.shellExec() - Processing pathIn: {pathIn} pathOut: {pathOut} options: %{options}.".format(pathIn=pathIn, pathOut=pathOut, options=options))
    
    # Create the command to execute.
    command = None
    if "command-template" in options:
        command = options["command-template"]
        # TODO: Verify "command-arguments" is a dict.
        if "command-arguments" in options:
            command = command.format(pathIn=pathIn, pathOut=pathOut, **options["command-arguments"])
        else:
            command = command.format(pathIn=pathIn, pathOut=pathOut)
    
    # Do we have a command?
    if command == None or len(command) <= (len(pathIn) + len(pathOut)):
        logger.error("shellexec.shellExec() - Command '{0}' is invalid.".format(command))
        return False
    
    # Execute the command.
    try:
        retcode = subprocess.call(command, shell=True)
        if retcode < 0:
            logger.error("shellexec.shellExec() - Command '{0}' was terminated by a signal. Return code: {1}.".format(
                    command, -retcode))
        elif retcode != 0:
            logger.error("shellexec.shellExec() - Command '{0}' resulted in a non-zero return code. Return code: {1}.".format(
                    command, retcode))
    except OSError:
            logger.exception("shellexec.shellExec() - Command '{0}' failed with an exception.".format(command))
    
    # Done!
    return retcode == 0


def filterFiles(inputs, outputs, options, logger):
    """SQS filter files function that executes a shell command. The options argument is a  
    dictionary which must contain the named value 'command-template' and may optionally 
    contain the named value 'command-arguments'. The command template may contain template 
    values for pathIn, pathOut and any named values in the 'command-arguments' dictionary."""
    
    logger.debug("shellexec.filterFiles().")
    
    # Setup
    result = 0
    outExt = None
    if "out-ext" in options:
        outExt = options["out-ext"]

    # Process input files.
    for pathIn in inputs:
        # Output name will be same as input name, optionally with a different file extension.
        nameOut = os.path.basename(pathIn)
        if outExt:
            nameOut = forceFileExtension(nameOut, outExt)
            
        # Filter it.
        if shellExec(pathIn, outputs(nameOut), options, logger):
            result = result + 1
            
    # Done.
    return result
    