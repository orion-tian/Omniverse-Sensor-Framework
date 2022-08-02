from omni.ui import scene as sc
import omni.ui as ui

from .sensor_csv_parser import Parse

class Click(sc.ClickGesture):
    """class that inherits from sc.ClickGesture to respond to clicks on ui Sensors"""
    def __init__(self, transform: sc.Transform, sensorId):
        super().__init__()
        self.__transform = transform
        self.sensorId = sensorId
        self.windows = {}

    def on_ended(self):
        """creates a pop-up window to display a graph of the temperature data for a csv, whose path is hard coded,
        also makes sure to delete previous windows for the same sensor but there are bugs"""
        # code to make sure to draw only one window per sensor even if it receives multiple clicks, self.windows is a dict of created windows
        # TODO: has bugs of 
        if self.windows.get(self.sensorId) == None:
            window = ui.Window( self.sensorId + " Sensor Data", width=400, height=250)
            self.windows.update({self.sensorId: window})
        else:
            self.windows.get(self.sensorId).destroy()
            window = ui.Window( self.sensorId + " Sensor Data", width=400, height=250)
            self.windows.update({self.sensorId: window})
        # hard coded path to csv file containing sensor temperature data
        sensorDataDict = Parse.parse(R'C:\users\labuser\desktop\orionenergy\orion-sensor-extension\exts\orion.sensor\orion\sensor\dummySensorData.csv')
        with self.windows.get(self.sensorId).frame:
            with ui.VStack():
                for keys in sensorDataDict:
                    # only draw a graph of the data that matches sensor id of clicked ui sensor
                    if self.sensorId == keys:
                        temp = []
                        tm = []
                        magic_width = 50
                        ui.Label(keys + ' sensor temperature data', style={'alignment':ui.Alignment.CENTER, 'font_size': 20})
                        # put all values of temp and time into a single list from the complicated dictionary
                        for values in sensorDataDict[keys]:
                            temp.append(float(values['temp']))
                            tm.append((values['time']))
                        with ui.HStack():
                            with ui.VStack():
                                # the y-axis with min and max temperature
                                ui.Label(str(max(temp)) + 'C', width=magic_width, style={'alignment':ui.Alignment.TOP})
                                ui.Label(str(min(temp)) + 'C', width=magic_width, style={'alignment':ui.Alignment.BOTTOM})
                            # the graph itself with an empty label after to create a buffer between graph and window's right edge for aesthetics
                            ui.Plot(ui.Type.LINE, min(temp), max(temp), *temp, width = 300, height=100, style={'alignment': ui.Alignment.LEFT, 'color':0xFF0000FF})
                            ui.Label('', width=magic_width)
                        with ui.HStack(height=15):
                            # the x-axis with min and max time, also has buffers so they are underneath the graph
                            ui.Label('', width=magic_width)
                            ui.Label(tm[0], style={'alignment':ui.Alignment.LEFT})
                            ui.Label(tm[len(tm)-1], style={'alignment':ui.Alignment.RIGHT})
                            ui.Label('', width=magic_width)

