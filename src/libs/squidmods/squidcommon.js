
var SQUIDCOMMON = function() {
	
	var attachPlacerHooks = function(squidSpace){
		SQUIDSPACE.attachPlacerHook("LightCanPlacer",
			function(areaName, areaOptions, objectName, placeName, options, data, scene) {
				
			squidSpace.logDebug(`LightCanPlacer called! ${areaName}, ${placeName}, ${objName}`);
			
			let meshes = SQUIDSPACE.getLoadedObject(objectName);
	    });
	};
	
	var attachLoaderHooks = function(squidSpace){
		SQUIDSPACE.attachObjectLoaderHook("BasicRoom",
			function(objName, options, data, scene) {
				
				squidSpace.logDebug(`BasicRoom called! ${objName}, ${options}, ${data}`);
				
				// Get options.
				
				// Get data.
				let size = [4, 2.75, 6]; // Very small room
				if (data["size"]) {
					size = data["size"];
				}
				let w = size[0];
				let d = size[2];
				let h = size[1];
				let floorMat = undefined;
				if (data["floor-material"]) {
					floorMat = SQUIDSPACE.getMaterial(data["floor-material"]);
					floorMat.backFaceCulling = false;
				}
				let wallMat = undefined;
				if (data["wall-material"]) {
					wallMat = SQUIDSPACE.getMaterialdata(["wall-material"]);
					wallMat.backFaceCulling = false;
				}
				let ceilingMat = undefined;
				if (data["ceiling-material"]) {
					ceilingMat = SQUIDSPACE.getMaterialdata(["ceiling-material"]);
					ceilingMat.backFaceCulling = false;
				}
				
				// Make floor.
				let floor = SQUIDSPACE.addFloorExp(0, 0, 0, w, d, floorMat, scene)[0]
				
				// Calculate positions.
				let origin = SQUIDSPACE.makePointXYZ(0, 0, 0)
				let longWallOptions = {
					width: d, 
					height: h,
					sideOrientation: BABYLON.Mesh.BACKSIDE
				};
				let leftWallPos = SQUIDSPACE.makePointVector(0, 0 + (h / 2), 0 + (d / 2));
				let leftWallRot = new BABYLON.Vector3(0, Math.PI / 2, 0);
				let rightWallPos = new BABYLON.Vector3(w, 0 + (h / 2),  0 - (d / 2));
				let rightWallRot = new BABYLON.Vector3(0, Math.PI + (Math.PI / 2), 0);
				let shortWallOptions = {
					width: w, 
					height: h,
					sideOrientation: BABYLON.Mesh.BACKSIDE
				};
				let backWallPos = new BABYLON.Vector3(0 + (w / 2), 0 + (h / 2), 0 - d);
				let backWallRot = new BABYLON.Vector3(0, 0, 0);
				let frontWallOptions = {
					width: w, 
					depth: 0.025, 
					height: h * 0.33
				};
				let frontWallPos = new BABYLON.Vector3(0 + (w / 2), 0 + ((h  * 0.33) / 2),  0);
				let frontWallRot = new BABYLON.Vector3(0, 0, 0);
				let ceilingOptions = {
					width: w, 
					height: d,
					sideOrientation: BABYLON.Mesh.DOUBLESIDE
				};
				let ceilingPos = new BABYLON.Vector3(0 + (w / 2), h, 0 - (d / 2));
				let ceilingRot = new BABYLON.Vector3(Math.PI / 2, 0, 0);
				let roomOptions = {
					width: w, 
					depth: d, 
					height: h, 
					sideOrientation: BABYLON.Mesh.BACKSIDE
				}
				let roomPos = new BABYLON.Vector3(origin[0] + (w / 2), origin[1] + (h / 2) - 0.01, origin[2] - (d / 2));
				
				// Build room.
				let leftWall = BABYLON.MeshBuilder.CreatePlane("leftWall", longWallOptions, scene);
				if (wallMat) leftWall.material = wallMat;
				leftWall.position = leftWallPos;
				leftWall.rotation = leftWallRot;
				leftWall.checkCollisions = false;
				leftWall.isVisible = true;
				let rightWall = BABYLON.MeshBuilder.CreatePlane("rightWall", longWallOptions, scene);
				if (wallMat) rightWall.material = wallMat;
				rightWall.position = rightWallPos;
				rightWall.rotation = rightWallRot;
				rightWall.checkCollisions = false;
				rightWall.isVisible = true;
				let backWall = BABYLON.MeshBuilder.CreatePlane("backWall", shortWallOptions, scene);
				if (wallMat) backWall.material = wallMat;
				backWall.position = backWallPos;
				backWall.rotation = backWallRot;
				backWall.checkCollisions = false;
				backWall.isVisible = true;
				let frontWall = BABYLON.MeshBuilder.CreateBox("frontWall", frontWallOptions, scene);
				if (wallMat) frontWall.material = wallMat;
				frontWall.position = frontWallPos;
				frontWall.rotation = frontWallRot;
				frontWall.checkCollisions = false;
				frontWall.isVisible = true;
				let ceiling = BABYLON.MeshBuilder.CreatePlane("ceiling", ceilingOptions, scene);
				if (ceilingMat) ceiling.material = ceilingMat;
				ceiling.position = ceilingPos;
				ceiling.rotation = ceilingRot;
				ceiling.checkCollisions = false;
				ceiling.isVisible = true;
				room = BABYLON.MeshBuilder.CreateBox(objName, roomOptions);
				room.position = roomPos;
				room.checkCollisions = true;
				room.visibility = 0;
				room.isVisible = true;
				room.addChild(leftWall);
				room.addChild(rightWall);
				room.addChild(backWall);
				room.addChild(frontWall);
				room.addChild(ceiling);
				room.addChild(floor);
				
				//*
				let lightFrontFill = new BABYLON.PointLight("pointLight",
												squidSpace.makePointVector(size[0] / 2, 20,  size[0] * 0.66), scene);
				lightFrontFill.diffuse = new BABYLON.Color3(1, 1, 1);
				lightFrontFill.specular = new BABYLON.Color3(0.5, 0.5, 0.5);
				lightFrontFill.range = 90;

				let lightBackFill = new BABYLON.PointLight("pointLight",
												squidSpace.makePointVector(size[0] / 2, 20,  size[0] * 0.33), scene);
				lightBackFill.diffuse = new BABYLON.Color3(1, 1, 1);
				lightBackFill.specular = new BABYLON.Color3(0.5, 0.5, 0.5);
				lightBackFill.range = 90;
				
				//room.addChild(lightFrontFill);
				//room.addChild(lightBackFill);
				//*/
				//scene.createDefaultLight();
		
				// Add room object to SquidSpace.
				SQUIDSPACE.addObjectInstance(objName, [room]);
		
				return [room];

	    });
	};
	
	return {
		wireSquidSpace: function(options, data, squidSpace) {
			//attachPlacerHooks(squidSpace);
			attachLoaderHooks(squidSpace);
		}
	}
}();