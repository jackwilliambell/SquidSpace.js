# SquidSpace.js Module Files Reference

SquidSpace.js Module Files are JSON data used as inputs to several of the SquidSpace.js tools and as configuration for all of them. In particular they are inputs to the SquidSpace.js tools that manage the asset pipeline and generate runtime files.

All Module Files must conform to the [Module File Specification](modulefile-specification.md). However, that specification does not detail the content values of configuration, options, and data subsections of the different object types; leaving that to the implementation. In general, configuration ("config") subsections are used by tools that read and use Module Files to do work. Options ("options") and Data ("data") subsections are used by the runtime API and are usually passed through by the tools unchanged or with minimal modification; although (especially for resources) the code generation tools may create the data section at runtime based on the configuration and/or modify other values.

This document specifies the configuration subsection values supported by the SquidSpace.js tools. For more details on the tools please see the [SquidSpace.js tools documentation](squidspace-tools.md). 

This document also specifies the options and data subsection values used by the runtime SquidSpace.js API. For more details on the runtime API please see the [SquidSpace.js API reference](squidspace-api.md). 

## Module File Levels

This document is organized by "levels", starting from the top-level of the file and then drilling down through sections. The [Module File Specification](modulefile-specification.md) details how the sections are organized; this document expands on that for the SquidSpace.js-specific implementation by specifying the contents of the "config", "options" and "data" subsections of each section on each level.

The 'top' level is the 'Global Level', containing values applying to the whole Module File and, if the Module File is named 'world.module.json', to the project in the current working directory. For more detail see Global Level below.

3D assets are specified in the 'Resources Level', which allows you to describe textures, materials, 3D objects and even runtime code 'mods', either directly or by referencing external files. For more detail see Resources Level below.

How objects are arranged and displayed at runtime is specified in the 'Layouts Level', which allows you to describe what 3D object instances go where, using what materials. For more detail see Layouts Level below.

Events may be attached to 3D objects and other things in the 'Events Level', which allows you to specify what event along with related options and data to be passed to the event handler. For more detail see Events Level below.

Mods may be 'wired in' to the SquidSpace.js runtime in the 'Wiring Level', which allows you to specify exactly how a Mod modifies SquidSpace.js runtime behavior. For more detail see Wiring Level below.

Example:

	{
		"doc": "Top level.",
		"config": {
			"doc": "Global configuration values.",
			. . . Zero or more global configuration values.
		},
		"options": {
			"doc": "Global option values.",
			. . . Zero or more global options values.
		},
		"resources": {
			"doc": "Resources Level.",
			. . . Zero or more resource types.
		},
		"layouts": [
			"doc": "Layouts Level.",
			. . . Zero or more layout areas.
		],
		"events": [
			"doc": "Events Level.",
			. . . Zero or more event declarations.
		],
		"wiring": [
			"doc": "Wiring Level.",
			. . . Zero or more wiring declarations.
		]
	}

## How Module Files are Used

Module Files may be used in a number of ways by different SquidSpace.js tools and by third-party tools. The two most common usages are Code Generation (packing) and Asset Pipeline Management (pipelines).

### Providing Project Defaults and Information

All of the SquidSpace.js tools are configurable and each Module File can contain it's own configuration to drive the tools. The SquidSpace.js tools also support a 'default' configuration file, either provided with the tool command or behind the scenes by loading a file named 'world.module.json' in the working directory. In this way the 'world.module.json' file provides project-level defaults and information, although you can override it by specifying with the command a different module file containing a "config" section.

Module Files containing override configurations may consist of only the "config" section, the other sections are not required nor used.

For more details on the SquidSpace.js tools, see the [SquidSpace.js tools documentation](squidspace-tools.md). For more details on the possible configuration values see Global Configuration below.

### Code Generation and Data Packing 

The Module File may be used as input to a code generation tool, which then generates some sort of application-specific code from the data in the Module File; using the configuration sections to guide what code is generated. 

In this case the SquidSpace.js SQS 'generate' command outputs an older-style javascript module, which may have the file contents of asset files ran through filters and then 'packed' into it for each "resource" section item with a "pack-options" value in their "config" subsection. Data packing allows running a SquidSpace.js-based simulation in a web browser without being blocked by CORS – when the requesting HTML file is opened from a file system. See Resource Data Packing below.

For more details on the code generation, see the [SquidSpace.js Tools documentation](squidspace-tools.md). For more details on the SquidSpace.js tools, see the [SquidSpace.js tools documentation](squidspace-tools.md). For more details on the possible configuration values see Global Configuration and Standard Resource Configuration below.

NOTE: It is possible to create your own SquidSpace content modules from scratch or to edit generated SquidSpace content modules. However, this is discouraged. Besides, Module Files are almost certainly simpler to use.

### 3D Asset Pipeline Management

The Module File may be used as input to a asset file pipeline management tool, which then retrieves and processes remote files before placing them in a local cache for use by a code generation tool; using the configuration sections to guide the process.

In this case the SQS 'pipeline' command processes the "resources" section of a Module File and, for each resource with a with a "cache-options" value in their "config" subsection, the resource file is retrieved appropriately, passed through series of 'filters', and then written to the local cache. See Resource Data Caching below.

For more details on the SquidSpace.js tools, see the [SquidSpace.js tools documentation](squidspace-tools.md). For more details on the possible configuration values see Global Configuration and Standard Resource Configuration below.

