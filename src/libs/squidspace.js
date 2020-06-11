// NOTE: Strict mode is causing problems I can't track down right now. 
// TODO: Find out why this breaks things and fix.
//'use strict'; 


/** The SquidSpace module provides a runtime for a simulated
	scene. It allows you to define a 'world' and will then run
	that world as a simulation using the world's settings and 
	allowing the user to move around it in similar to how they 
	navigate through a real world. 

	In most cases the physics used are simplified, but broadly similar 
	to the real-world. However, some physics parameters may 
	be changed. For example, gravity can be increased or decreased;
	affecting how far you can jump and how fast you move.

	NOTE: SquidSpace is intentionally implemented as an old-style Javascript 
	module, despite the fact it uses some newer Javascript functionality. 
	This allows SquidSpace.js to be used from a file system without creating
	requiring a server and side-steps CORS exceptions in general.

	## Some ideas for improvement

	Some options reduce CPU, but degrade the experience. One way to handle this might
	be to have a basic setting for 'low', 'medium', and 'high', where high uses every
	option and low uses the least. We could provide a way to choose the setting on the web
	page, which saves the setting to a cookie and reloads the page. The code would simply
	check the cookie on startup and use the appropriate options based on the setting.

	We need to figure out what is required to support tablets and phones and implement that.

	We need to determine if we want to support gamepads.

	SquidSpace, the associated tooling, and the documentation are copyright Jack William Bell 2020. 
    All other content, including HTML files and 3D assets, are copyright their respective
    authors.
*/

// Log levels.
const SS_LOG_ALL = 0;
const SS_LOG_DEBUG = 0;
const SS_LOG_INFO = 1;
const SS_LOG_WARN = 2;
const SS_LOG_ERROR = 3;
const SS_LOG_NONE = 9;

