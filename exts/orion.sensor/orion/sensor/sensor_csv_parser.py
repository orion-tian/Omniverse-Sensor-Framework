import csv

class Parse:
    """class to parse csv files"""

    def parse(fileName):
        """returns a dict of {sensorID: [{time1:temp1}, {time2:temp2},...]}"""
        data = {}
        with open(fileName, 'r') as file:
            csv_reader = csv.reader(file)
            fields = next(csv_reader)
            for row in csv_reader:
                tmp = {}
                time = row[0].strip()
                sensorID = row[1].strip()
                temp = row[2].strip()
                tmp.update({'time':time})
                tmp.update({'temp':temp})
                if data.get(sensorID)==None:
                    data.update({sensorID:[tmp]})
                else:
                    data.update({sensorID:data.get(sensorID) + [tmp]})
        return data
