# Module File Specification

Module Files let you specify one or more modules. Module Files are processed by reading them in and using them to generate some output or otherwise to control some work. For example, SquidSpace.js provides tools that use Module Files to manage asset pipelines and to generate runtime javascript files. The Module File processor and the context the Module File is used in determines what the outputs are and the details of what Module File values are required. (See also, Module File Processors below.)

Module Files are processed by reading them in and using them to generate some output or otherwise to control some work. For example, SquidSpace.js provides tools that use Module Files to manage asset pipelines and generate runtime javascript files. The Module File processor and the context the Module File is used determines what the outputs are and the details of what Module File values are required. (See also, Module File Processors and Code Generation below.)

Although designed for use by the SquidSpace.js library and toolset, Module Files are generalized and could be used as inputs for other 3D applications. (See also, Module Files as a DSL below.)

IMPORTANT! This specification is for the basic structure of a Module File and does not include any specific features of SquidSpace.js. For details on how Module Files are used in SquidSpace.js, see the [SquidSpace.js packfiles documentation](squidspace-packfiles.md) and the [SquidSpace.js tools documentation](squidspace-tools.md).

A Module File consists of JSON data containing one or more of the following named top-level objects, although a specific Module File processor may add others:

1. "doc" – [string; optional] – documentation for the entire file, use to describe what the file is for 

2. "config" – [object; optional, but may be required or ignored by some Module File processors] – global configuration details for the entire file (See also, Configuation below)

3. "options" – [object; optional, but may be required or ignored by some Module File processors] – global options for the entire file (See also, Options below)

4. "data" – [any type; optional, but may be required or ignored by some Module File processors] – global data for the entire file (See also, Data below)

5. "resources" – [object; optional, but may be required or ignored by some Module File processors] – a specification for all the resources in the module (see also, Resources Section below)

6. "layouts" – [object; optional, but may be required or ignored by some Module File processors] – a specification for all the layouts in the module (see also, Layouts Section below)

7. "events" – [object; optional, but may be required or ignored by some Module File processors] – a specification for all the events in the module (see also, Events Section below)

8. "wiring" – [object; optional, but may be required or ignored by some Module File processors] – a specification for all the wiring in the module (see also, Wiring Section below)

Module File example:

	{
		"doc": "This is a 'synthetic' example with no relation to an actual Module File implementation.",
		"config": {
			"doc": "Contains global configuration values for the file.",
			. . . Other configuration values
		},
		"options": {
			"doc": "Contains global option values for the file.",
			. . . Other options values
		},
		"data": "Contains global data values for the file.",
		"resources": {
			"arbitrary-resource-type-name": {
				"doc": "Each resource represents one thing used at runtime.",
				"resource-name": "Unique name (within resource type) of a resource of type 'resource-type-name.'",
				"config": {
					"doc": "Contains configuration values for the resource.",
					. . . Other configuration values
				},
				"options": {
					"doc": "Contains option values for the resource.",
					. . . Other option values
				},
				"data": "Contains data values for the resource."
			}
		},
		"layouts": [
			{
				"doc": "Each layout represents one 'area' within a 3D space.",
				"layout-name": "Unique name (within layouts) for a layout area.'",
				"config": {
					"doc": "Contains configuration values for the layout area.",
					. . . Other configuration values
				},
				"options": {
					"doc": "Contains option values for the layout area.",
					. . . Other option values
				},
				"data": [
					{
						"doc": "Each object placement specifies placement commands for that object within a 3D space.",
						"object": "Name of a loaded object resource.'",
						"config": {
							"doc": "Contains configuration values for the object placement.",
							. . . Other configuration values
						},
						"options": {
							"doc": "Contains option values for the object placement.",
							. . . Other option values
						},
						"data": [
							{
								"doc": "Each placement command specifies object placement within a 3D space.",
								"place-name": "Unique name (within layout area) used for placed objects.'",
								"config": {
									"doc": "Contains configuration values for the placement command.",
									. . . Other configuration values
								},
								"options": {
									"doc": "Contains option values for the placement command.",
									. . . Other option values
								},
								"data": "Contains data values for the placement command."
							}
						]
					}
				]
			}
		],
		"events": [
			"doc": "TODO: Implement and Document."
		],
		"wiring": [
			"doc": "TODO: Implement and Document."
		]
	}

## Doc

A 'doc' string may appear as a member of any object in a Module File, including at the top level. The purpose of doc strings is to provide human-readable comments and explanations for that object within the overall context.

