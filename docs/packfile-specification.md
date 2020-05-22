# Pack File Specification

Pack Files let you specify one or more modulesPack files are processed by reading them in and using them to generate some output or otherwise to control some work. For example, SquidSpace.js provides tools that use pack files to manage asset pipelines and to generate runtime javascript files. The pack file processor and the context the pack file is used in determines what the outputs are and the details of what pack file values are required. (See also, Pack File Processors below.)

Pack files are processed by reading them in and using them to generate some output or otherwise to control some work. For example, SquidSpace.js provides tools that use pack files to manage asset pipelines and generate runtime javascript files. The pack file processor and the context the pack file is used determines what the outputs are and the details of what pack file values are required. (See also, Pack File Processors and Code Generation below.)

Although designed for use by the SquidSpace.js library and toolset, Pack Files are generalized and could be used as inputs for other 3D applications. (See also, Pack Files as a DSL below.)

IMPORTANT! This specification is for the basic structure of a pack file and does not include any specific features of SquidSpace.js. For details on how pack files are used in SquidSpace.js, see the (SquidSpace.js tools documentation)[squidspace_tools.md].

A Pack File consists of JSON data containing one or more of the following named top-level objects, although a specific pack file processor may add others:

1. "doc" – (string; optional) – documentation for the entire file, use to describe what the file is for 

2. "config" – (object; optional, but may be required or ignored by some pack file processors) – global configuration details for the entire file (See also, Configuation below)

3. "options" – (object; optional, but may be required or ignored by some pack file processors) – global options for the entire file (See also, Options below)

4. "data" – (any type; optional, but may be required or ignored by some pack file processors) – global data for the entire file (See also, Data below)
	 
5. "modules" – (array; optional, but may be required or ignored by some pack file processors) – a specification for each module to be generated (see also, Modules below)

Pack File example:

TODO: Update to a more complete example.

	{
		"doc": "SquidSpace example: Simple Room - a very basic room made using only procedurals and builtins.",
		"config": {
			"doc": "'outdir' specifies where the output files are generated.",
			"outdir": "libs/dungeon_room/"
		},
		"options": {
			"doc": "No options.",
		},
		"data": "No data.",
		"modules": [
			{
				"doc": "The world module specifies .",
			    "name": "world",
				"config": {
					"doc": "No config."
				},
				"options": {
					"doc": "No options."
				},
				"data": {
					"doc": "'world-origin' specifies a NE corner of the world, from which all world locations originate.",
					"world-origin": [0, 0, 0]
				},
				"resources": {
					"textures": [
					
					],
					"materials": [
					
					],
					"objects": [
						{
							"name": "arena",
							"doc": "Example object.",
							"config": {
								"space-object": true,
							},
							"data": {
								"action": "insert",
								"file": "objects/arena.babylon"
							}
						},
						{
							"name": "beam",
							"data": {
								"action": "link",
								"root": "objects/",
								"file": "beam.babylon"
							}
						}
					],
					"lights": [
					
					],
					"mods": [
					
					]
				},
				"layouts": [
					{
						"name": "beam",
						"doc": "Example object.",
						"config": {
							"doc": "No config."
						},
						"options": {
							"doc": "No options."
						},
						"data": {
							"doc": "No data."
						},
						"object-placements": [
							{
								"object": "beam",
								"doc": "Example object.",
								"config": {
									"doc": "No config."
								},
								"options": {
									"doc": "No options."
								},
								"data": {
									"doc": "No data."
								},
								"placements": [
									{
										"placer": "linear-series",
										"doc": "Example 'linear-series' placement.",
										"config": {
											"doc": "No config.",
											"count": 8,
											"position": [
												20,
												0.01,
												1.6
											],
											"offset": 0.3,
											"rotation": "= Math.PI / 2",
											"across": true
										},
										"options": {
											"doc": "No options."
										},
										"data": {
											"doc": "No data."
										}
									}
								]
							
							}
						]
					}
				],
				"wiring": [
					{
						"mod": "squidmmo",
						"config": {
							"doc": "No config."
						},
						"options": {
							"doc": "No options."
						},
						"data": {
							"doc": "No data."
						},
					}
				]
			}
		]
	}
	

## Doc

