import omni.ext
import omni.kit.commands
from pxr import Usd, Tf

from .useful_functions import Func

class Sensors:
    """class to create sensors and react to changes to the sesnros"""

    def __init__(self, viewport_scene):
        """create xForms for sensors and initiazlize needed variables"""
        Func.defineXform('/World/Sensor_Results')
        sensorsFold = Func.defineXform('/World/Sensor_Results/Sensors')
        self.sensorsFold = sensorsFold
        self.radius = 25
        self.viewport_scene = viewport_scene
        self.usd_context = omni.usd.get_context()
        self.sensorPrims = {}

        # variables to track stage events
        self.stage_listener = None
        self.events = self.usd_context.get_stage_event_stream()
        self.stage_event_delegate = self.events.create_subscription_to_pop(self.on_stage_event, name="Stage Event")

    def createSensor(self, sensorID, sel_paths):
        """Creates a sphere to act as the sensor and places it at the center of bounding box of the first selected prim, 
        also calls drawSensor to draw the UI element on top of the sphere"""
        # create sphere and set its radius as self.radius
        omni.kit.commands.execute('CreatePrim',
                                prim_type='Sphere', 
                                prim_path = Func.getPath(self.sensorsFold) + '/' + sensorID + 'Sensor')
        sphere_prim = Func.getPrimAtPath(Func.getPath(self.sensorsFold) + '/' + sensorID + 'Sensor')
        sphere_prim.GetAttribute('radius').Set(self.radius)
        # move sphere to center of bounding box of the first selected prim
        sel_prim = Func.getPrimAtPath(sel_paths[0])
        sphere_prim.GetAttribute('xformOp:translate').Set(self.viewport_scene.get_position_prim(sel_prim))
        # keep track of which sensors are already created and drawSensors
        self.sensorPrims.update({sphere_prim: sensorID})
        self.viewport_scene.drawSensors(self.sensorPrims)
    
    def on_stage_event(self, event):
        """Create a listener to call notice_changed"""
        stage = self.usd_context.get_stage()
        self.stage_listener = Tf.Notice.Register(Usd.Notice.ObjectsChanged, self.notice_changed, stage)
    
    def notice_changed(self, notice: Usd.Notice, stage: Usd.Stage) -> None:
        """Called by Tf.Notice. Calls drawSensor when a sensor prim changes in any way so that 
        the ui element follows the sphere prim if it moves"""
        for p in notice.GetChangedInfoOnlyPaths():
            for prim in self.sensorPrims:
                if Func.getPath(prim) in str(p.GetPrimPath()):
                    self.viewport_scene.drawSensors(self.sensorPrims)
    
    def destroy(self):
        """stop tracking stage events"""
        self.events = None
        self.stage_event_delegate.unsubscribe()