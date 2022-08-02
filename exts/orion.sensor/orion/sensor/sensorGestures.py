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
            window = ui.Window( self.sensorId + " Sensor Data", width=400, height=250)
            self.windows.update({self.sensorId: window})
        else:
            self.windows.get(self.sensorId).destroy()
            window = ui.Window( self.sensorId + " Sensor Data", width=400, height=250)
            self.windows.update({self.sensorId: window})
        sensorDataDict = Parse.parse(R'C:\users\labuser\desktop\orionenergy\orion-sensor-extension\exts\orion.sensor\orion\sensor\dummySensorData.csv')
        with self.windows.get(self.sensorId).frame:
            with ui.VStack():
                for keys in sensorDataDict:
                    if self.sensorId == keys:
                        temp = []
                        tm = []
                        magic_width = 50
                        ui.Label(keys + ' sensor temperature data', style={'alignment':ui.Alignment.CENTER, 'font_size': 20})
                        for values in sensorDataDict[keys]:
                            temp.append(float(values['temp']))
                            tm.append((values['time']))
                        with ui.HStack():
                            with ui.VStack():
                                ui.Label(str(max(temp)) + 'C', width=magic_width, style={'alignment':ui.Alignment.TOP})
                                ui.Label(str(min(temp)) + 'C', width=magic_width, style={'alignment':ui.Alignment.BOTTOM})
                            ui.Plot(ui.Type.LINE, min(temp), max(temp), *temp, width = 300, height=100, style={'alignment': ui.Alignment.LEFT, 'color':0xFF0000FF})
                            ui.Label('', width=magic_width)
                        with ui.HStack(height=15):
                            ui.Label('', width=magic_width)
                            ui.Label(tm[0], style={'alignment':ui.Alignment.LEFT})
                            ui.Label(tm[len(tm)-1], style={'alignment':ui.Alignment.RIGHT})
                            ui.Label('', width=magic_width)

