# Get all positions around given point within 2 km circle.
# ZHOU Kunpeng, 14 Dec 2018

from model import models
from math import *

class GetPositionsAround():
    # params: longitude (float), latitude(float)
    # returns: a list of positions in (id, longitude, latitude) tuple
    #          i.e. w/type list<(int, float, float)>
    def getPositionsAround(self, longitude, latitude):
        positionsAround = []
        positions = models.Position.objects.all()

        for position in positions:
            # within 2 km range
            dist = self._getDistance(longitude, latitude, position.longitude, position.latitude)
            if dist <= 2:
                positionsAround.append([position.id, position.longitude, position.latitude])

        print(positionsAround)
        return positionsAround


    # params: two (longitude, latitude) points in float
    # returns: distance between them on earth
    # copied from https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    def _getDistance(self, longitude1, latitude1, longitude2, latitude2):
        # approximate radius of earth in km
        R = 6373.0

        lat1 = radians(latitude1)
        lon1 = radians(longitude1)
        lat2 = radians(latitude2)
        lon2 = radians(longitude2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        return distance