## Configuration

A 'config' JSON object may appear as a member of any object in a Module File, including at the top level. The purpose of the config object is to set the configuration values used when processing the object they are attached to. The Module File processor may remove the config values when creating output as they have no runtime meaning. What named values a config object may contain and how they are used is dependent both on the Module File processor and the context of the config object within the Module File.

IMPORTANT! Configuration values must not used directly for runtime purposes. They are only meant for code that processes the Module File. However, the Module File processor may add, remove or modify runtime values (options and data) to the processed output based on the contents of the Configuration.

IMPORTANT! The Module File specification does not specify what named values a config object must or may contain. Please refer to the documentation for the Module File processor you will be using for more information.

## Options

An 'options' JSON object may appear as a member of any object in a Module File, including at the top level. The purpose of the options object is to set the optional values used at runtime by the object they are attached to and within it's context, although how those values are represented in the output is dependent on Module File processing. What named values an options object may contain and how they are used is dependent both on the Module File processor and the context of the options object within the Module File.

IMPORTANT! The Module File specification does not specify what named values an options object must or may contain. Please refer to the documentation for the Module File processor you will be using for more information.

## Data

An 'data' value (any type allowed) may appear as a member of any object in a Module File, including at the top level, unless specified with a specific type below. The purpose of the data object is to contain the data value(s) used at runtime by the object they are attached to and within it's context, although how those values are represented in the output is dependent on Module File processing. Data values may be any valid JSON type, although the specific type and how it is are used is dependent both on the Module File processor and the context of the data object within the Module File.

IMPORTANT! The Module File specification does not specify what named values a data object must or may contain. Please refer to the documentation for the Module File processor you will be using for more information.

## Special Value Types

Module Files support some special value types that extend JSON. These include:

* Expression Strings

* Binary Strings.

### Expression Strings ($=)

Module Files support 'Expression Strings'. Any JSON string value starting with the characters '$=' is an Expression String and the entire contents of the string after those characters is considered to be a Javascript or other programming language expression, not as a standard JSON string value. How expression strings are interprested and evaluated is dependent on the Module File Processor.

Expression Strings can be used for any data value of any type, so long as the expression they contain returns the correct value type.

WARNING: Expression Strings can result in runtime failures if they are invalid expressions for the runtime system. They may also introduce difficult to track down bugs since they are added to generated code as opposed to hand-written code. Use them carefully and keep these facts in mind.

Examples:

	"rotation": "$= [0, Math.PI / 2, 0]"

	"rotation": "$=[0, SquidSpace.rotate180, 0]"

	"position": "$= [16, MyMod.getFloaterHeight(), 35 * MyMod.backOffsetDefault]"

	"data": "$= PrivateLoaderFunc('foo')"

### Binary Strings ($#)

Module Files support 'Binary Strings' in Base64 format. Any JSON string value starting with the characters '$#' is a Binary String and the entire contents of the string after those characters must be Base64 data. SquidSpace itself does not translate Binary Strings from Base64, instead it expects the code it passes it to to know the data is in Base64 form and to handle it correctly. How binary strings are interprested converted is dependent on the Module File Processor.

WARNING: Binary Strings can result in runtime failures if they are not valid Base64 or if the data they contain is not the data or data type that was expected. Use them carefully and keep these facts in mind.

TODO: Example

## Resources Section

The resources section of a module is an object containing of one or more uniquely named 'resource types' to include in the output. There can be zero or more resource types. Resource types include, but are not limited to, things like object geometry, texture data, material descriptions and so on. The Module File processor determines which resource types are supported. Each resource type contains an array of 'resource items'. Resource items are descrbed below.

To re-state this more clearly: a 'resources' object contains named 'resource types', each of which contain arrays of 'resource items'. 
 
Each resource item consists of a specification for a single resource to be processed by the Module File processor. A resource item specification consists of the following named objects, although a specific Module File processor may add others:

1. "resource-name" – [string; required] – the name of the resource, should be unique within the resource type array 

2. "doc" – [string; optional] – documentation for the resource item, use to describe what the resource is for 

3. "config" – [object; optional, but may be required or ignored by some Module File processors] – resource-specific configuration (See also, Configuation above)

4. "options" – [object; optional, but may be required or ignored by some Module File processors] – resource-specific options (See also, Options above)