// SquidSpace core.
var SquidSpace = function() {
	
	//
	// Module data.
	//

	// TODO: Refactor to remove these. (Put in squidhall.js or SquidCommons?)
	var pnlwidth = 1;
	var norot = 0; // Do not rotate.
	var rot = Math.PI / 2; // Rotate 90 degrees.

	var logLevel = SS_LOG_ERROR;

	// This is the NW corner of the arena and the origin for layouts. 
	var floorOriginNW = [0, 0, 0]; 
	var floorSize = [0, 0];
	
	var textures = {};
	var materials = {};
	var objects = {};
	var lights = {};
	
	//
	// Hooks.
	//

	var logHook = function(message){console.log(message);};
	var prepareHook = function(scene){SquidSpace.logInfo("prepareHook()");};
	var buildHook = function(scene){SquidSpace.logInfo("buildHook()");};
	var textureLoaderHooks = {
		"default": function(texName, options, data, scene) {
			//return: object instance or undefined if object could not be loaded
		}
	};
	var materialLoaderHooks = {
		"default": function(matName, options, data, scene) {
			//return: object instance or undefined if object could not be loaded
		}
	};
	var objectLoaderHooks = {
		"objectData": function(objName, options, data, scene) {
			return SquidSpace.loadObject(objName, options, data, scene, null, null, false);
		},
		"floor": function(objName, options, data, scene) {
			// TODO: Size should be 3 elements.
			let sz = getValIfKeyInDict("size", data, [1, 1]);
			let pos = getValIfKeyInDict("position", data, [0, 0, 0]);
			let mn = getValIfKeyInDict("material", data, "");
			// TODO: Get material from material list by material name
			//       with a default if not loaded.
			return addFloor(pos[0], pos[1], pos[2], sz[0], sz[1], 
								materials.macadam, scene);
		},
		// TODO: Move this loader hook to squidhall.js
		"floorSection": function(objName, options, data, scene) {
			// TODO: Size should be 3 elements.
			let sz = getValIfKeyInDict("size", data, [1, 1]);
			let pos = getValIfKeyInDict("position", data, [0, 0, 0]);
			let mn = getValIfKeyInDict("material", data, "");
			// TODO: Get material from material list by material name
			//       with a default if not loaded.
			return addFloorSection(key, pos[0], pos[2], sz[0], sz[1], 
									materials.marble, scene);
		},
		"userCamera": function(objName, options, data, scene) {
			// TODO: Size should be 3 elements.
			let sz = getValIfKeyInDict("size", data, [1, 1]);
			let pos = getValIfKeyInDict("position", data, [0, 0, 0]);
			let mn = getValIfKeyInDict("material", data, "");
			let targetPos = getValIfKeyInDict("target-position", data, [20, 1.6, 20]);
			// TODO: Get material from material list by material name
			//       with a default if not loaded.
			return addCamera(pos[0], pos[1], pos[2], 
							targetPos[0], targetPos[1], targetPos[2], scene);
		}
	};
	objectLoaderHooks["default"] = objectLoaderHooks["objectData"]
	var modLoaderHooks = {
		"default": function(matName, options, data, scene) {
			//return: object instance or undefined if object could not be loaded
		}
	};
	var objectPlacerHooks = {
		"single": function(areaName, areaOptions, objectName, placeName, options, data, scene) {
			// TODO: Handle areaOptions as needed. 
			
			// Get values.
			let position = getValIfKeyInDict("position", data, [0, 0, 0]);
			let rotation = getValIfKeyInDict("rotation", data, [0, 0, 0]);
			let plc = [];
			
			// TODO: Placements currently do not include 'y' and only rotate on y axis.
			SquidSpace.addSingleInstanceToPlacements(placeName, plc, position[0], position[2], rotation[1]);

			if (plc.length > 0) {
				SquidSpace.placeObjectInstances(objectName, plc, undefined, scene);
				return true;
			}
			
			return false;
		},
		"linear-series": function(areaName, areaOptions, objectName, placeName, options, data, scene) {
			// TODO: Handle areaOptions as needed. 
			
			// Get values.
			let position = getValIfKeyInDict("position", data, [0, 0, 0]);
			let rotation = getValIfKeyInDict("rotation", data, [0, 0, 0]);
			let count = getValIfKeyInDict("count", data, 1);
			let across = getValIfKeyInDict("across", data, true);
			let offset = getValIfKeyInDict("offset", data, 0);
			let plc = [];
			
			// TODO: Placements currently do not include 'y' and only rotate on y axis.
			SquidSpace.addLinearSeriesToPlacements(placeName, plc, count, position[0], position[2], 
				offset, across, rotation[1]);
			
			if (plc.length > 0) {
				SquidSpace.placeObjectInstances(objectName, plc, undefined, scene);
				return true;
			}
			
			return false;
		},
		"rectangle-series": function(areaName, areaOptions, objectName, placeName, options, data, scene) {
			// TODO: Handle areaOptions as needed. 
			
			// Get values.
			let position = getValIfKeyInDict("position", data, [0, 0, 0]);
			let countWide = getValIfKeyInDict("countWide", data, 1);
			let countDeep = getValIfKeyInDict("countDeep", data, 1);
			let lengthOffset = getValIfKeyInDict("lengthOffset", data, 0);
			let widthOffset = getValIfKeyInDict("widthOffset", data, 0);
			let plc = [];
			
			// TODO: Placements currently do not include 'y' and only rotate on y axis.
			SquidSpace.addRectangleSeriesToPlacements(placeName, plc, countWide, countDeep, 
				position[0], position[2], lengthOffset, widthOffset);
			
			if (plc.length > 0) {
				SquidSpace.placeObjectInstances(objectName, plc, undefined, scene);
				return true;
			}
		
			return false;
		}
	};
	objectPlacerHooks["default"] = objectPlacerHooks["single"]
	var userModeHooks = {};
	
	//
	// Events.
	//
	
	var eventHandlers = {};
	
	//
	// Helper functions.
	//

	var getValIfKeyInDict = function(key, dict, defaultVal) {
		if ((dict != undefined) && (typeof dict === "object")) {
			if (key in dict) {
				return dict[key];
			}
		}
		
		return defaultVal;
	}
	
	//
	// Spec process functions.
	//
	// TODO: Wiring. 
	//
	
	var processLoaders = function(loaderSpecs, loaderHooks, scene, loaderTypeName) {
		// Process all the objects. This does not define processing order, so if we 
		// run into use cases where there are inter-object depedencies we'll need to
		// control order as well.
		for (key in loaderSpecs) {			
			// Get working values.
			let options = getValIfKeyInDict("options", loaderSpecs[key], {});
			let data = getValIfKeyInDict("data", loaderSpecs[key], undefined);
			let loaderName = getValIfKeyInDict("loader", options, "default");
			let loader = getValIfKeyInDict(loaderName, loaderHooks, undefined);
			
			SquidSpace.logDebug(`processLoaders(): ${key} spec / ${loaderName} loader.`);
			
			// Do we have a loader?
			if (typeof loader === "function") {
				// Load it!
				// TODO: Try/Catch and error handling.
				let result = loader(key, options, data, scene);
				
				// Do we have a result?
				if (result != undefined) {
					// Append the options.
					result.options = options;
					
					// TODO: Event processing.
					
					// Save the object for later.
					SquidSpace.addObjectInstance(key, result);
				}
			}
			else {
				SquidSpace.logError(`processLoaders(): No ${loaderTypeName} loader hook named '${loaderName}'.`);
			}
		}
	}
	
	var processLayouts = function(layoutsSpecs, scene) {
		// Process all the layouts. This does not define processing order, so if we 
		// run into use cases where there are inter-layout depedencies we'll need to
		// control order as well.
		for (key in layoutsSpecs) {
			SquidSpace.logDebug(`processLayouts(): ${key} area.`);

			// Get working values.
			let areaOptions = getValIfKeyInDict("options", layoutsSpecs[key], {});
			let objPlacements = getValIfKeyInDict("objectPlacements", layoutsSpecs[key], []);

			// TODO: Handle area layout options. (Currently ignoring them.) Things to do:
			// 1. Save area and provide a get function
			// 2. Rework options adding default values if needed
			// 3. Come up with more options

			// Process the object placements.
			for (placement of objPlacements) {
				// Get working values.
				let objectName = getValIfKeyInDict("object", placement, undefined);
				let placers = getValIfKeyInDict("placers", placement, []);

				// Do we have an object name?
				if (typeof objectName === "string") {
					SquidSpace.logDebug(`processLayouts(): ${key} area / ${objectName} object.`);

					// Process the placers.
					for (placer of placers) {
						// Get working values.
						let options = getValIfKeyInDict("options", placer, {});
						let data = getValIfKeyInDict("data", placer, {});
						let placeName = getValIfKeyInDict("place-name", placer, undefined);
						let placerName = getValIfKeyInDict("placer", options, "default");
						let placerFunc = getValIfKeyInDict(placerName, objectPlacerHooks, undefined);

						// do we have a place name?
						if (typeof placeName === "string") {
							SquidSpace.logDebug(
								`processLayouts(): ${key} area / ${objectName} object / ${placeName} place / ${placerName} placer.`);
							// Do we have a placer?
							if (typeof placerFunc === "function") {
								// Place it!
								// TODO: Try/Catch and error handling.
								let result = placerFunc(key, areaOptions, objectName, placeName,
									options, data, scene);
					
								// Do we have a result?
								if (result) {
									// TODO: Event processing.
								} else {
									SquidSpace.logError(
										`processLayouts(): Placer Hook function ${placerName} for ${placeName} of ${objectName} in ${key} area failed.`);
								}
							} else {
								SquidSpace.logError(
									`processLayouts(): No placer hook named '${placerName}'.`);
							}
						} else {
							SquidSpace.logError(
								`processLayouts(): Placement without a valid place name for ${objectName} in ${key} area.`);
						}
					}
				} else {
					SquidSpace.logError(
						`processLayouts(): Placement without a valid object name in ${key} area.`);
				}
			}
		}
	}
	
	//
	// Loader Builtins.
	//

	var addFloor = function (x, y, z, w, d, material, scene) {
		// NOTE: This makes the floor origin/size and the layout-based origin/size the same 
		//       so long as both use the same origin and size.
		// IMPORTANT! This function *must* be called before doing any layouts. 

		// Override global origin and size because everything else will calculate from that.
		// IMPORTANT! The origin specifies the point the floor starts from at the NW corner of
		// the arena. All layout offsets are calculated from that point!
		floorOriginNW = [x, y, z]; 
		floorSize = [w, d]; 

		// Calculate offsets.
		x = x + (w / 2);
		z = z - (d / 2);

		// Make the floor.
		let floor = BABYLON.Mesh.CreateGround('floor', w, d, 2, scene);
		floor.position = new BABYLON.Vector3(x, y, z);
	    floor.material = material;
	    //floor.receiveShadows = true; // This seems to increase the CPU requirements by quite a bit.
		floor.checkCollisions = true;

		return [floor];
	}

	// TODO: Refactor this into squidhall.js
	var addFloorSection = function(secName, x, z, w, d, material, scene) {
		var floorSection = BABYLON.MeshBuilder.CreatePlane(secName, 
												{width: w, height:d}, scene);
		floorSection.position = new SquidSpace.makeLayoutVector(x, 0.001, z, w, d);
		floorSection.rotation = new BABYLON.Vector3(Math.PI / 2, 0, 0);
	    floorSection.material = material;
		floorSection.material.backFaceCulling = false;
		return [floorSection];
	}
	
	var addCamera = function(x, y, z, targetX, targetY, targetZ, scene) {

		// Add a camera to the scene and attach it to the canvas
		// TODO: Specify camera in world file.
		// TODO: Support switching to VirtualJoysticksCamera if running on a tablet or phone.
		// See https://doc.babylonjs.com/babylon101/cameras#virtual-joysticks-camera
		let camera = new BABYLON.UniversalCamera("usercamera", 
												SquidSpace.makePointVector(x, y, x), scene);
		//var camera = new BABYLON.FreeCamera("default camera", new BABYLON.Vector3(0, 5, -10), scene);
		//var camera = new BABYLON.FlyCamera("default camera", new BABYLON.Vector3(0, 5, -10), scene);
		camera.setTarget(new SquidSpace.makePointVector(targetX, targetY, targetZ));
		camera.attachControl(canvas, true);

		//
		// Enable walking.
		// TODO: Specify the options in world file, add support code to squidspace.js
		//

		// Set the ellipsoid around the camera for collision detection.
		// TODO: Experiment with values to find best.
		// TODO: Consider making pack file settable.
		// NOTE: ellipsoid values must be carefully chosen to reduce image tearing when
		//       up close to objects, while still allowing you to navigate around without
		//       getting stuck between things. However, this does mean you can't get really
		//       close to anything straight in front of you.
		camera.ellipsoid = new BABYLON.Vector3(1, 1, 1);

		// WASD movement.
	    camera.keysUp.push(87);    //W
	    camera.keysDown.push(83)   //D
	    camera.keysLeft.push(65);  //A
	    camera.keysRight.push(68); //S

		// Support gamepad.
		//camera.inputs.add(new BABYLON.FreeCameraGamepadInput());
		//camera.inputs.attached.gamepad.gamepadAngularSensibility = 250;

		// Apply collisions and gravity to the active camera
		camera.checkCollisions = true;
		camera.applyGravity = true;

		/* TODO: Remove and refactor.
		// Other camera settings.
		// TODO: Experiment with values to find best.
		// TODO: Consider making pack file settable or even dynamically settable.
		camera.fov = 1.3;
		if (!debugCamera) {
			//camera.speed = 0.15; // Lower values slow movement down.
			camera.speed = 0.20;
			//camera.speed = 0.25; .
			//camera.speed = 0.55; 
		    //camera.inertia = 0.2; // Lower values slow movement down, but also affect look/turning.
			//camera.inertia = 0.4;
			//camera.inertia = 0.6;
			camera.inertia = 0.8;
			//camera.inertia = 1; // DO NOT USE - you will not like it.
			//camera.angularSensibility = 500; // Lower values increase look/turning speed, default is 2000.
			camera.angularSensibility = 750;
			//camera.angularSensibility = 1000;
		}
		*/
		
		return [camera];
	}
		
	//
	// Layout Builtins.
	//
	
	// TODO: Implement.

	return {
		//
		// Public helper functions.
		//
		
		/** Returns an array of points in the form [x, y, z], where the points are 
		    calculated from the passed points using the following rules:

			1. x and z are normalized from the floor origin point, located in the 
		       NW corner of the floor
		
			TODO: Add origin argument, which if undefined defaults to floor origin.
		 */
		makePointXYX: function(x, y, z) {
			// TODO: This function was created because I don't understand how Babylon
			//       does local vectors and was under time pressure, so couldn't do the
			//       research. At some point we need to use the BJS code instead, but could
			//       just insert it here without breaking dependent code.
			// IMPORTANT! The origin specifies the point the floor starts from at the NW corner of
			// the arena. All layout offsets are calculated from that point!

			return [
				floorOriginNW[0] + x, 
				floorOriginNW[1] + y, 
				floorOriginNW[2] + (z * -1)
			];
		},
		
		/** Returns an array of points in the form [x, y, z], where the points are 
		    calculated from the passed points using the following rules:
			
			1. x and z are normalized from the floor origin point, located in the 
		       NW corner of the floor
		
			2. x and z are further normalized to the NW corner of the rectangle 
		       specified by w and d
		
			TODO: Add origin argument, which if undefined defaults to floor origin.
		 */
		makeLayoutXYZ: function(x, y, z, w, d) {
			// TODO: This function was created because I don't understand how Babylon
			//       does local vectors and was under time pressure, so couldn't do the
			//       research. At some point we need to use the BJS code instead, but could
			//       just insert it here without breaking dependent code.
			// IMPORTANT! The origin specifies the point the floor starts from at the NW corner of
			// the arena. All layout offsets are calculated from that point!

			return [
				floorOriginNW[0] + x + (w / 2), 
				floorOriginNW[1] + y, 
				floorOriginNW[2] + (z * -1) - (d / 2)
			];
		},


		/** Returns a Babylon Vector, where the points are 
		    calculated from the passed points using the following rules:
	
			1. x and z are normalized from the floor origin point, located in the 
		       NW corner of the floor
		
			TODO: Add origin argument, which if undefined defaults to floor origin.
		 */
		makePointVector: function(x, y, z) {
			// TODO: This function was created because I don't understand how Babylon
			//       does local vectors and was under time pressure, so couldn't do the
			//       research. At some point we need to use the BJS code instead, but could
			//       just insert it here without breaking dependent code.
			// IMPORTANT! The origin specifies the point the floor starts from at the NW corner of
			// the arena. All layout offsets are calculated from that point!

			return new BABYLON.Vector3(
				floorOriginNW[0] + x, 
				floorOriginNW[1] + y, 
				floorOriginNW[2] + (z * -1)
			);
		},


		/** Returns Babylon Vector, where the points are 
		    calculated from the passed points using the following rules:
		
			1. x and z are normalized from the floor origin point, located in the 
		       NW corner of the floor
	
			2. x and z are further normalized to the NW corner of the rectangle 
		       specified by w and d
		
			TODO: Add origin argument, which if undefined defaults to floor origin.
		 */
		makeLayoutVector: function(x, y, z, w, d) {
			// TODO: This function was created because I don't understand how Babylon
			//       does local vectors and was under time pressure, so couldn't do the
			//       research. At some point we need to use the BJS code instead, but could
			//       just insert it here without breaking dependent code.
			// IMPORTANT! The origin specifies the point the floor starts from at the NW corner of
			// the arena. All layout offsets are calculated from that point!

			return new BABYLON.Vector3(
				floorOriginNW[0] + x + (w / 2), 
				floorOriginNW[1] + y, 
				floorOriginNW[2] + (z * -1) - (d / 2)
			);
		},

		//
		// Texture management functions.
		//
		// TODO: More.
		//
		
		addTextureInstance: function(texName, texture) {		
			// TODO: Check if texName already exists. Decide how to handle. (Error?)
			
			// Keep a local reference to the texture.
			textures[texName] = texture;
		},
		
		/** Returns the texture for the passed texture name, assuming the texture was 
		specified in the pack file, loaded with the loadTexture(),
		or added with the addTextureInstance() function. If the texture is available it 
		is returned. If it was not it returns 'undefined'. */
		getTexture: function(texName) {
			if (texName in textures) {
				return textures[texName];
			}
			
			return undefined;
		},

		//
		// Material management functions.
		//
		// TODO: More.
		//
		
		addMaterialInstance: function(matName, material) {		
			// TODO: Check if matName already exists. Decide how to handle. (Error?)
			
			// Keep a local reference to the material.
			materials[matName] = material;
		},
		
		
		/** Returns the material for the passed material name, assuming the material was 
		specified in the pack file, loaded with the loadMaterial(),
		or added with the addMaterialInstance() function. If the texture is available it 
		is returned. If it was not it returns 'undefined'. */
		getMaterial: function(matName) {
			if (matName in materials) {
				return materials[matName];
			}
			
			return undefined;
		},

		//
		// Object management functions.
		//
		

		/** Loads the named object using the passed options and data. Calls the passed success
		    function if the object is loaded calls the passed fail function if the object could 
			not be loaded. Unless the doNotAdd paramater is true it adds the object to 
			the internal list, making it available to the getLoadedObjectMeshes() function. 
			Returns the loaded object or 'undefined'. 
		
		    The options and data values are the same as used for pack file options with the 
			'default' loader. 
		*/
		loadObject: function(objName, options, data, scene, onSuccessFunc, onFailFunc, doNotAdd) {
			let obj = undefined;
			let visible = getValIfKeyInDict("visible", options, false);
			let collisionDetect = getValIfKeyInDict("collision-detection", options, true);
			// For meshNameFilter, empty string means import *all* meshes in the object.
			let meshNameFilter = getValIfKeyInDict("mesh-name-filter", options, ""); 
			let loaderPluginExtension = getValIfKeyInDict("loader-plugin", options, false);
			
			let rootUrl = "";
			let sceneFilename = null;
			if (typeof data === "string") {
				sceneFilename = "data:" + data;
			}
			else if ((typeof data === "object") && ("url" in data)) {
				rootUrl = data["url"];
			}
			else if ((typeof data === "object") && ("dir" in data) && ("file-name" in data)) {
				rootUrl = data["dir"];
				sceneFilename = "data:" + data["file-name"];
			}
			else {
				// TODO: Log error. 
				return undefined;
			}
			
			// TODO: Events support.
			
			BABYLON.SceneLoader.ImportMesh(meshNameFilter, rootUrl, sceneFilename, scene, 
					function(newMeshes) {
						// Process each mesh based on the options.
						for (mesh of newMeshes) {
							mesh.isVisible = visible;
							mesh.checkCollisions = collisionDetect;
						}
						
						// Save the meshes for later?
						if (!doNotAdd) SquidSpace.addObjectInstance(objName, newMeshes);
						
						// Is there a success function?
						if (typeof onSuccessFunc == "function") onSuccessFunc(newMeshes);
						
						// We are good!
						// NOTE: This could be a bug if BJS changes the ImportMesh() function
						//       to process this in a different thread! It would be better if they
						//       used a 'future', but they didn't. 
						// TODO: Research workarounds for ImportMesh().
						obj = newMeshes;
					}, null,
					function(scene, message, exception) {
						SquidSpace.logError("== '" + objName + 
							"' mesh import failed. ==\n  Message: " + 
							message.substring(0, 64) + " ... " +  message.substring(message.length - 64) +
							"\n  Exception: " + exception);
							
							// Is there a fail function?
							if (typeof onSuccessFunc == "function") onFailFunc(scene, message, exception);
					}, 
					loaderPluginExtension); 
			
			// Done.
			return obj;
		},
		
		
		/** Makes a cloned copy of the object for the passed object name, assinging the 
		    passed clone object name to the new object. Returns the cloned meshes or 
		    'undefined' if it fails. 
		*/
		cloneObject: function(objName, cloneObjName) {
			let meshes = SquidSpace.getLoadedObjectMeshes(objName);
			let clone = [];
			
			// If we have meshes, clone them.
			if (typeof meshes != "undefined") {
				for (m of meshes) {
					clone.push(m.clone(cloneObjName));
				}
			}

			// Did we get anything?
			if (clone.length > 0) {
				// Add the cloned object to the internal list.
				SquidSpace.addObjectInstance(cloneObjName, clone);
				
				// We are good!
				return clone;
			}
			
			return undefined;
		},
		
		addObjectInstance: function(objName, meshes) {
			// Force ID of all meshes to the object name.
			for (m of meshes) {
				m.id = objName;
			}
			
			// TODO: Check if objName already exists. Decide how to handle. (Error?)
			
			// Keep a local reference to the object.
			objects[objName] = meshes;
		},
		
		/** Returns the meshes for the passed object name, assuming the object was 
			specified in the pack file, loaded with the loadObject(), cloned with cloneObject,
			or added with the addObject() function. If the object is available it returns 
			an array of meshes for the object. If it was not it returns 'undefined'. 
		*/
		getLoadedObjectMeshes: function(objName) {
			if (objName in objects) {
				return objects[objName];
			}
			
			return undefined;
		},

		//
		// Layout helper functions.
		//
	
		/** Adds a single instance to a placements array at the passed position
		    and rotation.
		
		    TODO: Support y.
		
		    TODO: Currently only supports horizontally aligned placements, add ability 
		    to do vertical.
		 */
		addSingleInstanceToPlacements: function(instanceName, placements, x, z, rotation) {
			placements.push([instanceName, x, z, rotation]);
		},
	
		/** Adds a count series of placements elements to an existing placements array, 
			starting at the the provided x and z and separated by the provided offset. If 
			across is true the elements start at the west and go east. Otherwise the elements
			start at the south and go north. The passed rotation is used for all elements
			in the series.
		
		    TODO: Support y.
		
		    TODO: Currently only supports horizontally aligned placements, add ability 
		    to do vertical.
		*/
		addLinearSeriesToPlacements: function(seriesName, placements, count, x, z, offset,
												across, rotation) {
			for (let i = 0;i < count;i++) {
				placements.push([seriesName + i, x, z, rotation])
				if (across) {
					x += offset;
				}
				else {
					z += offset;
				}
			}
		},

		/** Adds a count wide and count deep series of placements elements to an 
		    existing placements array in the form of a rectangle, 
			starting at the the provided x and z and separated by the provided offsets. 
		    The passed rotation is used for all elements in the series.
		
		    TODO: Support y.
		
		    TODO: Currently only supports horizontally aligned placements, add ability 
		    to do vertical.
		
		    TODO: Currently only supports horizontally aligned placements, add ability 
		    to do vertical.
		*/
		addRectangleSeriesToPlacements: function(seriesName, placements, countWide, countDeep,
													x, z, lengthOffset, widthOffset) {
			// Calculate starting positions.
			let wx = x + widthOffset;
			let bz = z + (countDeep * lengthOffset) - widthOffset;
			let rx = x + (countWide * lengthOffset) - lengthOffset;

			// Do width placements.
			for (let i = 0;i < countWide;i++) {
				SquidSpace.addLinearSeriesToPlacements(seriesName + "-top-", placements, 
													countWide, wx, z, lengthOffset, true, norot);
				SquidSpace.addLinearSeriesToPlacements(seriesName + "-bottom-", placements, 
													countWide, wx, bz, lengthOffset, true, norot);
			}

			// Do depth placements.
			for (let i = 0;i< countDeep;i++) {
				SquidSpace.addLinearSeriesToPlacements(seriesName + "-left-", placements, 
								countDeep, x - lengthOffset, z + lengthOffset, lengthOffset, false, rot);
				SquidSpace.addLinearSeriesToPlacements(seriesName + "-right-", placements, 
								countDeep, rx, z + lengthOffset, lengthOffset, false, rot);
			}
		},

		/** Places instances of the object referred to by object name (string) using 
		    the passed material name (string, null or undefined), using the locations and 
		    rotations specified in the passed placements array.
		
			TODO: Material not currently supported. Consider removing it, since it isn't
		          clear which mesh would get the material. (All meshes in object?)
		 */
		placeObjectInstances: function(objName, placements, matName, scene) {
			// Get the meshes.
			let meshes = SquidSpace.getLoadedObjectMeshes(objName);
			if ((typeof meshes != "object") && !(meshes instanceof Array) && (meshes.length < 1))
				 throw `Mesh not loaded for object reference: ''${objName}''.`;
		
			for (instance of placements) {
				let newMeshes = [];
				for (mesh of meshes) {
					// Create an instance and add it to the new meshes.
					let m = mesh.createInstance(instance[0]);
					newMeshes.push(m);
					
					// Set placement values.
					m.position = SquidSpace.makeLayoutVector(
										instance[1], 0.01, instance[2], m.scaling.x, m.scaling.y);
					if (placements[3] != 0) {
						m.rotate(BABYLON.Axis.Y, instance[3]);
						m.position.z -= (pnlwidth / 2);
					}
					
					// Set other values.
					// TODO: Do we want to add these to placement somehow?
					m.checkCollisions = true;
					m.visible = true;
					// TODO: Fix this. IMPORTANT!
					//let bv = m.getBoundingInfo().boundingBox.minimum;
				}
				SquidSpace.addObjectInstance(instance[0], newMeshes);			
			}
		},

		//
		// Logging.
		//
		
		/** Sets the current log level to the passed level, if valid. */
		setLogLevel: function(logLvl) {
			// Is it a valid log level?
			if ([SS_LOG_DEBUG, SS_LOG_INFO, SS_LOG_WARN, SS_LOG_ERROR].includes(logLvl)) {
				// Set the log level.
				logLevel = logLvl;
				SquidSpace.logDebug(`setLogLevel(): Setting log level to ${logLevel}.`);
			}
			else {
				SquidSpace.logError(`setLogLevel(): Invalid log level: ${logLevel} - could not set.`);
				// TODO: Throw exception?
			}
		},
		
		/** Logs a debug-level message. */
		logDebug: function(message) {
			if (logLevel <= SS_LOG_DEBUG) {
				logHook("[DEBUG] " + message);
			}
		},
		
		/** Logs an info-level message. */
		logInfo: function(message) {
			if (logLevel <= SS_LOG_INFO) {
				logHook("[INFO] " + message);
			}
		},
		
		/** Logs a warning-level message. */
		logWarn: function(message) {
			if (logLevel <= SS_LOG_WARN) {
				logHook("[WARNING] " + message);
			}
		},
		
		/** Logs an error-level message. */
		logError: function(message) {
			if (logLevel <= SS_LOG_ERROR) {
				logHook("[ERROR] " + message);
			}
		},
				
		//
		// Hooks.
		//
		
	 	/** The logHook is called by the SquidSpace.js logging functions to output 
			a formatted message to a logging service. The default implmentation
			uses console.log(), but you can attach a hook function to override that and 
			do something different; including sending log output to a server for 
			remote debugging.
		
		    Signature: hookFunction(message)
		 */
		attachLogHook: function(hookFunction) {
			let oldHook = logHook;
			logHook = hookFunction;
			return oldHook;
		},
		
	 	/** The prepareHook is called before buildWorld() processing to add builtins or do 
			other things to the scene in preparation for building the world.
		
		    Signature: hookFunction(scene)
		 */
		attachPrepareHook: function(hookFunction) {
			let oldHook = prepareHook;
			prepareHook = hookFunction;
			return oldHook;
		},
		
	 	/** The BuildHook is called after buildWorld() processing to add extra 3D 
			content, attach non-SquidSpace.js events outside or do other things to the 
			scene in preparation for running the world.
		
		    Signature: hookFunction(scene)
		 */
		attachBuildHook: function(hookFunction) {
			let oldHook = prepareHook;
			buildHook = hookFunction;
			return oldHook;
		},
		
		// TODO: Loader hooks for textures and materials.
		
	 	/** ObjectLoaderHooks are called by name during object loading to create new 
			instances of complex or custom objects.
	
		    Signature: hookFunction(objName, options, data, scene) {return: 
			                        object instance or undefined if object could not be loaded}
		 */
		attachObjectLoaderHook: function(hookName, hookFunction) {
			let oldHook = objectLoaderHooks[hookName];
			objectLoaderHooks[hookName] = hookFunction;
			return oldHook;
		},
	
	 	/** ObjectPlacerHooks are called by name during layout processing to perform complex
		    or custom object placements.
	
		    Signature: hookFunction(areaName, areaOptions, objectName, placeName, 
		                            options, data, scene) {return: boolean}
		 */
		attachObjectPlacerHook: function(hookName, hookFunction) {
			let oldHook = objectPlacerHooks[hookName];
			objectPlacerHooks[hookName] = hookFunction;
			return oldHook;
		},
		
	 	/** The UserModeHook is called by name to modify the user camera settings and 
			other user related values with the setUserMode() function, where the hook 
			name is the name of the user mode.
		
			The SquidSpace.js SquidDebug mod adds 'debug', 'debug-inspect' and 
			'inspect' user modes.
		
			The SquidSpace.js SquidWalkthrough mod adds 'fly', 'walk' and 'run' user modes.
		
			NOTE: The user camera is set up as an object during worldBuild() processing. Some 
			user cameras may not be compatable with particular user modes. 
	
		    Signature: hookFunction(options, data, userCamera, scene) {return: boolean}
		 */
		attachUserModeHook: function(hookName, hookFunction) {
			let oldHook = userModeHooks[hookName];
			userModeHooks[hookName] = hookFunction;
			return oldHook;
		},

		//
		// Events.
		//

		attachClickEventToObject: function(objName, eventName, eventData, scene) {
			meshes = SquidSpace.getLoadedObjectMeshes(objName);
			
			if (typeof meshes != "undefined") {
				for (mesh of meshes) {
					// TODO: Wrap with try-catch and then raise custom error or log or something.
					mesh.actionManager = new BABYLON.ActionManager(scene);
					mesh.actionManager.registerAction(
						new BABYLON.ExecuteCodeAction(
							{
								trigger: BABYLON.ActionManager.OnPickTrigger
							},
							function () {SquidSpace.fireEvent(eventName, objName, eventData);}
						),
					);
				}
			}
			else {
				// TODO: error or log or something.
			}
		},
		
		fireEvent: function(eventName, sourceObjectName, eventData) {
			if (eventName in eventHandlers) {
				for (hdlr of eventHandlers[eventName]) {
					hdlr(sourceObjectName, eventData);
				}
			}
		},
		
		addEventHandler: function(eventName, handlerFunc) {
			if (!(eventName in eventHandlers)) {
				// Initialize the event name with an empty array.
				eventHandlers[eventName] = [];
			}
			
			// Add the event to the array.
			eventHandlers[eventName].push(handlerFunc);
		},
		
		removeEventHandler: function(eventName, handlerFunc) {
			if (!(eventName in eventHandlers)) {
				// No event handlers! Bail now.
			}
			
			// Find the handler function in the array and remove it.
			let idx = eventHandlers[eventName].indexOf(handlerFunc);
			if (idx >=0) {
				eventHandlers.splice(idx, 1);
			}
		},
		
		//
		// User functions.
		//
		
		/** Returns the current user camera object. */
		getUserCamera: function() {
			return objects["userCamera"];
		},
		
		/** Sets the user mode to the passed mode using the passed options 
			and data. There must be a user mode hook with the mode name. Returns
			false if the user mode is not available, otherwise returns the 
			user mode hook function result.
		*/
		setUserMode: function(modeName, options, data, scene) {
			if (modeName in userModeHooks) {
				return userModeHooks[modeName](options, data, 
					SquidSpace.getUserCamera(), scene);
			}

			// Failed. 
			SquidSpace.logError(`Unknown user mode: ${modeName}.`)
			return false;
		},
		
		//
		// Public scene management functions.
		//
		
		/** PoC-specific function to load the passed scene from the world 
		    and content specs. 
		
			If not provided, userMode defaults to 'default'. 
		*/
		buildWorld: function(worldSpec, contentSpecs, scene) {
			// Assume success.
			let success = true;
		 
		 	/* TODO: Remove and refactor.
			if (debugVerbose) {
				// TODO: Improve debug handling.
				// TODO: Either make this optional or move it to a hook.
				// Log plugin activations.
				BABYLON.SceneLoader.OnPluginActivatedObservable.add(function (plugin) {
				    logDebug(`Plugin Activated: ${plugin.name}`);
				});
			}
			*/
		
			// Turn on optimizaton.
			// TODO: Remove and refactor into SquidCommon as a hook. (New hook?)
			var options = new BABYLON.SceneOptimizerOptions();
			options.addOptimization(new BABYLON.HardwareScalingOptimization(0, 1));
			/* Set Degredation Level - TODO: Come up with a way to make this user settable.
			BABYLON.SceneOptimizerOptions.LowDegradationAllowed()  
			BABYLON.SceneOptimizerOptions.ModerateDegradationAllowed()  
			BABYLON.SceneOptimizerOptions.HighDegradationAllowed() 
			*/
			options.addOptimization(new BABYLON.SceneOptimizerOptions.ModerateDegradationAllowed());
			var optimizer = new BABYLON.SceneOptimizer(scene, options);
			optimizer.targetFrameRate = 40 // TODO: Come up with a way to make this user settable.

		 	/* TODO: Remove and refactor.
			if (debugVerbose) {
				logDebug(`Optimizer target framerate: ${optimizer.targetFrameRate}`)
				optimizer.onSuccessObservable = new function() {
					logDebug("Optimizer 'success'.")
				}
				optimizer.onNewOptimizationAppliedObservable = new function() {
					logDebug("New optimization applied.")
				}
				optimizer.onFailureObservable = new function() {
					logDebug(`Optimizer unable to reach target framerate: ${optimizer.targetFrameRate}`)
				}
			}
			*/
			//optimizer.start(); // Don't need?

		 	/* TODO: Remove and refactor into SquidDebug as a user mode hook.
			if (debugLayer) scene.debugLayer.show();
			*/
			
			// Call prepare hook.
			// TODO: try/catch.
			prepareHook(scene);
			
			/* TODO: Remove this.
			debugCamera = debugVerbose;
			if (debugVerbose) {
				//showWorldAxis(10)
			}
			*/
		 
			// Verify inputs.
			// TODO: Add other validation checks, such as object
			//       member validation.
			if (typeof worldSpec != "object") {
				// World spec is required.
				success = false;
			}
			if ((typeof contentSpecs != "object") && !(contentSpecs instanceof Array)) {
				// Default to empty list.
				contentSpecs = [];
			}
			if (typeof scene != "object") {
				// Scene is required.
				success = false;
			}
		
			// Are we OK to continue?
			if (!success) {
				return success;
			}
			
			// Load resources from specs using a specific order to avoid dependency issues.
			processLoaders(getValIfKeyInDict("mods", worldSpec, {}), modLoaderHooks, 
							scene, "mods");
			for (spec of contentSpecs) {
				processLoaders(getValIfKeyInDict("mods", spec, {}), modLoaderHooks, 
								scene, "mods");
			}
			processLoaders(getValIfKeyInDict("textures", worldSpec, {}), textureLoaderHooks, 
							scene, "textures");
			for (spec of contentSpecs) {
				processLoaders(getValIfKeyInDict("textures", spec, {}), textureLoaderHooks, 
								scene, "textures");
			}
			processLoaders(getValIfKeyInDict("materials", worldSpec, {}), materialLoaderHooks, 
							scene, "materials");
			for (spec of contentSpecs) {
				processLoaders(getValIfKeyInDict("materials", spec, {}), materialLoaderHooks, 
								scene, "materials");
			}
			processLoaders(getValIfKeyInDict("objects", worldSpec, {}), objectLoaderHooks, 
							scene, "objects");
			for (spec of contentSpecs) {
				processLoaders(getValIfKeyInDict("objects", spec, {}), objectLoaderHooks, 
								scene, "objects");
			}
			
			// Process layouts from specs.
			processLayouts(getValIfKeyInDict("layouts", worldSpec, {}), scene);
			for (spec of contentSpecs) {
				processLayouts(getValIfKeyInDict("layouts", spec, {}), scene);
			}

			
		 	/* TODO: Remove and refactor into SquidDebug as a user mode hook.
			// Set gravity for the scene (G force on Y-axis)
			// See https://doc.babylonjs.com/babylon101/cameras,_mesh_collisions_and_gravity
			// TODO: Determine best settings here.
			if (debugVerbose) {
				// TODO: Give this it's own argument instead of debugVerbose.
				// Allow user to fly.
				scene.gravity = new BABYLON.Vector3(0, 0, 0); 
			}
			else {
				// User walks on ground.
				// TODO: Configure from pack file?
				scene.gravity = new BABYLON.Vector3(0, -0.9, 0);
			}
			*/
			// User walks on ground.
			// TODO: Configure from pack file?
			scene.gravity = new BABYLON.Vector3(0, -0.9, 0);

			// Enable Collisions for scene.
			scene.collisionsEnabled = true;
			
			// Call build hook.
			// TODO: try/catch.
			buildHook(scene);

			// Done.
			return success;
		}
	}
}();
