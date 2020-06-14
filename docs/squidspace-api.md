TODO: The following from older notes and needs extensive rework:

SquidSpace is a Javascript module of the old-fashioned kind you can load without CORS issues. It provides a basic scene manager and controller framework for [[Babylon.js]].

Squidspace itself provides a basic framework for loading and arranging objects in a 3D space, with a focus on creating 'walkthrough simulations'. It relies on code generated from SquidSpace Pack Files to know what 3D assets to load, how to place them in a 3D space, and how to wire them up to events.

SquidSpace is easily customized using SquidSpace Hook Functions and SquidSpace Event Handler Functions and may be extended with new features via [[SquidSpace Mods]].

## Hook Functions

Currently supported Hook Functions include:

* attachPrepareBuiltinsHook() [singular] called during prepareWorld() processing to add builtin 3D content

* attachPlacerHook() [plural] called by name during layout processing to perform complex or custom object placements

## Event Handler Functions

Event Handler Functions are functions with the 