5. "data" – [any type; optional, but may be required or ignored by some Module File processors] – resource-specific data (See also, Data above)

IMPORTANT! The Module File specification does not detail configuration, options, and data values for resource items. Please refer to the documentation for the Module File processor you will be using for more information.

## Layouts Section

The layouts section of a module is an array containing one or more 'layout areas' to include in the output. There can be zero or more layout areas. Layout areas specify an area and contain a layout specification for the objects in that area. A layout area consists of the following named objects, although a specific Module File processor may add others:

1. "layout-name" – [string; required] – the name of the layout area, should be unique within the layouts array 

2. "doc" – [string; optional] – documentation for the layout area, use to describe what the layout area is for 

3. "config" – [object; optional, but may be required or ignored by some Module File processors] – layout area-specific configuration (See also, Configuation above)

4. "options" – [object; optional, but may be required or ignored by some Module File processors] – layout area-specific options (See also, Options above)

5. "data" – [array; required] – a list of object placements in the layout area, described below

Each object placement consists of a specification for zero to many locations of the same object within the layout area, to be processed by the Module File processor. A object placement consists of the following named objects, although a specific Module File processor may add others:

1. "object" - (string; required] – the name of the object to place zero to many times in the layout area; in most cases this will refer to an object-type resource, but the reference could be to an object specified in a separate Module File or to an object built into the runtime; should be unique within the object placements

2. "doc" – [string; optional] – documentation for the object placement, use to describe what the object placement is for 

3. "config" – [object; optional, but may be required or ignored by some Module File processors] – object placement-specific configuration (See also, Configuation above)

4. "options" – [object; optional, but may be required or ignored by some Module File processors] – object placement-specific options (See also, Options above)

5. "data" – [array; required] – a list of placement commands for the object, described below

IMPORTANT! The Module File specification does not detail configuration, options, and data values for object placements. Please refer to the documentation for the Module File processor you will be using for more information.

Each placement command consists of the following objects:

1. "place-name" – [string; required] – A unique name within the Layout Area, used to identify all instances of this placement

2. "doc" – [string; optional] – documentation for the placement command, use to describe what the placement is for 

3. "config" – [object; optional, but may be required or ignored by some Module File processors] – placement command-specific configuration (See also, Configuation above)

4. "options" – [object; optional, but may be required or ignored by some Module File processors] – placement command-specific options (See also, Options above)

5. "data" – [any type; optional, but may be required or ignored by some Module File processors] – placement command-specific data (See also, Data above)

IMPORTANT! The Module File specification does not detail configuration, options, and data values for placement commands. Please refer to the documentation for the Module File processor you will be using for more information.

## Events Section

The events section of a module is an array containing one or more 'event declarations' to include in the output. There can be zero or more event declarations. Event declarations specify an object and a list of events and a list of events to attach to it. An event declaration consists of the following named objects, although a specific Module File processor may add others:

1. "object" - (string; required] – the name of the object to attach the event to

2. "doc" – [string; optional] – documentation for the event declaration, use to describe what the placement is for 

3. "config" – [object; optional, but may be required or ignored by some Module File processors] – event declaration-specific configuration (See also, Configuation above)

4. "options" – [object; optional, but may be required or ignored by some Module File processors] – event declaration-specific options (See also, Options above)

5. "data" – [any type; optional, but may be required or ignored by some Module File processors] – event declaration-specific data (See also, Data above)

IMPORTANT! The Module File specification does not detail configuration, options, and data values for event declarations. Please refer to the documentation for the Module File processor you will be using for more information.

## Wiring Section

TODO: Design. Consider if this should be a SquidSpace.js-only section.

## Module File Processors

Module File processors are computer programs that read in a JSON file conforming to the Module File specification and use the data in the Module File to perform some work. The type of work a Module File processor might do includes, but is not limited to:

* Managing asset pipelines

* Generating code for a runtime system

* Creating distributable packages

* Configuring servers and external applications

## Module Files as a DSL 

Module Files support enough complexity to act as a [DSL (Domain-Specific-Language)](https://en.wikipedia.org/wiki/Domain-specific_language) for arbitrary 3D Graphics applications. A DSL is basically a tiny programming language, often declarative, which is focused on a very specific problem domain. 

SquidSpace uses the Module File DSL capability to declare the functionality for walkthrough simulations. However, Module Files are generic enough to drive a completely different kind of 3D application through that application providing different Module File processors, resources, modifiers and/or doing object placement differently.

