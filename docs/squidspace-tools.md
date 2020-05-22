TODO: The following from older notes and needs extensive rework:

There are are an assortment of SquidsSpace management tools:

1. spacepipeline – The spacepipeline tool manages an asset pipeline used by spacepack
   - Configuration is specified by each pack file when processed, but any configuration values will be overridden by a world pack file specified with a command argument or located in the same directory as the tool is ran from
   - World pack is specified with a command argument
   - Pack file to process is specified with a command argument

2. spaceclean – The spaceclean tool processes 3D assets; optimizing specified 3D files, texture images, 3D videos and so on
   - Configuration is specified by each clean file when processed, but any configuration values will be overridden by a world pack file specified with a command argument or located in the same directory as the tool is ran from
   - World pack is specified with a command argument
   - Clean file to process is specified with a command argument

3. spacepack – The spacepack tool packages assets, layouts, and runtime wiring into asset pack files, which are Javascript files for runtime use with squidspace
   - Configuration is specified by each pack file when processed, but any configuration values will be overridden by a world pack file specified with a command argument or located in the same directory as the tool is ran from
   - World pack is specified with a command argument
   - Pack file to process is specified with a command argument

4. spaceship – the spaceship tool builds a release package from asset sources in the pipeline and asset pack files
   - Configuration is specified by each ship file when processed, but any configuration values will be overridden by a world pack file specified with a command argument or located in the same directory as the tool is ran from
   - World pack is specified with a command argument
   - Ship file to process is specified with a command argument

5. missioncontrol – the missioncontrol tool runs jobs that control the other tools to do a series of actions
   - Configuration is specified by each control file when processed, but any configuration values will be overridden by a world pack file specified with a command argument or located in the same directory as the tool is ran from
   - World pack is specified with a command argument
   - Control file to process is specified with a command argument

Besides the management tools, there are testing and debugging tools:

1. spaceserve – starts a simple server on localhost using a selected port
   - Directory to serve is specified with a command argument

All of these tools are also available from a single command-line runner named 'sqs'. You use them in the sqs [command] [arguments] [options], where 'command' is one of 'pipe', 'clean', 'pack', 'ship', 'control', or 'serve'. 
