# How To Manage Content for Squid Hall

This document provides specific information for running the SQS pipeline command in Squid Hall.

Content management consists of two separate steps, which must be done in the following order: 

1. Running the asset pipeline

2. Generating and Merging the code for autoloading

Each of these steps is described in more detail in a section below. For more information about content files see the [Creating and Testing Content Module Files Tutorial](tutorial-content-module-files.md) and the [SquidSpace Module File requirements](squidspace-modulefiles.md).

In cases when you are running the same commands over and over again it is helpful to create a shell or batch file containing those commands. How to do this is beyond the scope of this document. However, the 'buildall.sh' and buildcontent.sh' shell files are examples.

All the commands described below should be run from the root of the Squid Hall project directory.

## How To Run the Content Pipeline for Squid Hall

This section provides specific information for running the SQS asset pipeline command for content in Squid Hall.

You have several options for running the pipeline. In most cases you will only want to run the asset pipeline for one or two content modules file you have just created or modified. In some cases you will want to run the pipeline for all content module files.

IMPORTANT! Asset pipeline processing requires fetching a large number of large files from the Internet. Depending on the number of content module files you are processing and the speed of your Internet connection you may find this takes a while. 

### Location and naming of Content Files

All Content files should be in the 'content/' folder. The name should be descriptive, but must end with '.content.module.json'. 

### Running the Pipeline for a single Content File

To run the pipeline for a single content file, use the following command:

    python3 tools/sqs/sqs.py pipeline content/YOURFILENAME.content.module.json

It should complete silently. If there are errors you may need to make changes to the content file and run it again.

### Running the Pipeline for two or more Content Files at one time

To run the pipeline for two or more content files, use the following command:

    python3 tools/sqs/sqs.py pipeline content/YOURFILENAME1.content.module.json content/YOURFILENAME2.content.module.json

It should complete silently. If there are errors you may need to make changes to the content file and run it again.

### Running the Pipeline for all Content Files at once

To run the pipeline for all of the content files, use the following command:

    python3 tools/sqs/sqs.py pipeline content/*.content.module.json

If you are on a Unix system there is an existing shell commend for this you can run with the following command:

    ./pipeall.sh

It should complete silently. If there are errors you may need to make changes to the content file and run it again.

## How To Generate/Merge Content Code for Squid Hall

This section provides specific information for running the SQS code generation command for content in Squid Hall.

Like with the pipeline processing described above you can generate code for one or two content modules at a time. However, there really isn't a need to do so since code generation is fast and you are assured of picking all the latest changes by generating for everything


### Generating/Merging Code for all Content Files at once

To generate and merge code for all of the content files, use the following commands:

	python3 tools/sqs/sqs.py generate content/*.content.module.json
	python3 tools/sqs/sqs.py filter libs/modules/ MergeContentJS libs/modules/content/*.js

If you are on a Unix system there is an existing shell commend for this you can run with the following command:

    ./buildcontent.sh

It should complete silently. If there are errors you may need to make changes to the content file and run it again.

### Rebuilding Everything

If you need to generate code for every module file for some reason, use the following commands:

	python3 tools/sqs/sqs.py generate world.module.json
	python3 tools/sqs/sqs.py generate furniture.module.json
	python3 tools/sqs/sqs.py generate content/*.content.module.json
	python3 tools/sqs/sqs.py filter libs/modules/ MergeContentJS libs/modules/content/*.js

If you are on a Unix system there is an existing shell commend for this you can run with the following command:

    ./buildall.sh

It should complete silently. If there are errors you may need to make changes to the content file and run it again.



