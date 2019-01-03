# Get all positions around given point within 2 km circle.
# ZHOU Kunpeng, 14 Dec 2018

from model import models
from controller import utils

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
            dist = utils.getDistance(longitude, latitude, position.longitude, position.latitude)
            if dist <= RANGE:
                # positionsAround.append([position.id, position.longitude, position.latitude, position])
                positionsAround.append(position)

        return positionsAround

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

# update last location of a user 
class UpdateUserLocation():
    # params: user(string), longitude(float), latitude(float)
    def updateUserLocation(self, userId, longitude, latitude):
        user = models.User.objects.get(wechatId = userId)
        user.lastLongitude = longitude
        user.lastLatitude = latitude 
        user.save()


from controller.pet import petDAOs
# A user checks in a given position
class CheckIn():
    # params: wechatId (string), positionId (int)
    # returns: a dictionary that shows total effect on user's pet.
    def checkIn(self, wechatId, positionId):
        # get user and position
        user = models.User.objects.filter(wechatId = wechatId)[0]
        position = models.Position.objects.filter(id = positionId)[0]

        if user == None or position == None:
            return None

        # check if this place (position) has been checked in by this user
        checkInQuery = models.CheckInRecord.objects.filter(user=user, point=position)
        if len(checkInQuery) != 0:
            return None

        # Create a check-in record
        checkInRecord = models.CheckInRecord.objects.create(user=user, point=position)

        # Upgrade pet's ability
        pet = user.pets.all()[0]
        item = position.itemLinked

        # pet.experience += item.addExp
        pet.health += item.addHealth
        pet.attack += item.addAttack
        pet.defend += item.addDefend
        pet.speed += item.addSpeed
        pet.dodgeRate += item.addDodgeRate
        pet.save()

        # update pet's experience (if leveled-up, ability will be updated accordingly)
        petDAOs.UpdateExperience().updateExperience(pet.id, pet.experience + item.addExp)

        return item
