# This file includes all funtions handling HttpRequests
# in global usecase 'map'.
# ZHOU Kunpeng, 14 Dec 2018

# Modified 22 Dec 2018: implement AttribServlet abstract class

from django.http import HttpResponse
from controller.map import mapDAOs
from controller import servlet
import json

def test(request):
    return HttpResponse("Buon giorno!")

# servlet for map/getpositions
# Modified 21 Dec 2018: now returns all positions exist in the database, 
#   and update user's latest location into server.
# request: POST w/form params
#   wechatId (string)
#   longitude (float)
#   latitude (float)
# response: json
#   length indicates the length of position list
#   For each position, obtain id, longitude, latitude, pic address, Description
#      of the position by 'idx', 'lonx', 'latx', 'picaddrx', 'descriptionx'
#      where x in range [0, length).
def getPositions(request):
    return GetPositionsServlet().execute(request)

class GetPositionsServlet(servlet.AttribServlet):
    def _action(self, request, response):
        # execute query
        dao = mapDAOs.GetAllPositions()
        positions = dao.getAllPositions()
        # dao = mapDAOs.GetPositionsAround()
        # positions = dao.getPositionsAround(float(longitude), float(latitude))

        # If contains wechatid, lon & lat, update user's latest location
        userId = request.get("wechatId", "")
        longitude = request.get("longitude", "")
        latitude = request.get("latitude", "")
        if userId != "" and longitude != "" and latitude != "":
            updateDao = mapDAOs.UpdateUserLocation()
            updateDao.updateUserLocation(userId, float(longitude), float(latitude))

        # format
        response['length'] = len(positions)
        for i in range(len(positions)):
            response['id' + str(i)] = str(positions[i].id)
            response['name' + str(i)] = str(positions[i].name)
            response['lat' + str(i)] = str(positions[i].latitude)
            response['lon' + str(i)] = str(positions[i].longitude)
            response['picaddr' + str(i)] = str(positions[i].pictureAddr)
            response['description' + str(i)] = str(positions[i].description)
            response['itemName' + str(i)] = str(positions[i].itemLinked.name)


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
    return CheckInServlet().execute(request)

class CheckInServlet(servlet.AttribServlet):
    def _action(self, request, response):
        wxid = request.get("wechatId", "")
        positionId = request.get("positionId", "")

        # execute
        dao = mapDAOs.CheckIn()
        item = dao.checkIn(wxid, int(positionId))

        if item == None:
            raise Exception("Check in failed")

        response['success'] = 1
        response['item'] = item.id
        response['addExp'] = item.addExp
        response['addHealth'] = item.addHealth
        response['addAttack'] = item.addAttack
        response['addDefend'] = item.addDefend
        response['addSpeed'] = item.addSpeed
        response['addDodgeRate'] = item.addDodgeRate
