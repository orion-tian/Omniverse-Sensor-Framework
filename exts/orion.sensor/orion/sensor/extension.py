import omni.ext
import omni.ui as ui
from pxr import Gf, Sdf
from omni.ui import scene as sc
import omni.kit.viewport

from .viewport_overlay_legend import LegendOverlay
from .useful_functions import Func
from .sensors import Sensors

from .viewport_scene_info import ViewportSceneInfo

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    
    #---------------------------------------------------#
    # Class variables for data, legend colors, viewport #
    #---------------------------------------------------#
    dataList = {"Simulation Data": "simulation_data",
                "Simulation Data 2": "simulation_data_2"}
    legendColors = [Gf.Vec3f(0.0, 0.0, 1),  
                    Gf.Vec3f(0.0, 0.5, 1), 
                    Gf.Vec3f(0, 1, 1), 
                    Gf.Vec3f(0, 1, 0.5),
                    Gf.Vec3f(0, 1, 0), 
                    Gf.Vec3f(0.5, 1, 0), 
                    Gf.Vec3f(1, 1, 0), 
                    Gf.Vec3f(1, 0.5, 0), 
                    Gf.Vec3f(1, 0, 0)]
    legendColors2 = [Gf.Vec3f(0.0, 0.0, 1), 
                    Gf.Vec3f(0.0, 0.5, 1), 
                    Gf.Vec3f(0.3, 0.5, 1), 
                    Gf.Vec3f(0.7, 0.7, 0.2),
                    Gf.Vec3f(1, 1, 0), 
                    Gf.Vec3f(1, 0.7, 0), 
                    Gf.Vec3f(1, 0.3, 0), 
                    Gf.Vec3f(1, 0.15, 0.2), 
                    Gf.Vec3f(1, 0, 0)]
    legendColorsBlueYellow = [Gf.Vec3f(0.0, 51.0/255, 150.0/255), 
                            Gf.Vec3f(23.0/255, 80.0/255, 172.0/255), 
                            Gf.Vec3f(51.0/255, 115.0/255, 196.0/255), 
                            Gf.Vec3f(84.0/255, 148.0/255, 218.0/255),
                            Gf.Vec3f(115.0/255, 185.0/255, 238.0/255), 
                            Gf.Vec3f(134.0/255, 206.0/255, 250.0/255), 
                            Gf.Vec3f(165.0/255, 145.0/255, 61.0/255), 
                            Gf.Vec3f(176.0/255, 155.0/255, 18.0/255), 
                            Gf.Vec3f(196.0/255, 175.0/255, 24.0/255), 
                            Gf.Vec3f(217.0/255, 194.0/255, 29.0/255), 
                            Gf.Vec3f(237.0/255, 214.0/255, 34.0/255)]
    legendColorsCyanRed = [Gf.Vec3f(21.0/255, 101.0/255, 109.0/255), 
                            Gf.Vec3f(68.0/255, 143.0/255, 154.0/255), 
                            Gf.Vec3f(0, 161.0/255, 172.0/255), 
                            Gf.Vec3f(84.0/255, 193.0/255, 207.0/255),
                            Gf.Vec3f(1, 190.0/255, 202.0/255),
                            Gf.Vec3f(240.0/255, 113.0/255, 120.0/255),  
                            Gf.Vec3f(1, 28.0/255, 0)]
    legendColorList = {"Blue to Green to Red": legendColors, 
                        "Blue to Yellow to Red": legendColors2, 
                        "Blue to Yellow": legendColorsBlueYellow,
                        "Cyan to Red": legendColorsCyanRed}
    sensorList = {'a1': 'a1',
                    'a2':'a2',
                    'a3':'a3',
                    'a4':'a4'}

    curr_legColor = 0

    def __init__(self) -> None:
            super().__init__()
            self.viewport_scene = None

    def on_startup(self, ext_id):
        print("[orion.sensor] MyExtension startup")
        # Get active viewport and create viewport_scene to draw to
        viewport_window = omni.kit.viewport.utility.get_active_viewport_window() 
        self.viewport_scene = ViewportSceneInfo(viewport_window, ext_id)
        self.sensors = Sensors(self.viewport_scene)

        self._window = ui.Window("Visualize Sensor Data", width=300, height=300)
        with self._window.frame:
            with ui.VStack(): 
                
                # ------------------------------------------------------------#
                # main functions the create sensors and visualize sensor data #
                # ------------------------------------------------------------#
                def createSensor():
                    print("clicked!")
                    self.sensors.createSensor(Func.getComboValue(sensorIdCombo, MyExtension.sensorList), Func.getSelPaths())
                def visualizeSensor():
                    print("clicked!")
                
                # ------------#
                # UI Elements #
                # ------------#
                ui.Label("Visualize Sensor Data and Create Legend", 
                        style = {"alignment":ui.Alignment.CENTER, "font_size": 25})

                sensorIdCombo = Func.makeComboAndLabel("Sensor ID", MyExtension.sensorList)
                ui.Button("Create Sensor", clicked_fn=lambda: createSensor(), style = {"font_size": 30})
                magicNumHeight = 30  # For things to look good
                with ui.HStack(height=0):
                    with ui.VStack():
                        dataComboBox = Func.makeComboAndLabel("Data", MyExtension.dataList)
                    
                    with ui.VStack():
                        paletteComboBox = Func.makeComboAndLabel("Legend Color Palette", MyExtension.legendColorList)

                    with ui.VStack():                            
                        directions = {'top':'top', 'bottom':'bottom', 'left':'left', 'right':'right'}
                        directionComboBox = Func.makeComboAndLabel("Legend Placement Relative to Viewport", directions)
                        def dummy_legend():
                            # If energy simulation not been visualized yet, prevent creating/changing legend
                            if MyExtension.curr_legColor == 0:
                                return
                            LegendOverlay.make_legend_overlay(Func.getComboValue(directionComboBox, directions), MyExtension.curr_legColor, viewport_window)
                        directionComboBox.model.add_item_changed_fn(lambda m, i: dummy_legend())
                ui.Button("Visualize", clicked_fn=lambda: visualizeSensor(), style = {"font_size": 30})

    def on_shutdown(self):
        self.sensors.destroy()
        if self.viewport_scene:
            self.viewport_scene.destroy()
            self.viewport_scene = None
        print("[orion.sensor] MyExtension shutdown")
