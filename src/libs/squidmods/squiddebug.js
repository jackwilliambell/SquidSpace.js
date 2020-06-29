// NOTE: Strict mode is causing problems I can't track down right now. 
// TODO: Find out why this breaks things and fix.
//'use strict'; 


/** TODO: Document

	SquidSpace.js, the associated tooling, and the documentation are copyright Jack William Bell 2020. 
    All other content, including HTML files and 3D assets, are copyright their respective
    authors.
*/


var SQUIDDEBUG = function() {
	
	var sceneGravity = new BABYLON.Vector3(0, -0.9, 0);
	var axesViewer = undefined;
	
	var label = undefined;
	
	var pluginObserver = function (plugin) {
	    SQUIDSPACE.logDebug(`Plugin Activated: ${plugin.name}`);
	}
	
	var getBUI = function() {
		// NOTE: Requires "babylon.gui.min.js" for support.
		if (BABYLON.GUI) {
			return BABYLON.GUI.AdvancedDynamicTexture.CreateFullscreenUI("UI");
		}
		
		return undefined;
	}
	
	var identifyOnClick = function() {
		let pickResult = scene.pick(scene.pointerX, scene.pointerY);
		if(!pickResult.hit) return;
		
		SQUIDDEBUG.removeLabel();
				
		// Is it a SquidSpace object?
		let nm = SQUIDDEBUG.findSquidSpaceObjectName(pickResult.pickedMesh);
		if (nm) {
			//SQUIDSPACE.logDebug("SQUIDDEBUG.identifyOnClick() name: " + nm)
			SQUIDDEBUG.labelObject(nm);
		}
	}
	
	return {
		
		//
		// Wiring.
		//
		
		wireSquidSpace: function(options, data, squidSpace) {
			// TODO:
		},
		
		//
		// Helper functions.
		//
		
		/** Returns the SquidSpace object name for the passed mesh
		    or undefined if the object could not be found. 
		 */
		findSquidSpaceObjectName(objMesh) {
			return SQUIDSPACE.mapObjects(function(objName, obj) {
				if (obj === objMesh) {
					return objName;
				}
				else if (Array.isArray(obj)) {
					for (mesh of obj) {
						if (mesh === objMesh) {
							return objName;
						}
					}
				}

				return undefined;
			});
		},
		
		/** Places a label on the named SquidSpace.js object and also logs 
		    information about the object. Only one label is allowed at a time, 
		    so labeling a new object removes the label for the previous object. 
		 */
		labelObject: function(objName) {
			SQUIDDEBUG.removeLabel();
			
			obj = SQUIDSPACE.getLoadedObject(objName);
			if (!obj) {
				SQUIDSPACE.logError("SQUIDDEBUG.labelObject() - Unknown object name: " + objName);
			}
			
			SQUIDSPACE.logInfo(SQUIDDEBUG.makeObjectInfoString(obj));
			
			ui = getBUI();
			if (ui) {
				// HACK: Using only the first element of a mesh array.
				// TODO: Come up with a way to include info for all mesh array elements if 
				//       they differ.
				if (Array.isArray(obj)) {
					obj = obj[0];
				}
				
				newlabel = {
					rect: new BABYLON.GUI.Rectangle(),
					nameText: new BABYLON.GUI.TextBlock(),
					posText: new BABYLON.GUI.TextBlock(),
					rotText: new BABYLON.GUI.TextBlock(),
					line: new BABYLON.GUI.Line()
				};

				ui.addControl(newlabel.rect);
				newlabel.rect.background = "#000C";
				newlabel.rect.cornerRadius = "5";
				newlabel.rect.color = "#F00";
				newlabel.rect.width = "400px";
				newlabel.rect.height = "80px";
				newlabel.rect.linkWithMesh(obj);
			    newlabel.rect.linkOffsetY = -250;
			    //newlabel.rect.linkOffsetX = xOff;
				
				newlabel.nameText.text = "Name: " + obj.id;
				newlabel.nameText.textVerticalAlignment = 0;
				newlabel.rect.addControl(newlabel.nameText);

				newlabel.posText.text = "Position: " + obj.position;
				newlabel.posText.textVerticalAlignment = 1;
				newlabel.rect.addControl(newlabel.posText);

				newlabel.rotText.text = "Rotation: " + obj.rotation;
				newlabel.rotText.textVerticalAlignment = 2;
				newlabel.rect.addControl(newlabel.rotText);
				
				ui.addControl(newlabel.line);
		        newlabel.line.lineWidth = 4;
		        newlabel.line.color = "red";
		        newlabel.line.y2 = 40;
		        newlabel.line.linkOffsetY = -12;
		        newlabel.line.linkOffsetX = 0;
		        newlabel.line.linkWithMesh(obj); 
		        newlabel.line.connectedControl = newlabel.rect;  

				label = newlabel;
			}
			else {
				SQUIDSPACE.logError("SQUIDDEBUG.labelObject() - BABYLON.GUI not available, cannot create label.");
			}
		},
		
		/** Removes a label previously added with labelObjectByName() or labelObject().
		 */
		removeLabel: function() {
			if (label) {
				// TODO: Is there something else we need to do to remove the label entirely? Could this
				//       be a memory leak if we don't also remove the text fields?
				ui.removeControl(label.line);
				ui.removeControl(label.rect);
				label = undefined;
			}
		},
		
		/** Returns a formatted string containing information about a Babylon.js object; useful
		    when logging. */
		makeObjectInfoString: function(obj) {
			str = "Not an object.";
			
			if (Array.isArray(obj)) {
				if (obj.length > 0) {
					str = `Mesh Array (${obj.length}): \n`;
					ctr = 0;
					for (o of obj) {
						str = str + ctr++ + " - " + SQUIDDEBUG.makeObjectInfoString(o) + "\n"
					}
				}
				else {
					str = "Empty mesh array.";
				}
			}
			else {
				str = `Mesh (id: ${obj.id}, position: ${obj.position}, size: ${obj.getBoundingInfo().boundingBox.extendSize}, rotation: ${obj.rotation})`;
			}
			
			return str;
		},
		
		/** Returns a formatted string containing information about a Babylon.js object; useful
		    when logging. */
		makeDetailedObjectInfoString: function(obj) {
			str = "Not an object.";
			
			if (Array.isArray(obj)) {
				if (obj.length > 0) {
					str = `Mesh Array (${obj.length}): \n`;
					ctr = 0;
					for (o of obj) {
						str = str + ctr++ + " - " + SQUIDSPACE.makeDetailedObjectInfoString(o) + "\n"
					}
				}
				else {
					str = "Empty mesh array.";
				}
			}
			else {
				str = `Mesh (id: ${obj.id}, name: ${obj.name}, isVisible: ${obj.isVisible}, position: ${obj.position}, absolutePosition: ${obj.absolutePosition}, size: ${obj.getBoundingInfo().boundingBox.extendSize}, world size: ${obj.getBoundingInfo().boundingBox.extendSizeWorld}, ellipsoid: ${obj.ellipsoid}, rotation: ${obj.rotation}, isAnInstance: ${obj.isAnInstance}, scaling: ${obj.scaling})`;
			}
			
			return str;
		},
		
		//
		// Modes.
		//
		
		/** Turns verbose mode on or off. When verbose mode is on there is
		    extra log output from Babylon.js and SquidSpace.js. This extra log output is
		    separate from the logging controlled by SQUIDPSPACE.setLogLevel(), although
		    what log output you actually see is controlled by SQUIDPSPACE.setLogLevel().
		 */
		verboseMode: function(on) {
			// TODO: More.
			if (on) {
				SQUIDSPACE.logInfo("Verbose Mode on.")
				// Log when Babylon.js plugins are activated.
				BABYLON.SceneLoader.OnPluginActivatedObservable.add(pluginObserver);
			} else {
				SQUIDSPACE.logInfo("Verbose Mode off.")
				BABYLON.SceneLoader.OnPluginActivatedObservable.remove(pluginObserver);
			}
		},
		
		/** Turns identify mode on or off. When identify mode is on you can click on an
		    object and a label will appear identifying the object with it's SquidSpace.js
		    name and other information.
		 */
		identifyMode: function(on) {
			// TODO: More.
			if (on) {
				SQUIDSPACE.logInfo("Identify Mode on.")
				window.addEventListener("click", identifyOnClick);
			} else {
				SQUIDSPACE.logInfo("Identify Mode off.")
				window.removeEventListener("click", identifyOnClick);
				SQUIDDEBUG.removeLabel();
			}
		},
		
		/** Turns Babylon.js 'debug layer' on or off. 
		    
			See: https://doc.babylonjs.com/how_to/debug_layer
		 */
		inspectorMode: function(on, scene) {
			if (on) {
				SQUIDSPACE.logInfo("Inspector Mode on.")
				// Show Babylon.js 'debug layer'.
				scene.debugLayer.show();
			} else {
				SQUIDSPACE.logInfo("Inspector Mode off.")
				scene.debugLayer.hide();
			}
		},
		
		/** Turns scene gravity on or off.
		 */
		gravityMode: function(on, scene) {
			if (on) {
				SQUIDSPACE.logInfo("Gravity Mode on.")
				// Set to saved gravity.
				scene.gravity = sceneGravity;
			} else {
				SQUIDSPACE.logInfo("Gravity Mode off.")
				
				// Save current gravity.
				sceneGravity = scene.gravity;
				
				// Turn gravity off.
				scene.gravity = new BABYLON.Vector3(0, 0, 0);
			}
		},
		
		///** Shows or hides the Axes Viewer.
		//
		//    BUG: Doesn't seem to work, BJS fails. Do not use until we find a work-around.
		// */
		//axesViewerMode: function(on, scene) {
		//	if (on) {
		//		axesViewer = BABYLON.Debug.AxesViewer(scene);
		//	} else if (axesViewer != undefined) {
		//		axesViewer.dispose();
		//		axesViewer = undefined;
		//	}
		//},
		
		// TODO: modifyUserCamera function that accepts options and data like
		//       for UserCamera values. Need to refactor UserCamera in SQUIDSPACE
		//       for support.
	}
}();