# This file includes all funtions handling HttpRequests
# in global usecase 'map'.
# ZHOU Kunpeng, 14 Dec 2018

from django.http import HttpResponse
from . import mapDAOs
import json

def test(request):
    return HttpResponse("Boun giorno!")

def getPositions(request):

    resp = {}

    try:

        if(request.method == "GET"):
            raise Exception("ERROR: request should use POST instead of GET")

        longitude = request.POST.get("longitude")
        latitude = request.POST.get("latitude")

        dao = mapDAOs.GetPositionsAround()
        positions = dao.getPositionsAround(float(longitude), float(latitude))

        resp['length'] = len(positions)
        for i in range(len(positions)):
            resp['id' + str(i)] = str(positions[i][0])
            resp['lat' + str(i)] = str(positions[i][1])
            resp['lon' + str(i)] = str(positions[i][2])

    except Exception as e:
        resp['length'] = 0
        resp['error'] = e.message
        print(e.message)

    finally:
        return HttpResponse(json.dumps(resp), content_type="application/json")