## SquidSpace.js-Specific Module File Values

SquidSpace.js supports some special data values to extend the capabilities of Module Files. These include certain Standard Value Types, Hook Function References, and Filter Declarations.

### Standard Value Types

TODO: (size, position, rotation, etc.)

### Hook Function References

SquidSpace.js supports "Hook Functions" that extend different classes of functionality. For some of these functionality classes the Hook Functions are named, in which case the that Hook Function name may be referenced in the Module File data to use instead of the default SquidSpace.js functionality for that functionality class. 

NOTE: There are also unnamed Hook Functions that are not referenced in the Module File but may invisibly modify SquidSpace.js behavior at runtime or when processing the Module File. For more detail on Hook Functions see the [SquidSpace.js API reference](squidspace-api.md) and the [SquidSpace.js Hook Functions documentation](squidspace-hooks.md).
 
Examples:

	"objects": [
		{
			"name": "foo",
			"options": {
				"loader": "FooLoader",
				. . . Other object options values specific to fooLoader.
			},
			. . . Other object values.
		},
	],

In the above example the "loader" value is a reference to the "FooLoader" Hook Function. 

	{
		"place-name": "bar",
		"options": {
			"placer": "BarPlacer",
			. . . Other object options values specific to BarPlacer.
		},
		"data": {
			"user-name": "Scooby Doo",
			"greeting": "What ya doin' Scooby Do?"
		}
	}

In the above example the "placer" value is a reference to the "BarPlacer" Hook Function and there are some data values specific to the "BarPlacer" Hook Function.


### Filter Declarations

Filter declarations consist of a JSON array specifying a series of filter specifications through which data files are passed in order. Each filter specification declaration consists of the following:

* "filter" – [required; string] – The name of the filter function to use

* "options" – [optional; JSON object] – Options sent to the filter function when it is invoked, the contents of which are determined by the filter function implementation

* "data" – [optional; any] – Data value sent to the filter function when it is invoked, the contents of which are determined by the filter function implementation

When the tools execute the named filter function they pass the options and data values, along with the input and output file paths to use. For each set of filter declarations, every filter in the set is called once, in the supplied order, with the last filter providing the output of the filtering operation.

## Global Level 

The 'top' or Global Level of the file contains global values applying to the whole file. Besides the "config" and "options" global value subsections the Global Level contains "resources", "layouts", "events", and "wiring" level subsections with their own values.

NOTE: Although the [Module File Specification](modulefile-specification.md) also allows a "data" global value subsection at the Global Level, SquidSpace.js Module Files do not require this subsection and the tooling will ignore it if present.

### Global Configuration

Global Configuration must be of type JSON object. The Global Configuration in the main world Module File sets the defaults for all related Module Files in a project. See Providing Project Defaults and Information. The Global Configuration in all other Module Files may override the world Module File configuration, but only for that file.

The Global Configuration contains general configuration for the entire project:

* "build-dir" – [optional; string] – Directory used for build output files; may be overridden for individual modules; defaults to "build/"

* "generate-dir" – [optional; string] – Directory used for code generator output files; may be overridden for individual modules; defaults to "libs/modules" 

* "texture-dir" – [optional; string] – Directory containing textures to import; can be overridden for individual textures; defaults to "assets/textures/"

* "material-dir" – [optional; string] – Directory containing materials to import; can be overridden for individual materials; defaults to "assets/materials/"

* "object-dir" – [optional; string] – Directory containing objects to import; can be overridden for individual objects; defaults to "assets/objects/"

* "mod-dir" – [optional; string] – Directory containing mods or other Javascript files to import; can be overridden for individual mods; defaults to "assets/mods/"

* "pretty-print" – [optional; boolean; default is false] – If true, all module not specifying otherwise are formatted to be readable, using the "pretty-offset" value for formatting; if false the module is "packed"; can be overridden for individual modules

* "pretty-offset" – [optional; positive integer or zero; default is "3"] – The number of spaces to offset when pretty printing; can be overridden for individual modules

* "filter-profiles" – [optional; JSON object; default is none] – Specifies arrays of global filter declarations keyed by profile name, See Standard Resource Configuration, Filter Declarations

Example:

	{
		"doc": "Top level.",
		"config": {
			"doc": "Global configuration.",
			"out-dir": "build/",
			"texture-dir": "assets/textures/",
			"material-dir": "assets/materials/",
			"object-dir": "assets/objects/",
			"mod-dir": "supportlibs/mods/",
			"pretty-print": true,
			"pretty-offset": 3
			"filter-profiles": {
				"fooprofile": [
					{
						"filter": "FooFilter",
						"options": {
							. . . Filter options
						},
						"data": "Filter data"
					},
					. . . Other filter declarations.
				],
				"barprofile": [
					{
						"filter": "BarFilter",
						"options": {
							. . . Filter options
						},
						"data": "Filter data"
					},
					. . . Other filter declarations.
				]
				. . . Other filter profiles.
			}
			. . . Other global configuration values.
		},
		. . . Other module values.
	}


### Global Options

Global options must be of type JSON object. The following named values are supported:

* "world-origin" – [optional if it is a world module, otherwise do not use; array of x, y, z values; defaults is [0, 0, 0]] Used to specify the NW corner of the world as an origin point

TODO: Example

### Global Data

SquidSpace.js does not use global data at this time.

## Resources Level

