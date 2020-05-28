
var SquidCommon = function() {
	
	var attachPlacerHooks = function(squidSpace){
		squidSpace.attachPlacerHook("hookname",
			function(areaName, areaOrigin, config, placeName, data, objName, meshes, scene) {
				
				squidSpace.logDebug(`hookname called! ${areaName}, ${areaOrigin}, ${config}, ${placeName}, ${data}`);
			// function body.
	    });
	};
	
	var attachPlacerHooks = function(squidSpace){
		squidSpace.attachPlacerHook("hookname",
			function(areaName, areaOrigin, config, placeName, data, objName, meshes, scene) {
				
				squidSpace.logDebug(`hookname called! ${areaName}, ${areaOrigin}, ${config}, ${placeName}, ${data}`);
			// function body.
	    });
	};
	
	return {
		wireSquidSpace: function(options, data, squidSpace) {
			// TODO:
		}
	}
}();