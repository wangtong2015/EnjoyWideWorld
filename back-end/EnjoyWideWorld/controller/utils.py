# This file includes all auxillary functions.

from math import *

# params: two (longitude, latitude) points in float
# returns: distance between them on earth
# copied from https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
def getDistance(longitude1, latitude1, longitude2, latitude2):
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

# copied from front-end
def getLevel(experience):
    LEVEL_SET = [0, 20, 60, 140, 300, 620, 1260, 2260]
    TOP_LEVEL = 7
    if experience < LEVEL_SET[TOP_LEVEL]:
        for i in range(TOP_LEVEL):
            if LEVEL_SET[i] <= experience and experience < LEVEL_SET[i + 1]:
                return i
    else: # 超出levels的情况下，以后每级的经验值不变
        left = experience - LEVEL_SET[TOP_LEVEL]
        leftLevels = floor(left / (LEVEL_SET[TOP_LEVEL] - LEVEL_SET[TOP_LEVEL - 1]))
        return TOP_LEVEL + leftLevels
