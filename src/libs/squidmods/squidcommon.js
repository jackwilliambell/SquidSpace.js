
var SQUIDCOMMON = function() {
	
	var attachPlacerHooks = function(squidSpace){
		SQUIDSPACE.attachPlacerHook("hookname",
			function(areaName, areaOrigin, config, placeName, data, objName, meshes, scene) {
				
				squidSpace.logDebug(`hookname called! ${areaName}, ${areaOrigin}, ${config}, ${placeName}, ${data}`);
			// function body.
	    });
	};
	
	var attachLoaderHooks = function(squidSpace){
		SQUIDSPACE.attachLoaderHook("hookname",
			function(areaName, areaOrigin, config, placeName, data, objName, meshes, scene) {
				
				squidSpace.logDebug(`hookname called! ${areaName}, ${areaOrigin}, ${config}, ${placeName}, ${data}`);
			// function body.
	    });
	};
	
	return {
		wireSquidSpace: function(options, data, squidSpace) {
			//attachPlacerHooks(squidSpace);
			//attachLoaderHooks(squidSpace);
		}
	}
}();