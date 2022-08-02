from omni.ui import scene as sc
import omni.ui as ui

from .sensor_csv_parser import Parse

class Click(sc.ClickGesture):
    def __init__(self, transform: sc.Transform, sensorId):
        super().__init__()
        self.__transform = transform
        self.sensorId = sensorId
        self.windows = {}

    def on_ended(self):
        """creates a window to display the temperature data for a csv which is hard coded currently,
        also makes sure to delete previous windows for the same sensor but there are bugs"""
        if self.windows.get(self.sensorId) == None:
            window = ui.Window( self.sensorId + " Sensor Data", width=300, height=300)
            self.windows.update({self.sensorId: window})
        else:
            self.windows.get(self.sensorId).destroy()
            window = ui.Window( self.sensorId + " Sensor Data", width=300, height=300)
            self.windows.update({self.sensorId: window})
        sensorDataDict = Parse.parse(R'C:\users\labuser\desktop\orionenergy\orion-sensor-extension\exts\orion.sensor\orion\sensor\dummySensorData.csv')
        with self.windows.get(self.sensorId).frame:
            with ui.VStack():
                for keys in sensorDataDict:
                    if self.sensorId == keys:
                        ui.Label(keys + ' sensor temperature data', style={'font_size': 20})
                        for values in sensorDataDict[keys]:
                            ui.Label(values['time'] + ': ' + values['temp'] + ' C')