Resources are JSON objects that contain none, some, or all of Textures ("textures"), Materials ("materials"), Objects ("objects"), Lights ("lights") and Mods ("mods") subsections. Each of these resource types are used at runtime by SquidSpace.js via a Loader Hook Function. (See Loader Hook Functions below.) 

Example:

	{
		"name": "exampleModule",
		"doc": "Module containing a resources section.",
		"resources": {
			"textures": [
				. . . Zero or more texture resources.
			],
			"materials": [
				. . . Zero or more material resources.
			],
			"objects": [
				. . . Zero or more object resources.
			],
			"mods": [
				. . . Zero or more mod resources.
			]
		},
		. . . Other module values.
	},

### Resource Data Caching

Besides controlling data packing during code generation, Module Files may also be used to manage an asset pipeline that manages a local resource cache, with optional optimization. This means there are three ways to manage file resources:

1. Local – The file is stored locally and may be accessed using a relative file path from the directory containing the Module File; "Local" files may be used with either "Insert" or "Link" ("Local" files are already in the cache)

3. Cached – The file is copied from a fully qualified file location or from a URL to a local file path and optimized via filters if necessary, after which it is available with a relative file path exactly like a "Local" file; "Cached" files may be used with either "Insert" or "Link" ("Cached" files are added to the cache)

2. Remote – The file is kept at remote location and always loaded from a fully qualified URL; "Remote" files may only be used with "Link" ("Remote" files are not cached and may even not be served from the same base URL if CORS headers are set up properly)

The directories used for "Local" or "Cached" files are specified in the global configuration. (See Global Configuration.)

Resource Data Caching is not a runtime functionality, therefore all cache control values are specified in the resource configuration. (See Standard Resource Configuration.)

Whether and how files are cached is specified in the configuration subsection of each individual resource.

IMPORTANT! It may be necessary to run asset pipeline management tools against a Module File to pre-load the cache before you can run the code generation tools, in cases where the file data is to be inserted.

### Resource Data Packing

Some resources may be specified entirely within the Module File using the option and data subsections. However, other resources may require external asset files of some kind. In the latter case SquidSpace.js provides a three ways to get the file data at runtime:

1. None – No file is used, if the specified Loader Hook Function requires data of some kind it is encoded directly into the Module File as a "data" subsection and copied into the generated code as the "data" value (basically the data is already 'packed')

2. Insert – The full contents of a file or URL are inserted directly into the generated code as the "data" value; using binary encoding, if required (in this way "Insert" is exactly like "None", except the data is 'packed' from a file)

3. Link – The contents of the file are loaded externally at runtime using a fully-specified URL or a relative link copied into the generated code as the "data" value

Whether and how data is packed is specified in the configuration subsection of each individual resource.

Advantages of "Insert" and "None" include the ability to load resources from the file system without experiencing CORS limitations and reducing the number of separate network streams required; with faster load times and no lost data due to network timeouts. Disadvantages of "Insert" and "None" includes the possibility of generating very large output files during the Pack step. In most cases "Insert" and "None" provide the best performance and stability.

Advantages of "Link" include the ability to utilize an external resource that might change over time and no CORS issues if your page headers are properly set up and you are not running from the file system. Disadvantages of Link include an increased number of network requests, lost data if the network times out, or the possibility the external resource may not be available at all for some reason.

Resource Data Packing is not a runtime functionality, therefore all pack control values are specified in the resource configuration. (See Standard Resource Configuration.) 

### Resource Loader Hook Functions

Resource Loader Hook Functions are added to SquidSpace.js at runtime by name and resource type before the buildWorld() API is called. For this reason a loader hook for a Texture resource can have the same name as a loader hook for a light resource, and so on. (See Hook Function References.)

TODO: 
	
NOTE: Resource Loader Hooks allow for alternative data loading methods, pre-defined resources (builtins) which are created from code, or any other resources created outside of the regular resource loading functionality. For more detail on Hook Functions see the [SquidSpace.js API documentation](squidspace-api.md) and the [SquidSpace.js Hooks documentation](squidspace-hooks.md).

### Standard Resource Configuration

All resource configuration subsections provide the following standard resource configuration values:

* "cache-options" – [optional; JSON object] – Specifies file cacheing options for the resource; default is no cacheing (local file resource only), options are:
	- "file-source" – [optional; string containing a fully-qualified file path, do not use if "url-source" is specified] – Specifies the source of the data to cache
	- "url-source" – [optional; string containing a fully-qualified URL, do not use if "file-source" is specified] – Specifies the source of the data to cache
	- "filters" – [optional; JSON array of Filter Declarations, do not use if "filter-profile" is supplied] – Specifies filters apply to the resource when it is being cached
	- "filter-profile" – [optional; string, do not use if "filters" is supplied] – Specifies a filter profile name from the global options "filter-profiles" to apply to the resource when it is being cached

* "pack-options" – [optional; JSON object] – Specifies file packing options for the resource; default is no packing (use "data" value as-is), options are:
	- "action": [optional; string containing one of "none", "insert", "link"] – Specifies file packing options for the resource; default is "none"
	- "filters" – [optional; JSON array of Filter Declarations, do not use if "filter-profile" is supplied] – Specifies filters to apply to the resource when it is being packed
	- "filter-profile" – [optional; string, do not use if "filters" is supplied] – Specifies a filter profile name from the global options "filter-profiles" to apply to the resource when it is being packed