A 'doc' string may appear as a member of any object in a pack file, including at the top level. The purpose of doc strings is to provide human-readable comments and explanations for that object within the overall context.

## Configuration

A 'config' object may appear as a member of any object in a pack file, including at the top level. The purpose of the config object is to set the configuration values used when processing the object they are attached to. The pack file processor may remove the config values when creating output as they have no runtime meaning. What named values a config object may contain and how they are used is dependent both on the pack file processor and the context of the config object within the pack file.

IMPORTANT! The pack file specification does not specify what named values a config object must or may contain. Please refer to the documentation for the pack file processor you will be using for more information.

## Options

An 'options' object may appear as a member of any object in a pack file, including at the top level. The purpose of the options object is to set the optional values used at runtime by the object they are attached to and within it's context, although how those values are represented in the output is dependent on pack file processing. What named values an options object may contain and how they are used is dependent both on the pack file processor and the context of the options object within the pack file.

IMPORTANT! The pack file specification does not specify what named values an options object must or may contain. Please refer to the documentation for the pack file processor you will be using for more information.

## Data

An 'data' value (any type allowed) may appear as a member of any object in a pack file, including at the top level. The purpose of the data object is to contain the data value(s) used at runtime by the object they are attached to and within it's context, although how those values are represented in the output is dependent on pack file processing. Data values may be any valid JSON type, although the specific type and how it is are used is dependent both on the pack file processor and the context of the data object within the pack file.

IMPORTANT! The pack file specification does not specify what named values a data object must or may contain. Please refer to the documentation for the pack file processor you will be using for more information.

## Modules

The module section of a pack file is an array of one or more modules to process. Each module item consists of a specification for a single module. A module specification consists of JSON data containing the following named objects, although a specific pack file processor may add others:

1. "name" – (string; required) – the name of the module, should be unique within the module array 

2. "doc" – (string; optional) – documentation for the module, use to describe what the module is for 

3. "config" – (object; optional, but may be required or ignored by some pack file processors) – module-wide configuration (See also, Configuation above)

4. "options" – (object; optional, but may be required or ignored by some pack file processors) – module-wide options (See also, Options above)

5. "data" – (any type; optional, but may be required or ignored by some pack file processors) – module-wide data (See also, Data above)
	 
6. "resources" – (object; optional, but may be required or ignored by some pack file processors) – a specification for all the resources in the module (see also, Resources below)
	 
7. "layouts" – (object; optional, but may be required or ignored by some pack file processors) – a specification for all the layouts in the module (see also, Layouts below)
	 
8. "wiring" – (object; optional, but may be required or ignored by some pack file processors) – a specification for all the wiring in the module (see also, Wiring below)

### Module Resources

The resources section of a module is an object containing of one or more uniquely named 'resource types' to include in the output. There can be zero or more resource types. Resource types include, but are not limited to, things like object geometry, texture data, material descriptions and so on. The pack file processor determines which resource types are supported. Each resource type contains an array of 'resource items'. Resource items are descrbed below.

To re-state this more clearly: a 'resources' object contains named 'resource types', each of which contain arrays of 'resource items'. 
 
Each resource item consists of a specification for a single resource to be processed by the pack file processor. A resource item specification consists of the following named objects, although a specific pack file processor may add others:

1. "name" – (string; required) – the name of the resource, should be unique within the resource type array 

2. "doc" – (string; optional) – documentation for the resource item, use to describe what the resource is for 

3. "config" – (object; optional, but may be required or ignored by some pack file processors) – resource-specific configuration (See also, Configuation above)

4. "options" – (object; optional, but may be required or ignored by some pack file processors) – resource-specific options (See also, Options above)

5. "data" – (any type; optional, but may be required or ignored by some pack file processors) – resource-specific data (See also, Data above)

IMPORTANT! The pack file specification does not detail configuration, options, and data values for resource items. Please refer to the documentation for the pack file processor you will be using for more information.

## Layouts

The layouts section of a module is an array containing one or more 'layout areas' to include in the output. There can be zero or more layout areas. Layout areas specify an area and contain a layout specification for the objects in that area. A layout area consists of the following named objects, although a specific pack file processor may add others:

1. "name" – (string; required) – the name of the layout area, should be unique within the layouts array 

