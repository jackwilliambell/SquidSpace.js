

var SQUIDDEBUG = function() {
	
	var sceneGravity = new BABYLON.Vector3(0, -0.9, 0);
	var axesViewer = undefined;
	
	var pluginObserver = function (plugin) {
	    SQUIDSPACE.logDebug(`Plugin Activated: ${plugin.name}`);
	}
	
	return {
		wireSquidSpace: function(options, data, squidSpace) {
			// TODO:
		},
		
		/** Turns verbose mode on or off. When verbose mode is on extra there is
		    extra log output from Babylon.js and SquidSpace.js. This extra log output is
		    separate from the logging controlled by SQUIDPSPACE.setLogLevel(), although
		    what log output you actually see is controlled by SQUIDPSPACE.setLogLevel().
		 */
		verboseMode: function(on) {
			// TODO: More.
			if (on) {
				// Log when Babylon.js plugins are activated.
				BABYLON.SceneLoader.OnPluginActivatedObservable.add(pluginObserver);
			} else {
				BABYLON.SceneLoader.OnPluginActivatedObservable.remove(pluginObserver);
			}
		},
		
		/** Turns Babylon.js 'debug layer' on or off. 
		    
			See: https://doc.babylonjs.com/how_to/debug_layer
		 */
		inspectorMode: function(on, scene) {
			if (on) {
				// Show Babylon.js 'debug layer'.
				scene.debugLayer.show();
			} else {
				scene.debugLayer.hide();
			}
		},
		
		/** Turns scene gravity on or off.
		 */
		gravityMode: function(on, scene) {
			if (on) {
				// Set to saved gravity.
				scene.gravity = sceneGravity;
			} else {
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