// NOTE: Strict mode is causing problems I can't track down right now. 
// TODO: Find out why this breaks things and fix.
//'use strict'; 


/** The SquidSpace.js module provides a runtime for a simulated
	scene. It allows you to define a 'world' and will then run
	that world as a simulation using the world's settings and 
	allowing the user to move around it in similar to how they 
	navigate through a real world. 

	In most cases the physics used are simplified, but broadly similar 
	to the real-world. However, some physics parameters may 
	be changed. For example, gravity can be increased or decreased;
	affecting how far you can jump and how fast you move.

	NOTE: SquidSpace.js is intentionally implemented as an old-style Javascript 
	module, despite the fact it uses some newer Javascript functionality. 
	This allows SquidSpace.js to be used from a file system without 
	requiring a server and side-steps CORS exceptions in general.

	## Some ideas for improvement

	Some options reduce CPU, but degrade the experience. One way to handle this might
	be to have a basic setting for 'low', 'medium', and 'high', where high uses every
	option and low uses the least. We could provide a way to choose the setting on the web
	page, which saves the setting to a cookie and reloads the page. The code would simply
	check the cookie on startup and use the appropriate options based on the setting.

	We need to figure out what is required to support tablets and phones and implement that.

	We need to determine if we want to support gamepads.

	SquidSpace.js, the associated tooling, and the documentation are copyright Jack William Bell 2020. 
    All other content, including HTML files and 3D assets, are copyright their respective
    authors.
*/

// Log levels.
const SQS_LOG_ALL = 0;
const SQS_LOG_DEBUG = 0;
const SQS_LOG_INFO = 1;
const SQS_LOG_WARN = 2;
const SQS_LOG_ERROR = 3;
const SQS_LOG_NONE = 9;