* "dir" – [optional; string; use only if "file-name" is also specified] – Directory containing the file resource; overrides the global "dir" value for the resource section; when doing cacheing also specifies the directory the file is cached in
	- TODO: Not currently implemented.

* "file-name" – [required if "pack" is "insert" optional if "pack" is "link", string; do not use if "url" is specified, do not use if "pack" is "none"] – Specifies the file resource in the related resource directory; when doing cacheing also specifies the file name of the cached file

* "url" – [optional if "pack" is "link", string containing a fully-qualified URL; do not use if "file-name" is specified, do not use if "pack" is "insert" or "none"] – Specifies the file resource URL

During asset pipeline management, if "cache-options" is not supplied the resource is ignored. Otherwise the file will be cached during asset pipeline management. This means the file is fetched from the source specified in the "cache-options", selected optimizations are performed on the file, and then the file is saved to the related resource directory using the "file-name" value. (See Resource Data Caching.) For this reason the "cache-options" subsection must contain one of a "file-source" or a "url-source" value referring to a valid file of the correct resource type and, minimally, the "file-name" must also be specified in the configuration. Do not specify a "url" in the configuration.

During code generation, if the "pack-options" is not supplied or the "action" is "none" the resource "options" and "data" subsections are used as-is. If "action" is "link" and a "file-name" value is specified it is assumed the file will be served locally using a relative URL from the related resource directory and the resource "data" value will be a JSON object containing the keys "dir" and "file-name". If "pack" is "link" and a "url" value is specified it is assumed the file will be served remotely and the resource "data" value will be a JSON object containing the key "url". If "pack" is "insert" and a "file-name" value is specified, the file will be opened and inserted into the resource "data" value as a string. 

Examples:

	"textures": [
		{
			"resource-name": "foo",
			"config": {
				"doc": "No cache, no pack. (Default.) No 'config' subsection results in same behaviour.",
				"pack-options": {
					"action": "none"
				},
			},
			. . . Other texture values.
		},
		{
			"resource-name": "bar",
			"config": {
				"doc": "No cache, local link.",
				"pack-options": {
					"action": "link"
				},
				"file-name": "bar.png"
			},
			. . . Other texture values.
		},
		{
			"resource-name": "barinsert",
			"config": {
				"doc": "No cache, insert local file.",
				"pack-options": {
					"action": "insert"
				},
				"file-name": "bar.png"
			},
			. . . Other texture values.
		},
		{
			"resource-name": "barcachelink",
			"config": {
				"doc": "Cache, local link. Local source.",
				"cache-options": {
					"file-source": "~/images/bar.png"
				},
				"pack-options": {
					"action": "link"
				},
				"file-name": "bar.png"
			},
			. . . Other texture values.
		},
		{
			"resource-name": "barcacheinsert",
			"config": {
				"doc": "Cache, insert cached file.",
				"cache-options": {
					"file-source": "~/images/bar.png"
				},
				"pack-options": {
					"action": "insert"
				},
				"file-name": "bar.png"
			},
			. . . Other texture values.
		},
		{
			"resource-name": "baz",
			"config": {
				"doc": "No cache, remote link.",
				"pack-options": {
					"action": "link"
				},
				"url": "http://example.com/images/baz.png"
			},
			. . . Other texture values.
		},
		{
			"resource-name": "bazcachelink",
			"config": {
				"doc": "Cache, local link. Remote source.",
				"cache-options": {
					"url-source": "http://example.com/images/baz.png"
				},
				"pack-options": {
					"action": "link"
				},
				"file-name": "baz.png"
			},
			. . . Other texture values.
		},
		. . . Other textures.
	],

TODO: Pack options? 

### Standard Resource Options

The following Standard Resource Options are supported:

* "loader" - [optional; string containing a loader hook name; default is 'default'] – Specifies the loader hook function to use for the resource; see Hook Function References

Some resource types have their own standard options and Resource Loader Hooks may require options specific to the loader hook function.

Example:

	{
		"resource-name": "CustomObject",
		"options": {
			"doc": "'CustomObjectLoader' hook function creates object from scratch.",
			"loader": "CustomObjectLoader",
			"visible": true
		},
		"data": {
			"size": [13, 17.5],
			"position": [22.5, 0.01, 39],
			"material": "marble"
		}
	},
	{
		"resource-name": "foo",
		"config": {
			"pack-options": {
				"action": "insert"
			},
			"file-name": "foo.babylon"
		},
		"options": {
			"doc": "Default loader loads an object from data specified in the pack-options.",
			"loader": "default"
		}
	},

### Standard Resource Data

If the options "loader" value is a Resource Loader Hook Function the resource data subsection may contain any values expected by the Hook Function using any valid JSON type, including JSON objects and arrays. Module File extension value types such as Expression Strings and Binary Strings are allowed.

If the configuration specifies a "pack-options" subsection with an "action" value other than "none" the resource data subsection values are copied in from an external source; overwriting any values supplied for the data subsection. (See "pack-options" in the resource configuration section above.) When you are specifying a configuraton source any data section value you also specify will be overwritten with the data from the source. This means if you do specify a custom data subsection for a resource loader hook you must not specify "pack-options" in the configuration. 

TODO: Example

## Textures

Textures are an array of Texture JSON objects specified with the key "textures" from the Resources level. Textures do not have subsections other than "config", "options", and "data". 

