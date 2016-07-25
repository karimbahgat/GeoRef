"""
GeoRef
Python Offline Georeferencer
by Karim Bahgat, 2014

Unfinished alpha version
"""

from helpers import timetaker,messages
from downloader import *
from datamanager import *



# FOR ADVANCED INSPIRATION AND ALGORITHM,
# SEE: https://github.com/mapbox/carmen/tree/master/test



#INTERNAL USE ONLY
class Geocoder:
    """
    The class that does the geocoding behind the scene
    
    IDEA: make geocoding condition a simple str expression for exec()...
    """
    def __init__(self):
        pass
    def add_match_condition(self):
        pass
    def find_match(self):
        #load and open country lookup table
        #loop through country table
        #   compare each record with the queried names/match conditions
        #   create match dictionary if match above threshold
        #return all match dictionaries
        pass

#USER FUNCTIONS
def geocode(city=None, adm1=None, adm2=None, adm3=None, admx=None, country=None):
    """
    Should return a dictionary with matched city,adm,country,shapetype,point/polygon coordinates,match similarity etc.
    """
    names = city,adm1,adm2,adm3,admx,country
    geocoder = Geocoder()
    for name in names:
        geocoder.add_match_condition(name)
    results = geocoder.find_match()
    return results

if __name__ == "__main__":
    #Download("gadm", downpath="C:/Users/BIGKIMO/Desktop/GADM_dl")
    pass