// SquidSpace.js core.
var SQUIDSPACE = function() {
	
	//
	// Module data.
	//

	var logLevel = SQS_LOG_ERROR;

	// This is the NW corner of the arena and the origin for layouts. 
	var floorOriginNW = [0, 0, 0]; 
	var floorSize = [0, 0];
	
	var textures = {};
	var materials = {};
	var objects = {};
	var lights = {};
	var contentModules = [];
	
	//
	// Hooks.
	//

	var logHook = function(message){console.log(message);};
	var prepareHook = function(scene){SQUIDSPACE.logInfo("prepareHook()");};
	var buildHook = function(scene){SQUIDSPACE.logInfo("buildHook()");};
	var textureLoaderHooks = {
		"TextureData": function(texName, options, data, scene) {
			return SQUIDSPACE.loadTexture(texName, options, data, scene, null, null, false);
		}
	};
	textureLoaderHooks["default"] = textureLoaderHooks["TextureData"]
	var materialLoaderHooks = {
		"default": function(matName, options, data, scene) {
			//return: material instance or undefined if object could not be loaded
		}
	};
	var objectLoaderHooks = {
		"ObjectData": function(objName, options, data, scene) {
			return SQUIDSPACE.loadObject(objName, options, data, scene, null, null, false);
		},
		"Floor": function(objName, options, data, scene) {
			// TODO: Size should be 3 elements.
			let sz = SQUIDSPACE.getValIfKeyInDict("size", data, [1, 1]);
			let pos = SQUIDSPACE.getValIfKeyInDict("position", data, [0, 0, 0]);
			let mn = SQUIDSPACE.getValIfKeyInDict("material", data, "");
			// TODO: Get material from material list by material name
			//       with a default if not loaded.
			return addFloor(pos[0], pos[1], pos[2], sz[0], sz[1], 
								materials.macadam, scene);
		},
		"UserCamera": function(objName, options, data, scene) {
			// TODO: Size should be 3 elements.
			let pos = SQUIDSPACE.getValIfKeyInDict("position", data, [0, 0, 0]);
			let targetPos = SQUIDSPACE.getValIfKeyInDict("target-position", data, [20, 1.6, 20]);
			return addCamera(pos[0], pos[1], pos[2], 
							targetPos[0], targetPos[1], targetPos[2], scene);
		}
	};
	objectLoaderHooks["default"] = objectLoaderHooks["ObjectData"]
	var modLoaderHooks = {
		"default": function(matName, options, data, scene) {
			//return: object instance or undefined if object could not be loaded
		}
	};
	var objectPlacerHooks = {
		"Single": function(layoutName, layoutOptions, objectName, placeName, options, data, scene) {
			// TODO: Handle layoutOptions as needed. 
			
			// Get values.
			// TODO: 'moreInfoData' is Squid Hall-specific. Use something different.
			let eventData = SQUIDSPACE.getValIfKeyInDict("moreInfoData", options, undefined);
			let mat = SQUIDSPACE.getValIfKeyInDict("material", data, undefined);
			let position = SQUIDSPACE.getValIfKeyInDict("position", data, [0, 0, 0]);
			let rotation = SQUIDSPACE.getValIfKeyInDict("rotation", data, [0, 0, 0]);
			let scale = SQUIDSPACE.getValIfKeyInDict("scale", data, 1);
			let plc = [];
			
			// TODO: Placements currently do not include 'y' and only rotate on y axis.
			SQUIDSPACE.addSingleInstanceToPlacements(placeName, plc, position[0], position[2], rotation[1]);

			if (plc.length > 0) {
				SQUIDSPACE.placeObjectInstances(objectName, plc, mat, eventData, scene, scale);
				return true;
			}
			
			return false;
		},
		"LinearSeries": function(layoutName, layoutOptions, objectName, placeName, options, data, scene) {
			// TODO: Handle layoutOptions as needed. 
			
			// Get values.
			// TODO: 'moreInfoData' is Squid Hall-specific. Use something different.
			let eventData = SQUIDSPACE.getValIfKeyInDict("moreInfoData", data, undefined);
			let mat = SQUIDSPACE.getValIfKeyInDict("material", data, undefined);
			let position = SQUIDSPACE.getValIfKeyInDict("position", data, [0, 0, 0]);
			let rotation = SQUIDSPACE.getValIfKeyInDict("rotation", data, [0, 0, 0]);
			let count = SQUIDSPACE.getValIfKeyInDict("count", data, 1);
			let across = SQUIDSPACE.getValIfKeyInDict("across", data, true);
			let offset = SQUIDSPACE.getValIfKeyInDict("offset", data, 0);
			let plc = [];
			
			// TODO: Placements currently do not include 'y' and only rotate on y axis.
			SQUIDSPACE.addLinearSeriesToPlacements(placeName, plc, count, position[0], position[2], 
				offset, across, rotation[1]);
			
			if (plc.length > 0) {
				SQUIDSPACE.placeObjectInstances(objectName, plc, mat, eventData, scene);
				return true;
			}
			
			return false;
		},
		"RectangleSeries": function(layoutName, layoutOptions, objectName, placeName, options, data, scene) {
			// TODO: Handle layoutOptions as needed. 
			
			// Get values.
			// TODO: 'moreInfoData' is Squid Hall-specific. Use something different.
			let eventData = SQUIDSPACE.getValIfKeyInDict("moreInfoData", data, undefined);
			let mat = SQUIDSPACE.getValIfKeyInDict("material", data, undefined);
			let position = SQUIDSPACE.getValIfKeyInDict("position", data, [0, 0, 0]);
			let countWide = SQUIDSPACE.getValIfKeyInDict("countWide", data, 1);
			let countDeep = SQUIDSPACE.getValIfKeyInDict("countDeep", data, 1);
			let lengthOffset = SQUIDSPACE.getValIfKeyInDict("lengthOffset", data, 0);
			let widthOffset = SQUIDSPACE.getValIfKeyInDict("widthOffset", data, 0);
			let plc = [];
			
			// TODO: Placements currently do not include 'y' and only rotate on y axis.
			SQUIDSPACE.addRectangleSeriesToPlacements(placeName, plc, countWide, countDeep, 
				position[0], position[2], lengthOffset, widthOffset);
			
			if (plc.length > 0) {
				SQUIDSPACE.placeObjectInstances(objectName, plc, mat, eventData, scene);
				return true;
			}
		
			return false;
		}
	};
	objectPlacerHooks["default"] = objectPlacerHooks["Single"]
	
	//
	// Events.
	//
	
	var eventHandlers = {};
	
	//
	// Spec processing functions.
	//
	// TODO: Wiring and events. 
	//
	
	var processLoaders = function(loaderSpecs, loaderHooks, scene, loaderTypeName, overWrite=false) {
		// TODO: Modify so 'overWrite' disallows replacing an existing resource.
		
		// Process all the objects. This does not define processing order, so if we 
		// run into use cases where there are inter-object depedencies we'll need to
		// control order as well.
		for (key in loaderSpecs) {			
			// Get working values.
			let options = SQUIDSPACE.getValIfKeyInDict("options", loaderSpecs[key], {});
			let data = SQUIDSPACE.getValIfKeyInDict("data", loaderSpecs[key], undefined);
			let loaderName = SQUIDSPACE.getValIfKeyInDict("loader", options, "default");
			let loader = SQUIDSPACE.getValIfKeyInDict(loaderName, loaderHooks, undefined);
			
			SQUIDSPACE.logDebug(`processLoaders(): ${loaderTypeName} / ${key} spec / ${loaderName} loader.`);
			
			// Do we have a loader?
			if (typeof loader === "function") {
				// Load it!
				// TODO: Try/Catch and error handling.
				let result = undefined;
				try {
					result = loader(key, options, data, scene);
				} catch(e) {
					SQUIDSPACE.logError(`processLoaders(): loader ${loaderName} failed with error ${e}.`)
				}
			
				// Do we have a result?
				if (result != undefined) {
					// Append the options.
					// TODO: Consider better ways to do this and if we want to. (Right now
					//       just wastes memory without a solid use case)
					//result.options = options;
					
					// Save the object for later.
					SQUIDSPACE.addObjectInstance(key, result);
				}
			}
			else {
				SQUIDSPACE.logError(`processLoaders(): No ${loaderTypeName} loader hook named '${loaderName}'.`);
			}
		}
	}
	
	var processLayouts = function(layoutsSpecs, scene, overWrite=false) {
		// TODO: Modify so 'overWrite' disallows replacing an existing object.
		
		// Process all the layouts. This does not define processing order, so if we 
		// run into use cases where there are inter-layout depedencies we'll need to
		// control order as well.
		for (layoutName in layoutsSpecs) {
			SQUIDSPACE.logDebug(`processLayouts(): ${layoutName} layout.`);

			// Get working values.
			let layoutOptions = SQUIDSPACE.getValIfKeyInDict("options", layoutsSpecs[layoutName], {});
			let objPlacements = SQUIDSPACE.getValIfKeyInDict("objectPlacements", layoutsSpecs[layoutName], []);

			// TODO: Handle area layout options. (Currently ignoring them.) Things to do:
			// 1. Save area and provide a get function
			// 2. Rework options adding default values if needed
			// 3. Come up with more options

			// Process the object placements.
			for (placement of objPlacements) {
				// Get working values.
				let objectName = SQUIDSPACE.getValIfKeyInDict("object", placement, undefined);
				let placers = SQUIDSPACE.getValIfKeyInDict("data", placement, []);

				// Do we have an object name?
				if (typeof objectName === "string") {
					SQUIDSPACE.logDebug(`processLayouts(): ${layoutName} layout / ${objectName} object.`);

					// Process the placers.
					for (placer of placers) {
						// Get working values.
						let options = SQUIDSPACE.getValIfKeyInDict("options", placer, {});
						let data = SQUIDSPACE.getValIfKeyInDict("data", placer, {});
						let placeName = SQUIDSPACE.getValIfKeyInDict("place-name", placer, undefined);
						let placerName = SQUIDSPACE.getValIfKeyInDict("placer", options, "default");
						let placerFunc = SQUIDSPACE.getValIfKeyInDict(placerName, objectPlacerHooks, undefined);

						// do we have a place name?
						if (typeof placeName === "string") {
							// Namespace place name with the layout name.
							placeName = layoutName + '.' + placeName;
							
							SQUIDSPACE.logDebug(
								`processLayouts(): ${layoutName} layout / ${objectName} object / ${placeName} place / ${placerName} placer.`);
							// Do we have a placer?
							if (typeof placerFunc === "function") {
								// Place it!
								let result = undefined;
								try {
									result = placerFunc(layoutName, layoutOptions, objectName, placeName,
																		options, data, scene);
								} catch(e) {
									SQUIDSPACE.logError(`processLayouts(): Placer Hook function ${placerName}  for ${placeName} of ${objectName} in ${layoutName} failed with error ${e}.`)
								}
							} else {
								SQUIDSPACE.logError(
									`processLayouts(): No placer hook named '${placerName}'.`);
							}
						} else {
							SQUIDSPACE.logError(
								`processLayouts(): Placement without a valid place name for ${objectName} in ${layoutName}.`);
						}
					}
				} else {
					SQUIDSPACE.logError(
						`processLayouts(): Placement without a valid object name in ${layoutName}.`);
				}
			}
		}
	}
	
	// TODO: Process events.
	
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
		let floor = BABYLON.Mesh.CreateGround('_floor_', w, d, 2, scene);
		floor.position = new BABYLON.Vector3(x, y, z);
	    floor.material = material;
	    //floor.receiveShadows = true; // This seems to increase the CPU requirements by quite a bit.
		floor.checkCollisions = true;

		return [floor];
	}
	
	var addCamera = function(x, y, z, targetX, targetY, targetZ, scene) {
		//SQUIDSPACE.logDebug(`addCamera() - Pos: [${x}, ${y}, ${z}] Target: [${targetX}, ${targetY}, ${targetZ}]`);

		// Add a camera to the scene and attach it to the canvas
		// TODO: Specify camera in world file.
		// TODO: Support switching to VirtualJoysticksCamera if running on a tablet or phone.
		// See https://doc.babylonjs.com/babylon101/cameras#virtual-joysticks-camera
		// HACK: The 'y + 0.4' forces the starting position to be correct so the camera 
		//       does not 'bob up' when you start to move. 
		// TODO: Calculate height instead of using a constant.
		let camera = new BABYLON.UniversalCamera("usercamera", SQUIDSPACE.makePointVector(x, y, z), scene);
		//var camera = new BABYLON.FreeCamera("default camera", new BABYLON.Vector3(0, 5, -10), scene);
		//var camera = new BABYLON.FlyCamera("default camera", new BABYLON.Vector3(0, 5, -10), scene);
		camera.setTarget(new SQUIDSPACE.makePointVector(targetX, targetY, targetZ));
		camera.attachControl(canvas, true);

		//SQUIDSPACE.logDebug(`addCamera() - floorOriginNW: ${floorOriginNW}`);
		//SQUIDSPACE.logDebug(`addCamera() - Camera Pos: ${camera.position}`);

		//
		// Enable walking.
		// TODO: Specify the options in world file, add support code to squidspace.js
		//

		// Set the ellipsoid around the camera for collision detection.
		// TODO: Make this settable from the world module file.
		// TODO: Experiment with values to find best.
		// TODO: Consider making pack file settable.
		// NOTE: ellipsoid values must be carefully chosen to reduce image tearing when
		//       up close to objects, while still allowing you to navigate around without
		//       getting stuck between things. However, this does mean you can't get really
		//       close to anything straight in front of you.
		//camera.ellipsoid = new BABYLON.Vector3(0.85, 0.8, 0.85);
		camera.ellipsoid = new BABYLON.Vector3(1, 0.8, 1);
		
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

		// Other camera settings.
		// TODO: Make these settable from the world module file.
		// TODO: Experiment with values to find best.
		// TODO: Consider making pack file settable or even dynamically settable.
		camera.fov = 1.3;
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
		
		return [camera];
	}
		
	//
	// Layout Builtins.
	//
	
	// TODO: Implement.

	return {
		//
		// Hacks.
		//
		
		// Expose addFloor().
		addFloorExp: function (x, y, z, w, d, material, scene) {
			return addFloor(x, y, z, w, d, material, scene);
		},
		
		
		//
		// Public helper functions.
		//
		
		/** Returns the value for the key in the dict, unless the dict 
		    is not a dictionary or the key does not exist; in which case
		    it returns the default value.
		 */
		getValIfKeyInDict: function(key, dict, defaultVal) {
			if ((dict != undefined) && (typeof dict === "object") && 
				(key in dict) && dict.hasOwnProperty(key)) {
				return dict[key];
			}
		
			return defaultVal;
		},
		
		/** Returns the size of the bounding box for an object as a Vector3. If 
		    the object is an array of meshes, returns the largest x, y, and z for
		    all meshes.
		*/
		getObjectSize: function(obj) {
			size = BABYLON.Vector3(0,0,0);
			
			if (Array.isArray(obj)) {
				if (obj.length > 0) {
					for (o of obj) {
						osz = SQUIDSPACE.getObjectSize(o);
						if (osz.x > size.x) size.x = osz.x;
						if (osz.y > size.y) size.y = osz.y;
						if (osz.z > size.z) size.z = osz.z;
					}
				}
				else {
					str = "Empty mesh array.";
				}
			}
			else {
				size = obj.getBoundingInfo().boundingBox.extendSize;
			}
			
			return size;
		},
		
		
		/** Returns an array of points in the form [x, y, z], where the points are 
		    calculated from the passed points using the following rules:

			1. x and z are normalized from the floor origin point, located in the 
		       NW corner of the floor
		
			TODO: Add origin argument, which if undefined defaults to floor origin.
		 */
		makePointXYZ: function(x, y, z) {
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

		loadTexture: function(texName, options, data, scene, onSuccessFunc, onFailFunc, doNotAdd) {		
			let url = "";
			if (typeof data === "string") {
				// TODO: Not currently handling data as BASE64 encoded. This is not supported.
				SQUIDSPACE.logError(`Not currently loading Texture ${texName} data as BASE64 encoded.`);
				return undefined;
				//sceneFilename = "data:" + data;
			}
			else if ((typeof data === "object") && ("url" in data)) {
				url = data["url"];
			}
			else if ((typeof data === "object") && ("dir" in data) && ("file-name" in data)) {
				url = data["dir"] + data["file-name"];
			}
			else {
				SQUIDSPACE.logWarn(`Invalid data values for ${texName}. Data ${data}`);
				return undefined;
			}
			
			/* TODO: The callback functions don't seem to work.
			let tx = new BABYLON.Texture(url, scene, false, false, null, 
					function(newTexture) {
						// Save the texture for later?
						if (!doNotAdd) SQUIDSPACE.addTextureInstance(texName, newTexture);
						
						// Is there a success function?
						if (typeof onSuccessFunc == "function") onSuccessFunc(newTexture);
					},
					function(scene, message, exception) {
						SQUIDSPACE.logError("== '" + objName + 
							"' texture import failed. ==\n  Message: " + 
							message.substring(0, 64) + " ... " +  message.substring(message.length - 64) +
							"\n  Exception: " + exception);
							
							// Is there a fail function?
							if (typeof onFailFunc == "function") onFailFunc(scene, message, exception);
					});
			*/
			// HACK: doing this because callback doesn't work.
			let tx = new BABYLON.Texture(url, scene);
			if (tx) {
				// Save the texture for later?
				if (!doNotAdd) SQUIDSPACE.addTextureInstance(texName, tx);
				
				// Is there a success function?
				if (typeof onSuccessFunc == "function") onSuccessFunc(tx);
			}
		},
		
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
			the internal list, making it available to the getLoadedObject() function. 
			Returns the loaded object or 'undefined'. 
		
		    The options and data values are the same as used for pack file options with the 
			'default' loader. 
		*/
		loadObject: function(objName, options, data, scene, onSuccessFunc, onFailFunc, doNotAdd) {
			let obj = undefined;
			let matName = SQUIDSPACE.getValIfKeyInDict("material", options, undefined);
			let visible = SQUIDSPACE.getValIfKeyInDict("visible", options, false);
			let collisionDetect = SQUIDSPACE.getValIfKeyInDict("collision-detection", options, true);
			// For meshNameFilter, empty string means import *all* meshes in the object.
			let meshNameFilter = SQUIDSPACE.getValIfKeyInDict("mesh-name-filter", options, ""); 
			let loaderPluginExtension = SQUIDSPACE.getValIfKeyInDict("loader-plugin", options, null);
			
			let rootUrl = "";
			let sceneFilename = "";
			if (typeof data === "string") {
				sceneFilename = "data:" + data;
			}
			else if ((typeof data === "object") && ("url" in data)) {
				rootUrl = data["url"];
			}
			else if ((typeof data === "object") && ("dir" in data) && ("file-name" in data)) {
				rootUrl = data["dir"];
				sceneFilename = data["file-name"];
			}
			else {
				SQUIDSPACE.logWarn(`Invalid data values for ${objName}. Data ${data}`);
				return undefined;
			}
			
			// HACK! This uses one material and applies it to all meshes of the object. 
			// TODO: Do materials right.
			material = undefined;
			if (matName) {
				material = SQUIDSPACE.getMaterial(matName);
			}
			
			BABYLON.SceneLoader.ImportMesh(meshNameFilter, rootUrl, sceneFilename, scene, 
					function(newMeshes) {
						// Process each mesh based on the options.
						for (mesh of newMeshes) {
							mesh.isVisible = visible;
							mesh.checkCollisions = collisionDetect;
							if (material) mesh.material = material;
						}
						
						// Save the meshes for later?
						if (!doNotAdd) SQUIDSPACE.addObjectInstance(objName, newMeshes);
						
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
						SQUIDSPACE.logError("== '" + objName + 
							"' mesh import failed. ==\n  Message: " + 
							message.substring(0, 64) + " ... " +  message.substring(message.length - 64) +
							"\n  Exception: " + exception);
							
							// Is there a fail function?
							if (typeof onFailFunc == "function") onFailFunc(scene, message, exception);
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
			let meshes = SQUIDSPACE.getLoadedObject(objName);
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
				SQUIDSPACE.addObjectInstance(cloneObjName, clone);
				
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
		getLoadedObject: function(objName) {
			if (objName in objects) {
				return objects[objName];
			}
			
			return undefined;
		},
		
		/** Returns an array of currently loaded object names. 
		 */
		getLoadedObjectNames: function() {
			return Object.keys(objects);
		},
		
		/** Calls the passed map function on every loaded object until the map function 
		    returns something other than 'undefined', at which point it stops processing
		    and returns the map function response. Returns undefined if the map function 
		    processes every object without returning something other than undefined. 
		
			Function signature: mapFunc(objName, obj)
		 */
		mapObjects: function(mapFunc) {
			for (var objName in objects) {
			    if (objects.hasOwnProperty(objName)) {           
			        let result = mapFunc(objName, objects[objName]);
					if (result != undefined) return result;
			    }
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
				placements.push([seriesName + '-' + i, x, z, rotation])
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
				SQUIDSPACE.addLinearSeriesToPlacements(seriesName + "-top-", placements, 
													countWide, wx, z, lengthOffset, true, 0);
				SQUIDSPACE.addLinearSeriesToPlacements(seriesName + "-bottom-", placements, 
													countWide, wx, bz, lengthOffset, true, 0);
			}

			// Do depth placements.
			for (let i = r;i< countDeep;i++) {
				SQUIDSPACE.addLinearSeriesToPlacements(seriesName + "-left-", placements, 
								countDeep, x - lengthOffset, z + lengthOffset, lengthOffset, false, Math.PI / 2);
				SQUIDSPACE.addLinearSeriesToPlacements(seriesName + "-right-", placements, 
								countDeep, rx, z + lengthOffset, lengthOffset, false, Math.PI / 2);
			}
		},

		/** Places instances of the object referred to by object name (string) using 
		    the passed material name (string, null or undefined), using the locations and 
		    rotations specified in the passed placements array.
		
			TODO: Material not currently supported. Consider removing it, since it isn't
		          clear which mesh would get the material. (All meshes in object?)
		 */
		placeObjectInstances: function(objName, placements, matName, eventData, scene, scale) {
			// Get the meshes.
			let meshes = SQUIDSPACE.getLoadedObject(objName);
			if ((typeof meshes != "object") || !(meshes instanceof Array) || (meshes.length < 1))
				 throw `Mesh not loaded for object reference: ''${objName}''.`;
			
			//if (!scale) scale = 1;
		
			for (instance of placements) {
				let newMeshes = [];
				for (mesh of meshes) {
					let m = undefined;
					if (eventData) {
						// Create a clone and add it to the new meshes.
						m = mesh.clone(instance[0]);
						newMeshes.push(m);
					}
					else {
						// Create an instance and add it to the new meshes.
						m = mesh.createInstance(instance[0]);
						newMeshes.push(m);
					}
					
					// Set placement values.
					m.position = SQUIDSPACE.makeLayoutVector(
										instance[1], 0.01, instance[2], m.scaling.x, m.scaling.y);
					if (placements[3] != 0) {
						// NOTE: rotate() appears to permanently change mesh rotation, so the
						//       rotation property shows no rotation afterwards.
						//m.rotate(BABYLON.Axis.Y, instance[3]);
						// TODO: Support other than 'y' axis rotation.
						m.rotation = new BABYLON.Vector3(0, instance[3], 0);
						//m.position.z -= (width / 2);
					}
					
					// Set other values.
					//m.scaling = new BABYLON.Vector3(scale, scale, scale);
					// TODO: Do we want to add these to placement somehow?
					m.checkCollisions = true;
					m.visible = true;
					// TODO: Fix this. IMPORTANT!
					//let bv = m.getBoundingInfo().boundingBox.minimum;
				}
				SQUIDSPACE.addObjectInstance(instance[0], newMeshes);	
				
				// Add event?
		    	if (eventData) {
					SQUIDSPACE.attachClickEventToObject(key, "onClickShowPopup", eventData, scene);
		    	}		
			}
		},

		//
		// Logging.
		//
		
		/** Sets the current log level to the passed level, if valid. */
		setLogLevel: function(logLvl) {
			// Is it a valid log level?
			if ([SQS_LOG_DEBUG, SQS_LOG_INFO, SQS_LOG_WARN, SQS_LOG_ERROR].includes(logLvl)) {
				// Set the log level.
				logLevel = logLvl;
				SQUIDSPACE.logInfo(`setLogLevel(): Setting log level to ${logLevel}.`);
			}
			else {
				SQUIDSPACE.logInfo(`setLogLevel(): Invalid log level: ${logLevel} - could not set.`);
			}
		},
		
		/** Logs a debug-level message. */
		logDebug: function(message) {
			if (logLevel <= SQS_LOG_DEBUG) {
				logHook("[DEBUG] " + message);
			}
		},
		
		/** Logs an info-level message. */
		logInfo: function(message) {
			if (logLevel <= SQS_LOG_INFO) {
				logHook("[INFO] " + message);
			}
		},
		
		/** Logs a warning-level message. */
		logWarn: function(message) {
			if (logLevel <= SQS_LOG_WARN) {
				logHook("[WARNING] " + message);
			}
		},
		
		/** Logs an error-level message. */
		logError: function(message) {
			if (logLevel <= SQS_LOG_ERROR) {
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
	
		    Signature: hookFunction(layoutName, layoutOptions, objectName, placeName, 
		                            options, data, scene) {return: boolean}
		 */
		attachObjectPlacerHook: function(hookName, hookFunction) {
			let oldHook = objectPlacerHooks[hookName];
			objectPlacerHooks[hookName] = hookFunction;
			return oldHook;
		},
		
		//
		// Events.
		//

		// Refactor to a named hook function and make this default.
		attachClickEventToObject: function(objName, eventName, eventData, scene) {
			meshes = SQUIDSPACE.getLoadedObject(objName);
			
			if (typeof meshes != "undefined") {
				for (mesh of meshes) {
					try {
						mesh.actionManager = new BABYLON.ActionManager(scene);
						mesh.actionManager.registerAction(
							new BABYLON.ExecuteCodeAction({
									trigger: BABYLON.ActionManager.OnPickTrigger
								},
								function () {SQUIDSPACE.fireEvent(eventName, objName, eventData);}
							),
						);
					} catch(e) {
						SQUIDSPACE.logError(`attachClickEventToObject(): Attaching click event to ${objName} failed with error ${e}.`)
					}
				}
			}
			else {
				SQUIDSPACE.logWarn(`attachClickEventToObject(): ${objName} not found.`)
			}
		},
		
		fireEvent: function(eventName, sourceObjectName, eventData) {
			if (eventName in eventHandlers) {
				for (hdlr of eventHandlers[eventName]) {
					hdlr(sourceObjectName, eventData);
				}
			}
		},
		
		addEventListener: function(eventName, handlerFunc) {
			if (!(eventName in eventHandlers)) {
				// Initialize the event name with an empty array.
				eventHandlers[eventName] = [];
			}
			
			// Add the event to the array.
			eventHandlers[eventName].push(handlerFunc);
		},
		
		removeEventListener: function(eventName, handlerFunc) {
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
		// Public scene management functions.
		//
		
		/** Loads a single content module. 
		 */
		loadContentModule: function(contentModule, scene, overWrite=false) {
			// Load resources from spec using a specific order to avoid dependency issues.
			processLoaders(SQUIDSPACE.getValIfKeyInDict("mods", contentModule, {}), modLoaderHooks, 
							scene, "mods", overWrite)
			processLoaders(SQUIDSPACE.getValIfKeyInDict("textures", contentModule, {}), textureLoaderHooks, 
							scene, "textures", overWrite)
			processLoaders(SQUIDSPACE.getValIfKeyInDict("materials", contentModule, {}), materialLoaderHooks, 
							scene, "materials", overWrite)
			processLoaders(SQUIDSPACE.getValIfKeyInDict("objects", contentModule, {}), objectLoaderHooks, 
							scene, "objects", overWrite)
			
			// Do layouts.
			processLayouts(SQUIDSPACE.getValIfKeyInDict("layouts", contentModule, {}), scene, overWrite);
			
			// TODO: Attach events.
		},
		
		/** Adds a content module to the 'autoload' list. These are loaded after the world module
		    and the preload modules. The order they are loaded is undefined.
		 */
		addAutoloadModule: function(contentModule) {
			contentModules.push(contentModule);
		},
		
		/** PoC-specific function to load the passed scene from the world 
		    and content specs. 
         */
		buildWorld: function(worldModule, preloadContentModuleModules, scene, overWrite=false) {
			// Assume success.
			let success = true;
					 
			// Verify inputs.
			// TODO: Add other validation checks, such as object
			//       member validation.
			if (typeof worldModule != "object") {
				SQUIDSPACE.logWarn("buildWorld(): No valid world module supplied.")
				success = false;
			}
			if ((typeof preloadContentModuleModules != "object") && !(preloadContentModuleModules instanceof Array)) {
				// Default to empty list.
				preloadContentModuleModules = [];
			}
			if (typeof scene != "object") {
				SQUIDSPACE.logWarn("buildWorld(): No valid scene supplied.")
				success = false;
			}
	
			// Are we OK to continue?
			if (!success) {
				SQUIDSPACE.logError("buildWorld(): Failed.")
				return success;
			}
		 					
			// Call prepare hook.
			try {
				prepareHook(scene);
			} catch(e) {
				SQUIDSPACE.logError(`buildWorld(): Prepare Hook Function failed with error ${e}.`)
			}
			
			// Load all the content. We start by loading the world.
			SQUIDSPACE.loadContentModule(worldModule, scene, overWrite);
			
			// Then we load the preload modules.
			for (module of preloadContentModuleModules) {
				SQUIDSPACE.loadContentModule(module, scene, overWrite);
			}
			
			// Finally we load the autoload modules.
			for (module of contentModules) {
				SQUIDSPACE.loadContentModule(module, scene, overWrite);
			}
			
			// Call build hook.
			try {
				buildHook(scene);
			} catch(e) {
				SQUIDSPACE.logError(`buildWorld(): Build Hook Function failed with error ${e}.`)
			}
		
			// NOTE: We want to turn on collisions using worker threads instead of main thread. However,
			//       it isn't clear if we still need the code below because BJS may now do it automatically. 
			//       Also, there may be issues with some browsers that don't properly support worker threads.
			// MORE: https://blog.raananweber.com/2015/06/06/collisions-using-workers-for-babylonjs-part-2/
			scene.workerCollisions = true; 	
						
			// Turn on optimizaton.
			//*
			// TODO: Consider if we want to refactor this into SquidCommon as a hook. (New hook?)
			var options = new BABYLON.SceneOptimizerOptions();
			options.addOptimization(new BABYLON.HardwareScalingOptimization(0, 1));
			
			// Set Degredation Level - TODO: Come up with a way to make this user settable.
			//BABYLON.SceneOptimizerOptions.LowDegradationAllowed()  
			//BABYLON.SceneOptimizerOptions.ModerateDegradationAllowed()  
			//BABYLON.SceneOptimizerOptions.HighDegradationAllowed() 
			
			options.addOptimization(new BABYLON.SceneOptimizerOptions.ModerateDegradationAllowed());
			var optimizer = new BABYLON.SceneOptimizer(scene, options);
			optimizer.targetFrameRate = 40 // TODO: Come up with a way to make this user settable.
			SQUIDSPACE.logDebug(`Optimizer target framerate: ${optimizer.targetFrameRate}`)
			optimizer.onSuccessObservable = new function() {
				SQUIDSPACE.logDebug("Optimizer 'success'.")
			}
			optimizer.onNewOptimizationAppliedObservable = new function() {
				SQUIDSPACE.logDebug("New optimization applied.")
			}
			optimizer.onFailureObservable = new function() {
				SQUIDSPACE.logDebug(`Optimizer unable to reach target framerate: ${optimizer.targetFrameRate}`)
			}
			optimizer.start(); // Don't need?
			//*/

			// Done.
			return success;
		}
	}
}();