Textures consists of image data that will be applied to a material. See Materials.

Example: 

	{
		"resource-name": "Foo",
		"config": {
			"cache-options": {
				"url-source": "https://example.com/images/foo.jpg",
				"filter-profile": "ArtJpg",
			},
			"doc": "Note the file name is a .png. The file will be converted from .jpg by the filters.",
			"file-name": "foo.png"
		},
		"options": {
			"loader": "default"
		}
	},

### Built-in Texture Loaders

SquidSpace.js provides the following 'built in' texture hooks:

* 'default' – A basic texture data loader that uses the built-in SquidSpace.loadTexture() function, which in turn is based on the Babylon.js Texture() constructor

* TODO: Various built-in procedural texture loaders

For more details on SquidSpace.js built-in loader functons, including their options and data values, see the [SquidSpace.js API Documentation](squidspace-api.md)

NOTE: One common way to create a custom loader hook is to call a built-in loader function from your hook function and then modify the returned texture for your specific requirements.

NOTE: The SquidSpace.js squidcommons mod provides a number of other commonly used loaders. 
TODO: Implement and document squidcommons.js.

### Texture Configuration

Texture resources support the Standard Resource Configuration. Textures created using the 'default' texture loader are likely to require data file or URL configuration. 

TODO: Example

### Texture Options

Texture resources support the Standard Resource Options. Other options are dependent on the loader hook specified.

TODO: Example

#### 'default' Texture Loader Options

The following options are specific to the texture resource 'default' loader hook; similar custom loader hooks should support these as well, unless the implementation and use case do not require them:

* "no-mipmap" – [optional; boolean; default is false] – Specifies if the texture will require mip maps or not

* "invert-y" – [optional; boolean; default is false] – Specifies if the texture needs to be inverted on the y axis during loading

* "mime-type" – [optional; string; default is none] – Specifies optional mime type information

### Texture Data

Texture resources supports the Standard Resource Data values. The data should specify all the geometry/meshes for a single object added to the space.

Texture resources support the Standard Resource Data using a standard image data type. Currently SquidSpace.js only supports data for non builtin textures.

TODO: Example

#### 'default' Texture Loader Data 

The texture resource 'default' loader hook supports the Standard Resource Data using configuration "pack-options", where the data is a supported image file type. See Standard Resource Configuration and Standard Resource Options.
   
## Materials

Materials are an array of Material JSON objects specified with the key "materials" from the Resources level. Materials do not have subsections other than "config", "options", and "data".

Materials consists of processed textures that will be applied to a objects. See Objects.

IMPORTANT! TODO: Material loaders are not currently implemented.

TODO: Example

### Built-in Material Loaders

SquidSpace.js provides the following 'built in' material hooks:

* 'default' – A basic material data loader that uses the built-in SquidSpace.loadMaterial() function, which in turn is based on the Babylon.js StandardMaterial() constructor

* TODO: Various built-in procedural and shader material loaders

For more details on SquidSpace.js built-in loader functons, including their options and data values, see the [SquidSpace.js API Documentation](squidspace-api.md)

NOTE: One common way to create a custom loader hook is to call a built-in loader function from your hook function and then modify the returned material for your specific requirements.

NOTE: The SquidSpace.js squidcommons mod provides a number of other commonly used loaders. 
TODO: Implement and document squidcommons.js.

### Material Configuration

At this time Materials do not have a data type that can be specified for inserting or loaded via a URL. All materials are specified with a Resource Loader Hook Function and their option and data values are dependent on the named Resource Loader Hook Function in the configuration.

### Material Options

Material resources support the Standard Resource Options. Other options are dependent on the loader hook specified.

TODO: Example

#### 'default' Material Loader Options

The following options are specific to the meterial resource 'default' loader hook; similar custom loader hooks should support these as well, unless the implementation and use case do not require them:

* TODO: specular options.

* TODO: orientation options.

* TODO: Alpha support options.

### Material Data

Material resource data values and types are dependent on the Resource Loader Hook Function specified in the material Options.

TODO: Example

#### 'default' Material Loader Data

The following data values are specific to the meterial resource 'default' loader hook; similar custom loader hooks should support these as well, unless the implementation and use case do not require them:

* "diffuse-color" – [optional; array of 3 color values; default is none, do not use if diffuse-texture is specified] – Specifies a diffuse color 

* "specular-color" – [optional; array of 3 color values; default is none, do not use if specular-texture is specified] – Specifies a specular color 

* "emissive-color" – [optional; array of 3 color values; default is none, do not use if emissive-texture is specified] – Specifies a emissive color 

* "ambient-color" – [optional; array of 3 color values; default is none, do not use if ambient-texture is specified] – Specifies a diffuse color 

* "diffuse-texture" – [optional; string name of a texture; default is none, do not use if diffuse-color is specified] – Specifies a diffuse texture

* "specular-texture" – [optional; string name of a texture; default is none, do not use if specular-color is specified] – Specifies a specular texture

* "emissive-texture" – [optional; string name of a texture; default is none, do not use if emissive-color is specified] – Specifies a emissive texture

* "ambient-texture" – [optional; string name of a texture; default is none, do not use if ambient-color is specified] – Specifies a diffuse texture

* TODO: other textures (reflection, refraction, others?)

## Objects

Objects are an array of 3D Object JSON objects specified with the key "objects" from the Resources level. Objects do not have subsections other than "config", "options", and "data".

