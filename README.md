# SquidSpace.js

SquidSpace.js provides a thin runtime controller wrapper around [Babylon.js](https://www.babylonjs.com/) focused on creating 'walkthrough simulations' of spaces; recreated from real spaces or imaginary. SquidSpace is designed for high extensibility through events and hooks and is driven by 'pack files' containing or referencing 3D content and runtime configuration. The pack file specification provides a Domain Specific Language (DSL) useful for applications using 3D content.

SquidSpace.js is extended with 'mods' and includes a selection of generally useful mods. You can also create your own mods and wire them into SquidSpace.js at runtime.

SquidSpace.js also includes extensive tooling with features like code generation, asset pipeline management, asset optimization, build management, and more.

Documentation for SquidSpace starts [here](docs/introduction.md). There is a 'Getting Started' tutorial  [here](docs/getting-started.md). SquidSpace.js tool documention is [here](docs/squidspace-tools.md) and the API is [here](docs/squidspace-api.md). Documentation for the included SquidSpace.js mods and how to create your own mods is [here](docs/squidspace-mods.md).

NOTE: SquidSpace.js is a work in progress and not ready for prime time. The documentation, in particular, is mostly empty at this time.

## Releases

None at this time.

## SquidSpace.js is used by

* ConZealand's [Squid Hall](https://github.com/jackwilliambell/squidhall) project.

(If you are using SquidSpace.js for your own project, please contact the project maintainer so they can add you to this list!)

## Developer notes

Start by reading the code and [the documentation](docs/introduction.md). Look at [the examples](docs/examples.md). Dive in and create your own space. If you have questions or encounter bugs, please open an issue on Github.

### Copyright, License, and Reliquishement of Contributor Copyright

SquidSpace.js, which includes the squidspace.js library, the squidmods, the associated tooling, and the documentation are copyright the project maintainer, Jack William Bell, 2020. All other content, including HTML files, third party libraries, and 3D assets, are copyright their respective authors.

This project will remain available under the GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007 Open Source license until and unless that license is changed in a future version. Versions created prior to that point will retain that license. You are encouraged to branch this project and work on it separately under that license, with the understanding the copyright to any code created by the project maintainer resides with them.

By submitting a Pull Request to this project for anything but examples or third-party libraries you are required to agree (a) the work submitted is your own work and (b) to relinquish any copright claim to the maintainer of this project. If you are unable to agree to both (a) and (b) your PR will not be accepted. In the case of examples, the submitter will retain copyright to that example under the same terms as above, even if subsequently modified by others. The same applies to third party libraries. However, all owner-copyrighted work must have a compatable Open Source license.

This requirement exists because the maintainer of the project may wish in the future to sell separate commercial licenses to SquidSpace.js – while retaining the Open Source license for other uses – and it would be too difficult to determine who owns copyright on how much and which code when doing so. 

### Workflow for adding features

The most common workflow for adding features to SquidSpace is to create a feature branch. (See Branching and branch names below.) Then, inside the feature branch, implement your feature. Test and debug until the feature is working properly. 

When your feature is ready to be moved into master (or some other integration branch) you clean up the code, perform finl validation testing, and then submit a Pull Request.

### Playgrounds

Developers are encouraged to create 'playground' branches where they can experiment in the absense of a specific feature requirement. (See Branching and branch names below.)

### Branching and branch names

This project is using a strategy of making the master the latest integrated code. Version releases
are assigned to version named branches. The following naming rules and branch purposes apply:

* master - The main integration branch with the mainline code for the latest version in progress, does not need to pass tests, but ideally should pass tests for all features currently integrated. Once all features slated for the version in progress are complete, integrated, and pass all tests we create a version branch as described below.

* feature-[feature-name] - Feature-specific development branches. Branch names always start with 'Feature' and are followed with the name of the feature after a dash. Generally these branches should be merged to master once the feature is working. If we have more than one person working on a feature they can create sub-branches named feature-[feature-name]-[developer-name]-[purpose].

* bug-[issue-ID] - Bug/Issue-specific development branches. Branch names always start with 'Feature' and are followed with the name of the feature after a dash. Generally these branches should be merged to master once the bug is fixed. If we have more than one person working on a bug they can create sub-branches named bug-[issue-ID]-[developer-name]-[purpose].

* version-[date in yyymmdd format] - Version integration branches, created from master whenever we decide we have reached all goals for a particular version, using the date the branch was created as part of the name. Must pass all tests when being tagged. (See below.)

* Version branches themselves are separately versioned using tags named [version-name].[version-number] where version-number follows the version name and a dot (.), starting at 0 and incremented for each version tag. For example, a version branch created on July 1, 2020 would be named 'version-20200701' and would have an initial tag of 'version-20200701.0'. If we later fixed a couple of bugs and backported a feature we would create a new tag of 'version-20200701.1' once all tests are passed. Metadata about the version should be included in the tag description.

* [version-name]-['feature' or 'bug']-[feature name or issue ID] Version branches being worked on to fix bugs in or to backport features from later versions. Branch names always start with the version name and then follow the feature or bug naming convention. These should be merged back to the original version branch and a new version tag created once they pass all tests.

* [developer-name]-[purpose] - Dev playground branches. Branch names always start with the developer name and are followed with the purpose of the branch after a dash. Generally these branches should never be merged to another branch. In most cases code created in these branches should be moved and integrated into a feature branch by hand in order to avoid introducing unintended dependencies.


