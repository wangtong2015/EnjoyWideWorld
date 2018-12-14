# This file includes all funtions handling HttpRequests
# in global usecase 'map'.
# ZHOU Kunpeng, 14 Dec 2018

from django.http import HttpResponse
from map.mapDAOs import GetPositionsAround

def test(request):
    return HttpResponse("Boun giorno!")

def getPositions(request):
    if(request.method == "GET"):
        return HttpResponse("ERROR: request should use POST instead of GET")

    resp = {}

    try:
        longitude = float(request.POST.get("longitude", None))
        latitude = float(request.POST.get("latitude", None))

        dao = GetPositionsAround()
        positions = dao.getPositionsAround(longitude, latitude)

        resp['length'] = len(positions)
        for i in range(len(positions)):
            resp['id' + string(i)] = string(positions[i][0])
            resp['lat' + string(i)] = string(positions[i][1])
            resp['lon' + string(i)] = string(positions[i][2])

    except Exception as e:
        resp['length'] = 0
        resp['error'] = 1
        print(e.message)

    finally:
        return HttpResponse(json.dumps(resp), content_type="application/json")