NOTE: Lights and user cameras are considered a special case of 'Object' and are specified in the Objects section using special Object Loader hooks functions.

TODO: Examples.

### Built-in Object Loaders

SquidSpace.js provides the following 'built in' loader hooks:

* 'ObjectData' – A basic object data loader that uses the built-in SquidSpace.loadObject() function, which in turn is based on the Babylon.js SceneLoader.ImportMesh() function

* 'default' – An alias for 'ObjectData'; also the loader used if no loader is specified

* 'Floor' – A basic object builder/loader that uses the SquidSpace.makeFloor() function, which in turn is based on the Babylon.js Mesh.CreateGround() function

* 'UserCamera' – A basic object builder/loader that uses the SquidSpace.makeUserCamera() function, which in turn is based on the Babylon.js UniversalCamera() function

* TODO: Other built-in object loader hooks. (light, plane, basic geometry)

For more details on SquidSpace.js built-in loader functons, including their options and data values, see the [SquidSpace.js API Documentation](squidspace-api.md)

NOTE: One common way to create a custom loader hook is to call a built-in loader function from your hook function and then modify the returned meshes for your specific requirements.

NOTE: The SquidSpace.js squidcommons mod provides a number of other commonly used loaders. 
TODO: Implement and document squidcommons.js.

### Object Configuration

Object resources support the Standard Resource Configuration. Objects created using the 'default' object loader are likely to require data file or URL configuration.

### Object Options

Object resources support the Standard Resource Options. Other options are dependent on the loader hook specified.

#### 'ObjectData'/'default' Object Loader Options

The following options are specific to the object resource 'default' loader hook; similar custom loader hooks should support these as well, unless the implementation and use case do not require them:

* "visible" – [optional; boolean; default is false] – Specifies that the object is made visible in the space at startup using the object's own position data; otherwise the object is a "layout object" and is made invisible in the space at startup and must be placed into the space using a layout (see also, Area  Layouts below)

* "collision-detection" - [optional; boolean; default is true] – Specifies if collision detection is on for the object

* "mesh-name-filter" - [optional; string or array of strings; default is no filter] – Specifies one or more submeshes of the object which will be imported; filtering out other submeshes

* "loader-plugin" – [required if the object file type is not ".babylon", otherwise do not use, string containing a file extension; default is ".babylon"] – Used to specify the Babylon.js object loading plugin to use by file name extension; currently supported loader plugin values include:
	 - ".obj"
	 - ".gltf"
	 - ".glb"
	 - ".stl"
   
* TODO: Other loadObject() function options

#### 'Floor' Object Loader Options

The following options are specific to the object resource 'floor' loader hook; similar custom loader hooks should support these as well, unless the implementation and use case do not require them:

* "visible" – [optional; boolean; default is false] – Specifies that the object is made visible in the space at startup using the object's own position data; otherwise the object is a "layout object" and is made invisible in the space at startup and must be placed into the space using a layout (see also, Area  Layouts below)

* "collision-detection" - [optional; boolean; default is true] – Specifies if collision detection is on for the object. 

* "gravity" - [TODO] – Specifies the amount and direction of the floor's gravity
   
* TODO: Other loadObject() function options

#### 'UserCamera' Object Loader Options

The following options are specific to the object resource 'user-camera' loader hook; similar custom loader hooks should support these as well, unless the implementation and use case do not require them:

* "visible" – [optional; boolean; default is false] – Specifies that the object is made visible in the space at startup using the object's own position data; otherwise the object is a "layout object" and is made invisible in the space at startup and must be placed into the space using a layout (see also, Area  Layouts below)

* "collision-detection" - [optional; boolean; default is true] – Specifies if collision detection is on for the object

* "fly" - [optional; boolean; default is false] – Specifies if the user camera is affected by gravity

* "mode" - [optional; string; default is false] – Specifies if the user camera is affected by gravity
   
* TODO: Other options

### Object Data

Object resources supports the Standard Resource Data values. The data should specify all the geometry/meshes for a single object added to the space.

#### 'default' Object Loader Data 

The object resource 'default' loader hook supports the Standard Resource Data using configuration "pack-options", where the data is a supported 3D object file type. See Standard Resource Configuration and Standard Resource Options.
   
#### 'floor' Object Loader Data

The following data values are specific to the object resource 'floor' loader hook; similar custom loader hooks should support these as well, unless the implementation and use case do not require them:

* "size" - [required; array of x, y, z values] – Specifies the size of the floor

* "position" - [optional; array of x, y, z values; default is [0, 0, 0]] – Specifies the NW corner of the floor

* "material" - [optional; material name; default is no material] – Specifies the material to use for the floor
   
* TODO: Other data
   
#### 'user-camera' Object Loader Data

The following data values are specific to the object resource 'user-camera' loader hook; similar custom loader hooks should support these as well, unless the implementation and use case do not require them:

* "size" - [required; array of x, y, z values] – Specifies the size of the user camera collision ellipsoid

* "position" - [optional; array of x, y, z values; default is [0, 0, 0]] – Specifies the point position of the camera

* "target" - [optional; array of x, y, z values; default is [0, 0, 0]] – Specifies the point position of the camera target (what it is looking at)
   
* TODO: Other data

## Mods

TODO: Rewrite and make work.