2. "doc" – (string; optional) – documentation for the layout area, use to describe what the layout area is for 

3. "config" – (object; optional, but may be required or ignored by some pack file processors) – layout area-specific configuration (See also, Configuation above)

4. "options" – (object; optional, but may be required or ignored by some pack file processors) – layout area-specific options (See also, Options above)

5. "data" – (any type; optional, but may be required or ignored by some pack file processors) – layout area-specific data (See also, Data above)

6. "object-placements" – (array; required) – a list of object placements in the layout area, described below

Each object placement consists of a specification for zero to many locations of the same object within the layout area, to be processed by the pack file processor. A object placement consists of the following named objects, although a specific pack file processor may add others:

1. "object" - (string; required) – the name of the object to place zero to many times in the layout area; in most cases this will refer to an object-type resource, but the reference could be to an object specified in a separate pack file or to an object built into the runtime; should be unique within the object placements

2. "doc" – (string; optional) – documentation for the object placement, use to describe what the object placement is for 

3. "config" – (object; optional, but may be required or ignored by some pack file processors) – object placement-specific configuration (See also, Configuation above)

4. "options" – (object; optional, but may be required or ignored by some pack file processors) – object placement-specific options (See also, Options above)

5. "data" – (any type; optional, but may be required or ignored by some pack file processors) – object placement-specific data (See also, Data above)

6. "placements" – (array; required) – a list of placement commands for the object, described below

IMPORTANT! The pack file specification does not detail configuration, options, and data values for object placements. Please refer to the documentation for the pack file processor you will be using for more information.

Each placement command consists of the following objects:

1. "placer" – (string; required) – the placement algorithm to use

2. "doc" – (string; optional) – documentation for the placement command, use to describe what the placement is for 

3. "config" – (object; optional, but may be required or ignored by some pack file processors) – placement command-specific configuration (See also, Configuation above)

4. "options" – (object; optional, but may be required or ignored by some pack file processors) – placement command-specific options (See also, Options above)

5. "data" – (any type; optional, but may be required or ignored by some pack file processors) – placement command-specific data (See also, Data above)

IMPORTANT! The pack file specification does not detail configuration, options, and data values for placement commands. Please refer to the documentation for the pack file processor you will be using for more information.

## Wiring

The wiring section of a module is an array containing one or more 'modifier specs' to include in the output. There can be zero or more mod specs. Modifier are external code 'wired into' the runtime system to make it behave differently. The pack file processor determines which modifiers are supported. Each modifier spec details how to wire in a single external code resource as processed by the pack file processor. A modifier spec consists of the following named objects, although a specific pack file processor may add others:

1. "mod" – (string; required) – the name of the modifier to wire, should be unique within the wiring array 

2. "doc" – (string; optional) – documentation for the modifier spec, use to describe what the modifier spec is for 

3. "config" – (object; optional, but may be required or ignored by some pack file processors) – modifier spec-specific configuration (See also, Configuation above)

4. "options" – (object; optional, but may be required or ignored by some pack file processors) – modifier spec-specific options (See also, Options above)

5. "data" – (any type; optional, but may be required or ignored by some pack file processors) – modifier spec-specific data (See also, Data above)

IMPORTANT! The pack file specification does not detail configuration, options, and data values for mod spec items. Please refer to the documentation for the pack file processor you will be using for more information.

## Pack File Processors

Pack file processors are computer programs that read in a JSON file conforming to the pack file specification and use the data in the pack file to perform some work. The type of work a pack file processor might do includes, but is not limited to:

* Managing asset pipelines

* Generating code for a runtime system

* Creating distributable packages

* Configuring servers and external applications

## Pack Files as a DSL

Pack Files support enough complexity to act as a [DSL (Domain-Specific-Language)](https://en.wikipedia.org/wiki/Domain-specific_language) for arbitrary 3D Graphics applications. A DSL is basically a tiny programming language, often declarative, which is focused on a very specific problem domain. 

SquidSpace uses the Pack File DSL capability to declare the functionality for walkthrough simulations. However, Pack Files are generic enough to drive a completely different kind of 3D application through that application providing different pack file processors, resources, modifiers and/or doing object placement differently.

