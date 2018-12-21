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
            raise Exception("ERROR: wechat id does not match any users")

        response['id'] = pet.id
        response['name'] = pet.name
        response['exp'] = pet.experience
        response['appearance'] = pet.appearanceId
        response['health'] = pet.health
        response['defend'] = pet.defend
        response['attack'] = pet.attack
        response['speed'] = pet.speed
        response['dodgeRate'] = pet.dodgeRate


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

# def getPetInfo(request):

#     resp = {}
#     resp['success'] = True

#     try:
#         if request.method == "POST":
#             wxid = request.POST.get("wechatId")
#         elif request.method == "GET":
#             wxid = request.GET.get("wechatId")
#         else:
#             raise Exception("ERROR: illegal request method")

#         # require wechat id 
#         if wxid == "":
#             raise Exception("ERROR: empty wechat id")

#         dao = petDAOs.GetPetInfo()
#         pet = dao.getPetInfo(wxid)

#         if pet == None:
#             raise Exception("ERROR: wechat id does not match any users")

#         resp['id'] = pet.id
#         resp['name'] = pet.name
#         resp['exp'] = pet.experience
#         resp['appearance'] = pet.appearanceId
#         resp['health'] = pet.health
#         resp['defend'] = pet.defend
#         resp['attack'] = pet.attack
#         resp['speed'] = pet.speed
#         resp['dodgeRate'] = pet.dodgeRate

#     except Exception as e:
#         resp['success'] = False
#         resp['error'] = str(e)
#         print(e)

#     finally:
#         return HttpResponse(json.dumps(resp), content_type="application/json")

