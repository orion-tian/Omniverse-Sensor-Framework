from omni.ui import scene as sc
from omni.ui import color as cl
from pxr import Usd, UsdGeom

from .sensorGestures import Click
from .useful_functions import Func

class ViewportSceneInfo():
    """Render into a Viewport"""
    def __init__(self, viewport_window, ext_id) -> None:
        self.scene_view = None
        self.viewport_window = viewport_window
        self.ext_id = ext_id

        self.stage_listener = None

        # NEW: Create a unique frame for our SceneView
        with self.viewport_window.get_frame(ext_id):
            # Create a default SceneView (it has a default camera-model)
            self.scene_view = sc.SceneView()
            # Register the SceneView with the Viewport to get projection and view updates
            self.viewport_window.viewport_api.add_scene_view(self.scene_view)
    
    def drawSensors(self, primList):
        """draws the UI sensors on top of the sphere prim sensors, 
        the UI has gestures that respond to clicks and makes a window to display that sensor's data"""
        self.scene_view.scene.clear()
        print(Func.getPrimAtPath('/World/Sensor_Results/Sensors').GetAttributes())
        #if Func.getPrimAtPath('/World/Sensor_Results/Sensors').GetAttribute('visibility').Get() == 'inherited':
        with self.viewport_window.get_frame(self.ext_id):
            with self.scene_view.scene:
                for prim in primList:
                    if prim.GetAttribute('visibility').Get() == 'inherited':
                        position = self.get_position_prim(prim)
                        with sc.Transform(transform=sc.Matrix44.get_translation_matrix(*position)):
                            transform = sc.Transform(look_at=sc.Transform.LookAt.CAMERA)
                            with transform:
                                radius = prim.GetAttribute('radius').Get()
                                #sc.Arc(radius+20, axis=2,  color=(0,1,0,1), gesture=[Click(transform, primList[prim])])
                                sc.Arc(radius, axis=2, color=cl.darkGreen, gesture=[Click(transform, primList[prim])])
                                sc.Arc(radius, axis=2,  color=(0,1,0,1), wireframe=True, thickness=20, gesture=[Click(transform, primList[prim])])
    
    def get_position_prim(self, prim):
        """Get position of prim directly from USD"""
        box_cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), includedPurposes=[UsdGeom.Tokens.default_])
        bound = box_cache.ComputeWorldBound(prim)
        range = bound.ComputeAlignedBox()
        bboxMin = range.GetMin()
        bboxMax = range.GetMax()

        x_Pos = (bboxMin[0] + bboxMax[0]) * 0.5
        y_Pos = (bboxMin[1] + bboxMax[1]) * 0.5
        z_Pos = (bboxMin[2] + bboxMax[2]) * 0.5
        position = (x_Pos, y_Pos, z_Pos)
        return position
    
    def __del__(self):
        self.destroy()

    def destroy(self):
        if self.scene_view:
            # Empty the SceneView of any elements it may have
            self.scene_view.scene.clear()
            # un-register the SceneView from Viewport updates
            if self.viewport_window:
                self.viewport_window.viewport_api.remove_scene_view(self.scene_view)
        # Remove our references to these objects
        self.viewport_window = None
        self.scene_view = None