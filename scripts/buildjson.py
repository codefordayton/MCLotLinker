import dbm
import csv
import json
from datetime import datetime

def get_city(record):
    return ' '.join(latlon[2:])

applied = []
with open('parcels.csv') as csvfile:
  reader = csv.DictReader(csvfile, ['parcel', 'addl', 'address'])
  for row in reader:
    applied.append(row['parcel'])
    if len(row['addl']) > 0:
      addl = row['addl'].split(',')
      for record in addl:
        record = record.strip()
        value = row['parcel'][:len(row['parcel']) - len(record)] + record
        applied.append(value)


db = dbm.open('./centroids.dbm', 'r')
#open output json file
file = open('georeaps.json', 'w')
values = []
with open('reapitems.csv') as csvfile:
    reader = csv.DictReader(csvfile, ['parcel', 'street', 'eligible', 'paymentplan', 'lastyear', 'paymentwindow', 'class', 'buildingvalue'])
    for row in reader:
        if row['eligible'] != 'Sold' and row['paymentplan'] == 'False' and row['paymentwindow'] == 'False' and row['lastyear'] < '2013' and row['class'] == 'R':
            try:
                latlon = db[row['parcel']].split()
                claimed = False
                lot = False
                if row['parcel'] in applied:
                    claimed = True
                if row['buildingvalue'] == '000000000000.00':
                    lot = True
                values.append({'parcelid': row['parcel'], 'street': row['street'] + ', ' + get_city(latlon), 'lat': latlon[0], 'lon': latlon[1], 'lot': lot, 'claimed': claimed})
            except Exception as e:
                print(e)
                #if not, log it in a separate json file for analysis/reporting
                print row['parcel']
    file.write('var lastupdated = new Date("' + datetime.now().strftime("%B %d, %Y %H:%M:%S") + '");\n')
    file.write('var points =')
    file.write(json.dumps(values, indent=2))
    file.write(';')
    file.close()
