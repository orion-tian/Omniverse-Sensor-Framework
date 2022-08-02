import csv

class Parse:
    
    def parse(fileName):
        """returns a dict {sensorID: [{time1:temp1}, {time2:temp2},...]}"""
        data = {}
        with open(fileName, 'r') as file:
            csv_reader = csv.reader(file)
            fields = next(csv_reader)
            # print(fields[0])
            # print(fields[1])
            # print(fields[2])
            for row in csv_reader:
                tmptmp = {}
                time = row[0].strip()
                sensorID = row[1].strip()
                temp = row[2].strip()
                tmptmp.update({'time':time})
                tmptmp.update({'temp':temp})
                if data.get(sensorID)==None:
                    data.update({sensorID:[tmptmp]})
                else:
                    data.update({sensorID:data.get(sensorID) + [tmptmp]})
        return data
