# Get all positions around given point within 2 km circle.
# ZHOU Kunpeng, 14 Dec 2018

from model import models
from math import *

# Get all pet information necessary for showing its status
class GetPetInfo():
    # params: wechatId (string)
    # returns: pet object (models.Pet)
    def getPetInfo(self, wechatId):
        userQuery = models.User.objects.filter(wechatId = wechatId)
        if len(userQuery) == 0:
            return None
        petQuery = models.Pet.objects.filter(master = userQuery[0])
        if len(petQuery) == 0:
            return None
        return petQuery[0]
