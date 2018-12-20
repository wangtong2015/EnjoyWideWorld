# Get all positions around given point within 2 km circle.
# ZHOU Kunpeng, 14 Dec 2018

from model import models
from math import *

# Get all positions around 2km range centered at given point
class GetPositionsAround():
    # params: longitude (float), latitude(float)
    # returns: a list of positions with their item information
    def getPositionsAround(self, longitude, latitude):

        # Range of the circle (only get positions within range)
        RANGE = 2

        positionsAround = []
        positions = models.Position.objects.all()

        for position in positions:
            # within 2 km range
            dist = self._getDistance(longitude, latitude, position.longitude, position.latitude)
            if dist <= RANGE:
                # positionsAround.append([position.id, position.longitude, position.latitude, position])
                positionsAround.append(position)

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

# Get all positions on map
class GetAllPositions():
    # params: longitude (float), latitude(float)
    # returns: a list of positions with their item information
    def getAllPositions(self):

        positionsRet = []
        positions = models.Position.objects.all()

        for position in positions:
            positionsRet.append(position)

        return positionsRet

# A user checks in a given position
class CheckIn():
    # params: wechatId (string), positionId (int)
    # returns: the item that applies its effect on user's pet.
    def checkIn(self, wechatId, positionId):
        # get user and position
        user = models.User.objects.filter(wechatId = wechatId)[0]
        position = models.Position.objects.filter(id = positionId)[0]

        if user == None or position == None:
            return None

        # check if this place (position) has been checked in by this user
        for position in user.checkInPositions.all():
            if position.id == positionId:
                return None

        # Create a check-in record
        checkInRecord = models.CheckInRecord.objects.create(user=user, point=position)

        # Upgrade pet's ability
        pet = user.pets.all()[0]
        item = position.itemLinked

        pet.experience += item.addExp
        pet.health += item.addHealth
        pet.attack += item.addAttack
        pet.defend += item.addDefend
        pet.speed += item.addSpeed
        pet.dodgeRate += item.addDodgeRate
        pet.save()

        return item