The Mods section of a module is an array containing one or more "modifier specs" to include in the output. There can be zero or more mod specs. Modifier are external code "wired into" the runtime system to make it behave differently. The Module File processor determines which modifiers are supported. Each modifier spec details how to wire in a single external code resource as processed by the Module File processor. A modifier spec consists of the following named objects, although a specific Module File processor may add others:

* "mod" – (string; required) – the name of the modifier to wire, should be unique within the wiring array 

* "doc" – (string; optional) – documentation for the modifier spec, use to describe what the modifier spec is for 

* "config" – (object; optional, but may be required or ignored by some Module File processors) – modifier spec-specific configuration (See also, Configuation above)

* "options" – (object; optional, but may be required or ignored by some Module File processors) – modifier spec-specific options (See also, Options above)

* "data" – (any type; optional, but may be required or ignored by some Module File processors) – modifier spec-specific data (See also, Data above)

IMPORTANT! The Module File specification does not detail configuration, options, and data values for mod spec items. Please refer to the documentation for the Module File processor you will be using for more information.

### Mod Configuration

Mods are an array of Mod JSON objects specified with the key "mods" from the Resources level. Mods do not have subsections other than "config", "options", and "data".

### Mod Options

TODO: implement and document.

### Mod Data

TODO: implement and document.

## Layouts Level

Layouts are JSON arrays containing a list of Layout Area JSON objects. Layouts do not contain "config", "options" and "data" subsections.

## Layout Areas

Layout Areas are JSON objects specifying a single area within the 3D space, each of which contain zero or more "object placements" specifying what objects the Layout Area contains and where they are located. Layout areas are dimennsioned as rectangular with a width and depth and specified with an origin point based off of the world origin. 

Layout Areas are singlular, box shaped, and contiguous; but may overlap with other Layout Areas. The object placements they contain use the layout area origin point when placing "standalone" objects, but do not need to be located within the Layout Area.

### Layout Area Configuration

None at this time.

### Layout Area Options

Layout Area options must be of type JSON object. The following named values are supported:

* "size" – [optional; array of w, h, d values; default is the same as the world floor size] Specifies the size of the layout area in terms of width (w), height (h), and depth (d) where w is east/west, h is up/down and d is north/south

* "origin" – [optional; array of w, h, d values; default is the same as the world floor origin] Used to specify the NW corner of the Layout Area as an origin point, based on the World origin point where x is east/west, y is up/down and z is north/south

IMPORTANT! TODO: "size" and "origin" option values are not implemented at this time. All layout coordinates should be based on the world coordinates.

NOTE: When a Layout Area is specified in the World specification module and there is a Layout Area of the same name in another module, the "size" and/or "origin" values from the World specification module are used and the separate module's "size" and/or "origin" values are ignored. A common use case is to declare Layout Areas with no or few object placements in a World specification module and then re-use those named Layout Areas in other modules, adding other object placements in those modules.

### Layout Area Data

The Layout Area data consists of a JSON array of JSON objects specifying zero or more 'object placements'; each for a single object within a Layout Area. Object Placements contain zero or more 'placements' specifying different the places that object is located within the 3D space. 

Object Placements specify a named object, which must have been loaded as a resource in the current module, loaded as a resource in a separate module belonging to the same world, or included as a "builtin" by the runtime. All of the contained placements are for the same object using the same Object Placement options.

WARNING! Specifying an object name that is not loaded results in undefined behavior. 

### Object Placement Configuration

None at this time.

### Object Placement Standard Options

* "materials" – [optional; JSON array] – Specifies zero or more materials and the named submeshes to apply the materials to:
	- "material" – [required; name of a loaded material] - Specifies the material to use
	- "submesh" – [optional; name of a submesh within the object] – Specifies applying the named material to a named submesh; if not provided the material is applied to all submeshes

The Materials option specify a named material, which must have been loaded as a resource in the current module, loaded as a resource in a separate module belonging to the same world, or included as a "builtin" by the runtime. 

IMPORTANT! TODO: "material" and "submesh" option values are not implemented at this time.

NOTE: Applying materials to an Object Placement creates a "clone" of the named object and all placements are instances of that clone. If no materials are applied all placements are instances of the original object. Generally clones create more geometry in the World space and use more memory and other runtime resources, so they should be avoided if possible.

WARNING! Specifying a material name that is not loaded results in undefined behavior. 

WARNING! Specifying multiple materials for the same submesh results in undefined behavior. 

### Object Placement Data

The Object Placement data consists of an JSON array of JSON objects specifying locations in the World space of zero or more instances of the object specified in the containing Object Placement. Each Placement must specify a named "placer" hook to use in its options, which must be a SquidSpace.js builtin placer or a "Placer Hook" loaded from a mod. Placements must also specify a unique "place-name" used within the Layout Area for the object instance(s) being placed. 

