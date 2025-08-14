import csv
from datetime import datetime

STATION_NAME = "Sunbury Station"

DAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday"
]

def processData(STATION_NAME, PLUGIN_DIR):
    # Step 1: Get Station ID for each platform
    stationIDs = {}

    with open(f"{PLUGIN_DIR}/data/stops.txt", "r", encoding='utf-8-sig') as stopsFile:
        reader = csv.DictReader(stopsFile)
        for row in reader:
            if row['stop_name'] == STATION_NAME:
                stationIDs[row['platform_code']] = row['stop_id']
        
    # Inverted Dictionary       
    invStationIDs = {v: k for k, v in stationIDs.items()}

    # Step 2: Get service_ids for today from calendar.txt
    serviceIDs = []

    currentDay = DAYS[datetime.today().weekday()]
    currentTime = datetime.now()

    with open(f"{PLUGIN_DIR}/data/calendar.txt", "r", encoding="utf-8-sig") as calendarFile:
        reader = csv.DictReader(calendarFile)
        for row in reader:
            # If the service id is valid for today
            if row[currentDay] == "1":
                # Check if the timetable is in effect yet
                startDate = datetime.strptime(row["start_date"], "%Y%m%d")
                endDate = datetime.strptime(row["end_date"], "%Y%m%d")
                if startDate <= currentTime <= endDate:
                    serviceIDs.append(row["service_id"])
                

    # Step 3: Get trips with valid service ids for today
    tripsForToday = []

    with open(f"{PLUGIN_DIR}/data/trips.txt", "r", encoding="utf-8-sig") as tripsFile:
        reader = csv.DictReader(tripsFile)
        for row in reader:
            if row["service_id"] in serviceIDs:
                tripsForToday.append(row["trip_id"])
                
    # Step 3a: Create dictionary of tripIDs to trip names
    tripNames = {}
    
    with open(f"{PLUGIN_DIR}/data/trips.txt", "r", encoding="utf-8-sig") as tripsFile:
        reader = csv.DictReader(tripsFile)
        for row in reader:
            tripNames[row["trip_id"]] = row["trip_headsign"]

    # Step 4: Get all departures for our station ids
    departures = {}

    for stopID in stationIDs.values():
        departures[stopID] = []
        

    with open(f"{PLUGIN_DIR}/data/stop_times.txt", "r", encoding="utf-8-sig") as stopTimesFile:
        reader = csv.DictReader(stopTimesFile)
        for row in reader:
            if row["stop_id"] in departures.keys() and row["stop_sequence"] == "1":
                departures[row["stop_id"]].append(row)
                

    # Step 5: Filter departures by todays valid trip_ids
    filteredDepartures = {}

    for stopID in stationIDs.values():
        filteredDepartures[stopID] = []

    for platform in departures.keys():
        for trip in departures[platform]:
            if trip["trip_id"] in tripsForToday:
                filteredDepartures[trip["stop_id"]].append(trip)


    # Step 6: Sort departures by time
    for platform in filteredDepartures.keys():
        filteredDepartures[platform] = sorted(filteredDepartures[platform], key=lambda x: x["departure_time"])
    
    return invStationIDs, filteredDepartures, tripNames
        
def printData(invStationIDs, filteredDepartures, tripNames):
    for platform in filteredDepartures.keys():
        print(f"Departures for Platform {invStationIDs[platform]}")
        for departure in filteredDepartures[platform]:
            if int(departure["departure_time"][:2]) >= 24:
                continue
            if datetime.strptime(departure["departure_time"], "%H:%M:%S").time() >= datetime.now().time():
                print(departure["departure_time"], tripNames[departure["trip_id"]])
            
# invStationIDs, filteredDepartures, tripNames = processData("Sunbury Station")
# printData(invStationIDs, filteredDepartures, tripNames)
