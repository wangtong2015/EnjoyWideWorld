# Get all positions around given point within 2 km circle.
# ZHOU Kunpeng, 18 Dec 2018

from model import models

# Get all pet information necessary for showing its status
class GetPetInfo():
    # params: wechatId (string)
    # returns: pet object (models.Pet); if user not exist or pet not exist, return None
    def getPetInfo(self, wechatId):
        userQuery = models.User.objects.filter(wechatId = wechatId)
        if len(userQuery) == 0:
            return None
        petQuery = models.Pet.objects.filter(master = userQuery[0])
        if len(petQuery) == 0:
            return None
        return petQuery[0]

# Create a new pet according to info given
class CreatePet():
    # params: wechatId (string) as pet's master, name (string), experience (int), \
    #   appearanceId (int), heath (int), attack (int), defend (int), speed (int), \
    #   dodgeRate (int)
    # returns: the id of the pet (int) 
    def createPet(self, wechatId, name, experience, appearanceId, \
            health, attack, defend, speed, dodgeRate):
        user = models.User.objects.get(wechatId=wechatId)
        petQuery = models.Pet.objects.filter(master=user)
        if len(petQuery) == 0:
            pet = models.Pet.objects.create(master=user, name=name, experience=experience, \
                appearanceId=appearanceId, health=health, attack=attack, defend=defend, \
                speed=speed, dodgeRate=dodgeRate)
        else:
            pet = petQuery[0]
            pet.name = name
            pet.experience = experience
            pet.appearanceId = appearanceId
            pet.health = health
            pet.attack = attack
            pet.defend = defend
            pet.speed = speed
            pet.dodgeRate = dodgeRate
        
        pet.save()
        return pet.id

from math import floor
# Update pet's ability according to the new experience level
class UpdateExperience():
    def updateExperience(self, petId, newExp):
        pet = models.Pet.objects.get(id=petId)
        oldExp = pet.experience
        oldLevel = self._getLevel(oldExp)
        newLevel = self._getLevel(newExp)
        
        pet.experience = newExp
        if newLevel > oldLevel:
            pet.health += 15 * (newLevel - oldLevel)
            pet.attack += 5 * (newLevel - oldLevel)
            pet.defend += 5 * (newLevel - oldLevel)
            pet.speed += 5 * (newLevel - oldLevel)
            pet.dodgeRate += 1 * (newLevel - oldLevel)
        pet.save()

    _levelSet = [0, 20, 60, 140, 300, 620, 1260, 2260]
    _topLevel = 7

    # copied from front-end
    def _getLevel(self, experience):
        if experience < self._levelSet[self._topLevel]:
            for i in range(self._topLevel):
                if self._levelSet[i] <= experience and experience < self._levelSet[i + 1]:
                    return i
        else: # 超出levels的情况下，以后每级的经验值不变
            left = experience - self._levelSet[self._topLevel]
            leftLevels = floor(left / (self._levelSet[self._topLevel] - self._levelSet[self._topLevel - 1]))
            return self._topLevel + leftLevels
