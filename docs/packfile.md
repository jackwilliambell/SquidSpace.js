# Pack File Specification

Pack Files let you specify one or more modules, which are then used to generate
Javascript modules to be loaded into a 3d application controller. (See also, 
Pack Files as a DSL and Code Generation below.)

A Pack File consists of JSON data containing the following top-level sections:

1. "doc" – [optional] – Documentation for the file, use to describe what the file is for 

2. "config" – [required] – Global configuration details for the entire file (See also, Configuation below)
	 
3. "modules" – [required] – A specification for each module to be generated (see also, 
	Module Section below)
	
Pack File example:

	{
		"doc": "Example pack file.",
		"config": {
			"outdir": "libs/objects/"
		},
		"modules": [
			{
			    "name": "world",
				"doc": "example module.",
				"config": {
					"pretty-print": true,
					"pretty-offset": 3
				},
				"data": {
					"doc": "Data values are arbitrary and application-controller dependent.",
					"some-thing": "some value",
					"foo": {
						"bar": 1,
						"baz": true,
						"boo": "some value",
					},
					"world-origin": [32, 0, -20]
				},
				"objects": [
					{
						"name": "arena",
						"doc": "Example object.",
						"action": "insert",
						"file": "objects/arena.babylon",
						"config": {
							"space-object": true
						}
					},
					{
						"name": "beam",
						"action": "link",
						"root": "objects/"
						"file": "beam.babylon"
					}
				],
				"textures": [],
				"materials": [],
				"lights": [],
				"area-layouts": [
					{
						"area": "artshow",
						"origin": [10, 0, 30]
						"object-placements": [
							{
								"name": "floorsection",
								"object": "floor",
								"material": "marble",
								"placements": [
									{
										"placer": "single",
										"position": [0, 0.01, 0]
									}
								]
							}
						]
					}
				],
				wiring [
					"mod": "squidmmo"
					"config": {},
					"options": {},
				]
			}
		]
	}
	

## Configuration

TODO:

### Global Configuration

TODO:

Required global configuration values include:

* "outdir" – [required] – Directory to write output modules to

## Module Section

The Module Section of a Packfile is a list of one or more modules to generate. Each module 
list item consists of a specification for a single module to generate output for. 

A module specification consists of JSON data containing the following top-level sections:

1. "name" – [required] – The name of the module, used for both the module file name and the 
   variable name the module is assigned to (see also, Code Generation below)

2. "doc" – [optional] – Documentation for the module, use to describe what the module is for 

3. "config" – [required] – Configuration details for the module, currently 
   supported configuration values include:
	 - "pretty-print" – [optional, default is false] – If true, the module is formatted to
	   be readable, using the 'pretty-offset' value for formatting; if false the module
	   is 'packed'
	 - "pretty-offset" – [optional, default is '3'] – The number of spaces to offset when
	   pretty printing

4. "data" – [optional] – A dictionary of arbitrary values to pack into the file for use
   by the simulation controller at runtime (see also, Module Data below)

5. "objects" – [optional] – A zero of one or more objects to pack into the file (see also, Loader Sections below)

6. "textures" – [optional] – A zero of one or more textures to pack into the file (see also, Loader Sections below)

7. "materials" – [optional] – A zero of one or more materials to pack into the file (see also, Loader Sections below)

8. "lights" – [optional] – A list of zero or more lights to pack into the file (see also, Loader Sections below)

9. "area-layouts" – [optional] – A list of zero or more area layouts to pack into the file (see also, Area Layouts below)

10. "hooks" – [optional] – A dictionary of zero or more named hooks, specifying a plugin and
    function along with argument data for each hook (see also, Hooks below)

11. "events" – [optional] – A list of zero or more event handlers, specifying a plugin and
    function for the handler and the event it is handling  (see also, Events below)

The following sections are 'loader' sections and all share the same structure; with some extra
values depending on the section type (see also, Loader Sections below):

1. "objects" – defines how to pack and load object geometry/mesh data

2. "textures" – defines how to pack and load texture data   

3. "materials" – defines how to pack and load material data

4. "lights" – defines how to pack and load object light data 

### Loader Sections

All Loaders of a Module are lists of one or more sets of data loading specifications to add 
to the generated module. Each list item consists of a specification for a single set of 
data, whether object geometry, texture data, or whatever. A loader specification consists 
of the following values:

1. "name" – [required] – The name of the object, used for the object name in the generated 
   module (see also, Code Generation below) and used as the ID value for all the loaded meshes
   contained in the object at runtime

2. "doc" – [optional] – Documentation for the object, use to describe what the object is for 

3. "config" – [optional] – Configuration details for the module, currently 
   supported configuration values include:
	- "space-object" – [optional, default is false] – Specifies that the object is 
	  made visible in the space at startup using the object's own position data; 
	  otherwise the object is a 'layout object' and is made invisible in the space 
	  at startup and must be placed into the space using a layout (see also, Area 
	  Layouts below)

4. "action" – [required] – Specifies the packing action to take (see also, Packing Actions 
   and Sources below), must be one of the following action values:
	- "insert" – The object data will be inserted into the generated module from the specifed
	  file or from the specified data
	- "link" – The object data will be loaded at runtime using the specified root and file
	- "builtin" - The object is a Babylon.js or SquidSpace built-in, created using the 
	  specified data (see also, Builtins below) 

5. "root" – [required if action is 'link', otherwise do not use] – Specifies the URL root 
   to insert into the module (see also, Packing Actions below)

6. "file" – [required if action is 'link', required if action is 'insert' and no 'data' is
   specified, otherwise do not use] – Specifies the file containing object data to insert 
   into the module if the action is 'include' or the file name to fetch at the root location 
   if the action is 'link' (see also, Packing Actions and Sources below)

7. "data" – [required if action is 'builtin' or the action is 'insert' and no 'file' is 
   specified, otherwise do not use] – Contains the actual element data; as a string if 
   'insert' or as a builtin spec if 'builtin' (see also, Packing Actions and Sources and
   Builtins below)

#### Packing Actions and Sources

TODO: Document in more detail how Packing Actions work.

#### Loading Object Data

Object data consists of all the geometry/meshes for a single object added to the space.

The following values are specific to 'object' sections:

1. "loader" – [required if the action is 'insert' or 'link' and the object file type 
   is not '.babylon', otherwise do not use] – Used to specify the object loading plugin
   to use by a file name extension; currently supported loader values include:
	 - ".obj"
	 - TODO: Research what filename extensions Babylon.js loaders support and add here


#### Loading Texture Data

TODO: Implement and Document.


#### Loading Material Data

TODO: Implement and Document.


#### Loading Lights Data

TODO: Implement and Document.

### Builtins

Builtins are 3D content 'built in' to Babylon.js, SquidSpace or SquidSpace
Plugins with prepare handlers. What builtins are available depends on the 
particular plugins loaded. See the SquidSpace documentation for a list 
of the default builtins and their expected data layouts.

### Area Layouts

TODO: Implement and Document.

### Module Data

TODO: Implement and Document.

### Wiring

TODO: Implement and Document.

#### Mods

TODO: Implement and Document.

## Pack Files as a DSL

Pack Files support enough complexity to act as a [DSL (Domain-Specific-Language)](https://en.wikipedia.org/wiki/Domain-specific_language) 
for arbitrary 3D Graphics applications. A DSL is basically a tiny programming 
language, often declarative, which is focused on a very specific problem domain. 

SquidSpace uses the Pack File DSL capability to declare the functionality for 
walkthrough simulations. However, Pack Files are generic enough to drive a completely
different kind of 3D application through that application providing different 
data, builtins and hooks and/or doing object placement differently.

## Code Generation

The Pack File is used as input to a packer, which then generates some sort of 
application-specific code. The SquidSpace 'spacepacker' utility generates 
an older-style javascript module, which allows loading without being blocked by 
CORS when the requesting HTML file is opened from a file system. If you 'insert'
all of your 3D content into the generated modules you can run SquidSpace without
requiring a web server. 

For more details on the module file interface generated by spacepacker, see 
the SquidSpace documentation. 

NOTE: It is possible to create your own SquidSpace content modules from scratch
or to edit generated SquidSpace content modules. However, pack files are 
almost certainly simpler to use.

## Copyright 

SquidSpace, the associated tooling, and the documentation are copyright Jack William Bell 2020. 
All other content, including HTML files and 3D assets, are copyright their respective
authors.
