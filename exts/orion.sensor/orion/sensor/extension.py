import omni.ext
import omni.ui as ui
import omni.kit.viewport

from .useful_functions import Func
from .sensors import Sensors
from .viewport_scene_info import ViewportSceneInfo

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    
    #----------------------------------------------------#
    #   Class variables for data, sensor Ids, viewport   #
    #----------------------------------------------------#
    dataList = {"Simulation Data": "simulation_data",
                "Simulation Data 2": "simulation_data_2"}
    sensorList = {'a1': 'a1',
                    'a2':'a2',
                    'a3':'a3',
                    'a4':'a4'}

    def __init__(self) -> None:
            super().__init__()
            self.viewport_scene = None

    def on_startup(self, ext_id):
        print("[orion.sensor] MyExtension startup")
        # Get active viewport, create viewport_scene to draw to, and initialize sensor class
        viewport_window = omni.kit.viewport.utility.get_active_viewport_window() 
        self.viewport_scene = ViewportSceneInfo(viewport_window, ext_id)
        self.sensors = Sensors(self.viewport_scene)

        self._window = ui.Window("Visualize Sensor Data", width=300, height=300)
        with self._window.frame:
            with ui.VStack(): 
                
                # --------------------------------------#
                #   main functions the create sensors   #
                # --------------------------------------#
                def createSensor():
                    print("clicked!")
                    self.sensors.createSensor(Func.getComboValue(sensorIdCombo, MyExtension.sensorList), Func.getSelPaths())
                
                # ----------------#
                #   UI Elements   #
                # ----------------#
                ui.Label("Visualize Sensor Data and Create Legend", 
                        style = {"alignment":ui.Alignment.CENTER, "font_size": 25})

                sensorIdCombo = Func.makeComboAndLabel("Sensor ID", MyExtension.sensorList)
                ui.Button("Create Sensor", clicked_fn=lambda: createSensor(), style = {"font_size": 30})

    def on_shutdown(self):
        # destroy all created objects
        self.sensors.destroy()
        if self.viewport_scene:
            self.viewport_scene.destroy()
            self.viewport_scene = None
        print("[orion.sensor] MyExtension shutdown")
