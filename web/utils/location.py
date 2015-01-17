import urllib.request
from web.config import geocode_apikey
def get_region(latlng):
    # latlng should be in format `lat, lng`
    url_construct = "https://maps.googleapis.com/maps/api/geocode/json?latlng={}&key={}".format(latlng, geocode_apikey)
    response = urllib.request.urlopen(url_construct)
    print(response)
