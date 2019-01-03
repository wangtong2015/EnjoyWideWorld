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
        pet = models.Pet.objects.create(master=user, name=name, experience=experience, \
            appearanceId=appearanceId, health=health, attack=attack, defend=defend, \
            speed=speed, dodgeRate=dodgeRate)
        pet.save()
        return pet.id