NOTE: If a placer algorithm results in multiple instances of the object, the instances are named using the "place-name" specified, with a dash ('-") and a number appended, where that number is zero to the number of instances placed minus one.

### Placement Configuration

None at this time.

### Standard Placement Options

The following Standard Placement Options are supported:

* "placer" - [optional; string containing a placer hook name; default is 'default'] – Specifies the placer hook function to use for the object; see Hook Function References

Some Placer Hooks may require options specific to the placer hook function.

TODO: Example

### Standard Placement Data

Standard data values for all Placer Algorithms, both builtins and "placer hook functions" include:

* "position" – [optional; array of x, y, z values, defaults to [0, 0, 0]] – Specifies the position of the placed object; if "place-on-object" is not specified the position is based on the Layout Area's origin, otherwise the position is based on the named submesh's origin (TODO: Find out Babylon.js standard origin point for submeshes); see below for "place-on-object" values

* "rotation" – [optional; array of x, y, z rotation values, defaults to [0, 0, 0]] Specifies the rotation to apply to all submeshes of the object for each axis

All SquidSpace.js builtins "placer hook functions" also support:

* "place-on-object" – [optional; the name of an object previously placed in the World Space] – Specifies an object to place an instance of this Object Placement on

* "place-on-submesh" – [optional if "place-on-object" is specified, otherwise do not use; A submesh of the object specified with the "place-on-object" value

IMPORTANT! TODO: "place-on-object" and "place-on-submesh" option values are not implemented at this time.

NOTE: A common submesh naming pattern for objects which will have other objects placed on them is to use "top", "bottom", "left", "right", "front", and "back" if possible. 

WARNING: "place-on-object" values are dependent on object loading order. This is determined by the order in which the Module File modules are passed to SquidSpace.js, where the first module loaded is *always* the World specification module, after which other Module File modules are loaded in an order specified when SquidSpace.js is initialized at runtime.

TODO: Find a way to remove the loading order issue. One option is to defer on-object placements until all objects are placed, but that raises the issue of what happens when you place an object on an object placed on another object.

TODO: Example

### Builtin Placer Algorithms

SquidSpace.js includes a number of builtin placer algorithms, any of which may be overridden by a "placer hook function" using the same name and using the same options. 

The builtin placer algorithms are:

* "Single" (also "default") – Places a single instance of an object in a particular location; requires only standard placement options values

* "LinearSeries" - Places a row of instances of an object starting from a particular location; requires the standard placement options values, plus:
	- "count" – [required; integer] – Specifies number of object instances to place in a row
	- "across" – [optional; boolean; default is true] – Specifies whether the series goes from lesser "x" to a greater "x" value (true) or from lesser "z" to a greater "z" value (false)
	- "offset" – [optional; number; default is "0"] – Specifies in size units the offset between objects when they are placed, if a negative value the objects may overlap

* "RectangleSeries" - Places a rectangle of instances of an object starting from a particular location; requires the standard placement options values, plus:
	- "countWide" – [required; integer] – Specifies number of object instances to place in a row from lesser "x" to a greater "x" value
	- "countDeep" – [required; integer] – Specifies number of object instances to place in a row from lesser "z" to a greater "z" value
	- "lengthOffset" – [optional; number; default is "0"] – Specifies in size units the offset between objects along the "x" axis when they are placed, if a negative value the objects may overlap
	- "widthOffset" – [optional; number; default is "0"] – Specifies in size units the offset between objects along the "x" axis when they are placed, if a negative value the objects may overlap

* TODO: Other builtin placers as we add them.

NOTE: "linear-series" and "rectangle" placement objects only place along the "x" and "z" axis's. The "y" axis is fixed from the placement's position.

TODO: Consider ways to do "y" axis placement.

TODO: Determine if we need other builtin placement algorithms.

## Events Level

IMPORTANT! TODO: Events are not yet fully designed or implemented. This section will change.

Events are a JSON array of JSON objects specifying zero or more 'Event Declarations'; each for a single loaded object. Each Event Declaration may specify zero to many events for the object.

* "event" – [string; required] – Specifies the name to which all Event handlers for this event are bound

* "options" - [object; optional] – Contains options values passed to all handlers for the event at runtime when the Event is triggered

* "data" - [any type; optional] – Contains data passed to all handlers for the event at runtime when the Event is triggered

TODO: Layout Area-level events, such as "on-keypress", "on-user-enter/on-leave", etc.

For example, if an "on-click" event is attached to an object in the layout object placements (see below), the Events subsection of the Object's options might look like this:

	{
		"object": "foo-object",
		"events": {
			"on-click": [
				{
					"event": "foo-click-event",
					"options": {
						"foo": "bar",
						"count": 3
					},
					"data": "bar"
				}
			]
		}
		. . . Other object placement values.
	}

If the user then clicks the "foo-object" object at runtime, every event handler assigned to "foo-click-event" is called in turn using the arguments `("foo-object", {"foo": "bar","count": 3}, "bar")`.


## Event Declarations

Event Declarations specify a single event for a named object, which must have been loaded as a resource in the current module, loaded as a resource in a separate module belonging to the same world, or included as a "builtin" by the runtime. The event specification includes an attacher hook function to attach the event to the object, an event name, and the options and data related to that event. When an event of the event type occurs for the object, the source object, options, and data are sent to all event handlers associated with the event name. For more on event handlers, see Wiring Events.

Standard data values for all Event Declarations include:

* "object" – [required; the name of an object previously placed in the World Space] – Specifies the object the event is attached to

* "attacher" – [optional; string containing an event attachment hook name; default is 'default'] – Specifies the event attachment hook function that 'attaches' the event to the object

* "event-name" – [required; string] – Specifies the name event handlers for the event are listening for

* "options" – (object; optional) – option values to pass to the event handler when the event occurs (See also, Options above)

* "data" – (any type; optional) – data value(s) to pass to the event handler when the event occurs (See also, Data above)

### Event Types

TODO: 

## Wiring Level

TODO:
