# This file includes all funtions handling HttpRequests
# in global usecase 'pet'.
# ZHOU Kunpeng, 18 Dec 2018

# Modified 22 Dec 2018: implement AttribServlet abstract class

from django.http import HttpResponse
from controller.pet import petDAOs
import json


# servlet for pet/petinfo
# returns necessary information for a pet
# request: GET or POST w/params
#   wechatId (string)
# response: pet information
#   id (int)
#   name (string)
#   appearance (int)
#   exp (int)
#   health/attack/defend/speed/dodgeRate (int)

from controller.servlet import AttribServlet

# Facade method
def getPetInfo(request):
    return GetPetInfoServlet().execute(request)

# Do the exact things
class GetPetInfoServlet(AttribServlet):

    def _action(self, request, response):
        wxid = request.get('wechatId')
        # require wechat id 
        if wxid == "":
            raise Exception("ERROR: empty wechat id")

        pet = petDAOs.GetPetInfo().getPetInfo(wxid)

        if pet == None:
            raise Exception("ERROR: cannot find pet or user")

        response['id'] = pet.id
        response['name'] = pet.name
        response['exp'] = pet.experience
        response['appearance'] = pet.appearanceId
        response['health'] = pet.health
        response['defend'] = pet.defend
        response['attack'] = pet.attack
        response['speed'] = pet.speed
        response['dodgeRate'] = pet.dodgeRate


# servlet for pet/add
# Add a new pet to the database. 
# request: POST or GET w/params
#   wechatId (string): user id
#   characterName (string): name of the pet
#   characterHP (int): health
#   characterAD (int): attack
#   characterDF (int): defend
#   characterSP (int): speed
#   characterMiss (int): dodgeRate
#   characterAppearance (int): appearanceId
#   characterExp (int): experience
# response: 
#   characterID (int): id of the pet

def createPet(request):
    return CreatePetServlet().execute(request)

class CreatePetServlet(AttribServlet):
    def _action(self, request, response):
        wechatId = request.get('wechatId')
        name = request.get('characterName')
        health = request.get('characterHP')
        attack = request.get('characterAD')
        defend = request.get('characterDF')
        speed = request.get('characterSP')
        dodgeRate = request.get('characterMiss')
        appearanceId = request.get('characterAppearance')
        experience = request.get('characterExp')

        print(name)

        id = petDAOs.CreatePet().createPet(wechatId, name, experience, \
            appearanceId, health, attack, defend, speed, dodgeRate)
        
        response['characterID'] = id