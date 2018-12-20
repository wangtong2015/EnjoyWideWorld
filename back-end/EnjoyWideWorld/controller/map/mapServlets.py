# This file includes all funtions handling HttpRequests
# in global usecase 'map'.
# ZHOU Kunpeng, 14 Dec 2018

from django.http import HttpResponse
from controller.map import mapDAOs
import json

def test(request):
    return HttpResponse("Buon giorno!")

# servlet for map/getpositions
# request: POST w/form params
#   longitude (float)
#   latitude (float)
# response: json
#   length indicates the length of position list
#   For each position, obtain id, longitude, latitude, pic address, Description
#      of the position by 'idx', 'lonx', 'latx', 'picaddrx', 'descriptionx'
#      where x in range [0, length).
def getPositions(request):
    resp = {}

    try:
        if(request.method != "POST"):
            raise Exception("ERROR: request should use POST")

        # longitude = request.POST.get("longitude")
        # latitude = request.POST.get("latitude")

        # execute query
        dao = mapDAOs.GetAllPositions()
        positions = dao.getAllPositions()
        # dao = mapDAOs.GetPositionsAround()
        # positions = dao.getPositionsAround(float(longitude), float(latitude))

        # format
        resp['length'] = len(positions)
        for i in range(len(positions)):
            resp['id' + str(i)] = str(positions[i].id)
            resp['name' + str(i)] = str(positions[i].name)
            resp['lat' + str(i)] = str(positions[i].latitude)
            resp['lon' + str(i)] = str(positions[i].longitude)
            resp['picaddr' + str(i)] = str(positions[i].pictureAddr)
            resp['description' + str(i)] = str(positions[i].description)
            resp['itemName' + str(i)] = str(positions[i].itemLinked.name)

    except Exception as e:
        resp['length'] = 0
        resp['error'] = str(e)
        print(e)

    finally:
        # pack up json and return
        return HttpResponse(json.dumps(resp), content_type="application/json")

# servlet for map/checkin
# request: POST w/form params
#   wechatId (string)
#   positionId (int)
# response: json
#   success: if the check-in is successful
#   item: id of the the item applied to the pet
#   addExp/Health/Attack/Defend/Speed/DodgeRate:
#       increase of experience/health/attack/defend/speed/dodgeRate of pet
def checkIn(request):
    resp = {}

    try:
        if request.method != 'POST':
            raise Exception("ERROR: request should use POST")

        wxid = request.POST.get("wechatId", "")
        positionId = request.POST.get("positionId", "")

        # execute
        dao = mapDAOs.CheckIn()
        item = dao.checkIn(wxid, int(positionId))

        if item == None:
            raise Exception("Check in failed")

        resp['success'] = 1
        resp['item'] = item.id
        resp['addExp'] = item.addExp
        resp['addHealth'] = item.addHealth
        resp['addAttack'] = item.addAttack
        resp['addDefend'] = item.addDefend
        resp['addSpeed'] = item.addSpeed
        resp['addDodgeRate'] = item.addDodgeRate

    except Exception as e:
        resp['success'] = 0
        resp['error'] = str(e)
        print(e)

    finally:
        # pack up json and return
        return HttpResponse(json.dumps(resp), content_type="application/json")
