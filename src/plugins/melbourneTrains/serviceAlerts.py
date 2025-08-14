import re
import requests
from collections import defaultdict
from google.transit import gtfs_realtime_pb2

# --------------------------
# Config
# --------------------------
API_KEY = "b6716086-2f5f-4551-ab51-ae34c8fe9ed9"
FEED_URL = "https://api.opendata.transport.vic.gov.au/opendata/public-transport/gtfs/realtime/v1/metro/service-alerts"

# Metro train line codes -> human names
ALL_LINES = {
    "ALM": "Alamein",
    "BEL": "Belgrave",
    "CRB": "Craigieburn",
    "CBE": "Cranbourne",
    "FKN": "Frankston",
    "GLN": "Glen Waverley",
    "HBE": "Hurstbridge",
    "LIL": "Lilydale",
    "MER": "Mernda",
    "PKM": "Pakenham",
    "SBE": "Sandringham",
    "SUN": "Sunbury",
    "UPF": "Upfield",
    "WER": "Werribee",
    "WIL": "Williamstown",
}

# Status priority (lowest index = worst)
STATUS_PRIORITY = [
    "Suspended",
    "Major Delays",
    "Cancellation",
    "Service Change",
    "Minor Delays",
    "Planned works",
    "Good Service"
]

# Mapping for normalisation
NORMALISE = {
    "planned works": "Planned works",
    "minor delay": "Minor Delays",
    "minor delays": "Minor Delays",
    "major delay": "Major Delays",
    "major delays": "Major Delays",
    "suspended": "Suspended",
    "cancellation": "Cancellation",
    "service change": "Service Change",
    "good service": "Good Service",
}

# Ignore station precinct works
IGNORE_KEYWORDS = ["station", "car space"]


def normalise_status(text):
    return NORMALISE.get(text.strip().lower(), None)


def get_worst_status(statuses):
    priority_map = {status: i for i, status in enumerate(STATUS_PRIORITY)}
    return sorted(statuses, key=lambda s: priority_map.get(s, 999))[0]


def fetch_and_parse_feed():
    headers = {"KeyId": API_KEY}
    r = requests.get(FEED_URL, headers=headers)
    r.raise_for_status()

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(r.content)

    grouped = defaultdict(list)  # route_code -> [(status, description)]

    for entity in feed.entity:
        if not entity.HasField("alert"):
            continue

        alert = entity.alert

        # Get status from header_text
        header_text = alert.header_text.translation[0].text if alert.header_text.translation else ""
        if any(k in header_text.lower() for k in IGNORE_KEYWORDS):
            continue

        status = normalise_status(header_text)
        if not status:
            continue

        # Prefer description_text, fallback to header_text
        if alert.description_text.translation and alert.description_text.translation[0].text.strip():
            description = alert.description_text.translation[0].text
        else:
            description = header_text

        # Extract route IDs
        route_ids = set()
        for ie in alert.informed_entity:
            if ie.route_id:
                match = re.search(r"vic-02-([A-Z]+)", ie.route_id)
                if match:
                    route_ids.add(match.group(1))

        for rid in route_ids:
            grouped[rid].append((status, description))

    # Build final dict
    final_status = {}
    for rid, name in ALL_LINES.items():
        if rid in grouped:
            statuses = [s for s, _ in grouped[rid]]
            worst_status = get_worst_status(statuses)
            matching_descs = list({desc for s, desc in grouped[rid] if s == worst_status and desc})
            final_status[name] = {
                "status": worst_status,
                "descriptions": matching_descs
            }
        else:
            final_status[name] = {
                "status": "Good Service",
                "descriptions": []
            }

    return final_status