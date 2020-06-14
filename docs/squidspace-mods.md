TODO: The following from older notes and needs extensive rework:

SquidSpace Mods are Javascript modules containing prebuilt SquidSpace Hook Functions and SquidSpace Event Handler Functions along with other helper and utility functions. Different types of SquidSpace Mods include:

* Simulation-specific Mods for a particular target virtual space

* Feature Mods adding generic or specific new functionality to SquidSpace at runtime

* Debug and editor Mods that assist when creating and debugging virtual spaces

By convention all SquidSpace Mods should provide the following two functions to make it easier to use the Mods from code and to enable specifying the mod in a world pack file:

1. wireSquidSpace(config <undefined, null or dict>, options<undefined, null or dict>) – Automatically attaches selected Hook Functions and adds Event Handler Functions to SquidSpace based on the configuration and options

2. unwireSquidSpace() – Automatically detaches Hook Functions and removes Event Handler Functions from SquidSpace previously added by wireSquidSpace() (alternatively the Extender can simply attempt to unwire everyting it may have wired)

However, it should also be possible to use SquidSpace Mods by 'hand-wiring' the Hook Functions and Event Handler Functions in code if you only want selected functionality and not everything wireSquidSpace() would add.

