import gpxpy.gpx
import requests
import uuid
import os

url = "https://maps.googleapis.com/maps/api/streetview?pitch=70&key=AIzaSyCJge5j2Wb8jsgcn9abQyFCS4qT-M8RZ8M"
size = [400, 420]
url = "{}&size={}x{}".format(url, size[0], size[1])

route_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(".gpx")]

all_points = []
for route_file in route_files:
    gpx_file = open(route_file, 'r')
    gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            all_points += segment.points

print("all points ", all_points.__len__())

filtered_points = all_points[0::12]

print("filtered_points ", filtered_points.__len__())

for i, point in enumerate(filtered_points):
    try:
        location_url = "{}&location={},{}".format(url, point.latitude, point.longitude)
        r = requests.get(location_url)
        if r.status_code == 200:
            with open("googlepics4/a_{}.jpg".format(i), 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            print("googlepics2/{}.jpg".format(i))
    except Exception as e:
        print(e)


