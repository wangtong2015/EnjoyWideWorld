# This file includes all funtions handling HttpRequests
# in global usecase 'community'.
# ZHOU Kunpeng, 21 Dec 2018

from django.http import HttpResponse
from controller.community import communityDAOs
from controller.map import mapDAOs
import json

# servlet for community/usersnearby
# request: POST w/form params
#   user (string) indicates the wechat id of the user who's sending request
#   longitude (float) & latitude (float) indicates user's current location
# response: json
#   length (int) indicates the length of valid users within R radius
#   userx (string) is the wechat id of xth user
def getUsersNearby(request):
    resp = {}
    resp['success'] = 1

    try:
        resp['length'] = 0

        if(request.method != "POST"):
            raise Exception("ERROR: request should use POST")

        # get user wechat id from request
        user = request.POST.get("user")
        if user == "" :
            raise Exception("ERROR: empty user id")

        # get longitude and latutude 
        longitudeStr = request.POST.get("longitude")
        latitudeStr = request.POST.get("latitude")
        if longitudeStr == "" or latitudeStr == "" :
            raise Exception("ERROR: empty longitude or latitude")
        longitude = float(longitudeStr)
        latitude = float(latitudeStr)

        # query
        R = 1.5     # Range in km
        result = communityDAOs.GerUsersNearby().getUsersNearby(user, longitude, latitude, R)

        # update last location
        mapDAOs.UpdateUserLocation().updateUserLocation(user, longitude, latitude)

        # format output
        resp['length'] = len(result)
        for i in range(len(result)):
            resp['user' + str(i)] = result[i]

    except Exception as e:
        resp['success'] = 0
        resp['error'] = str(e)
        print(e)

    finally:
        # pack up json and return
        return HttpResponse(json.dumps(resp), content_type="application/json")


# servlet for community/friendsinfo
# request: POST w/form params
#   user (string) indicates the wechat id of the user who's sending request
#   length (int) indicates the length of friend list
#   friendx (string) is the xth friend's wechat id, x in [0, length)
# response: json
#   length (int) indicates the length of valid friend list
#   expx (int) is exp of the xth friend's pet
#   isLikedx (int, 0 or 1) indicates whether the user has liked his/her xth friend
def getFriendsInfo(request):
    resp = {}
    resp['success'] = 1

    try:
        if(request.method != "POST"):
            raise Exception("ERROR: request should use POST")

        # get user wechat id from request
        user = request.POST.get("user")
        if user == "" :
            raise Exception("ERROR: empty user id")

        # get all friends from request; if failed, raise error
        length = int(request.POST.get("length", "0"))
        friends = []
        for i in range(length):
            friend = request.POST.get("friend" + str(i))
            if friend == "":
                raise Exception("ERROR: empty friend id in request at index " + str(i))
            friends.append(friend)

        # execute query
        dao = communityDAOs.GetFriendsInfo()
        # expected return: list of dictionaries, one dict for one friend
        friendsInfo = dao.getFriendsInfo(user, friends)

        # format
        resp['length'] = len(friendsInfo)
        for i in range(len(friendsInfo)):
            resp['exist' + str(i)] = str(friendsInfo[i]['exist'])
            if friendsInfo[i]['exist'] > 0:
                resp['exp' + str(i)] = str(friendsInfo[i]['exp'])
                resp['isLiked' + str(i)] = str(friendsInfo[i]['isLiked'])

    except Exception as e:
        resp['success'] = 0
        resp['error'] = str(e)
        print(e)

    finally:
        # pack up json and return
        return HttpResponse(json.dumps(resp), content_type="application/json")


# servlet for community/like
# request: POST w/form params
#   user (string) indicates the wechat id of the user who's sending request
#   friend (string) indicates the user who's being liked / canceled like
#   type (int) indicates the operation. 1=like, 0=delike
# response: json
#   performed (int): 1=success, 0=has been liked or deliked before
#   (NOTE success is still 1 if performed = 0. All other errors will cause success=0. )
def likeDelike(request):
    resp = {}
    resp['success'] = 1

    try:
        if(request.method != "POST"):
            raise Exception("ERROR: request should use POST")

        # get user wechat id from request
        user = request.POST.get("user")
        if user == "" :
            raise Exception("ERROR: empty user id")

        # get the one being liked from request
        friend = request.POST.get("friend")
        if friend == "":
            raise Exception("ERROR: empty friend id")

        typeStr = request.POST.get("type")
        if typeStr == "1":
            type = 1
        else:
            type = 0

        # perform like
        dao = communityDAOs.LikeDelike()
        result = dao.likeDelike(user, friend, type)
        if result:
            resp['performed'] = 1
        else:
            resp['performed'] = 0

    except Exception as e:
        resp['success'] = 0
        resp['error'] = str(e)
        print(e)

    finally:
        # pack up json and return
        return HttpResponse(json.dumps(resp), content_type="application/json")
