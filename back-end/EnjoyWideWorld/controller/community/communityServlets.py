# This file includes all funtions handling HttpRequests
# in global usecase 'community'.
# ZHOU Kunpeng, 21 Dec 2018

# Modified 22 Dec 2018: implement AttribServlet abstract class

from django.http import HttpResponse
from controller.community import communityDAOs
from controller.map import mapDAOs
from controller.servlet import AttribServlet 
import json

# servlet for community/nearbyinfo
# request: POST w/form params
#   user (string) indicates the wechat id of the user who's sending request
#   longitude (float) & latitude (float) indicates user's current location
# response: json
#   length (int) indicates the length of valid friend list
#   namex (int) is the name of xth friend
#   expx (int) is exp of the xth friend's pet
#   isLikedx (int, 0 or 1) indicates whether the user has liked his/her xth friend
#   isFightedx (int, 0 or 1) indicates whether the user has battled his/her xth friend as challenger
def getNearbyInfo(request):
    return GetNearbyInfoServlet().execute(request)

class GetNearbyInfoServlet(AttribServlet):
    def _action(self, request, response):
        user = request.get("user")
        if user == "" :
            raise Exception("ERROR: empty user id")

        # get longitude and latutude 
        # 22 Dec 2018: now it is optional
        longitudeStr = request.get("longitude", "")
        latitudeStr = request.get("latitude", "")
        if longitudeStr == "" or latitudeStr == "" :
            # raise Exception("ERROR: empty longitude or latitude")
            longitude = float('NaN')
            latitude = float('NaN')
        else:
            longitude = float(longitudeStr)
            latitude = float(latitudeStr)

        # # query nearbys
        # R = 1.5     # Range in km
        # nearbys = communityDAOs.GerUsersNearby().getUsersNearby(user, longitude, latitude, R)

        # # query nearbys' information 
        # friendsInfo = communityDAOs.GetFriendsInfo().getFriendsInfo(user, nearbys)

        # query 
        friendsInfo = communityDAOs.GetNearbyInfo().getNearbyInfo(user, longitude, latitude)

        # update last location
        mapDAOs.UpdateUserLocation().updateUserLocation(user, longitude, latitude)

        # format
        response['length'] = len(friendsInfo)
        for i in range(len(friendsInfo)):
            # if friendsInfo[i]['exist'] > 0:
            response['wechatId' + str(i)] = str(friendsInfo[i]['wechatId'])
            response['nickname' + str(i)] = str(friendsInfo[i]['nickname'])
            response['avatarUrl' + str(i)] = str(friendsInfo[i]['avatarUrl'])
            response['exp' + str(i)] = str(friendsInfo[i]['exp'])
            response['isLiked' + str(i)] = str(friendsInfo[i]['isLiked'])
            response['isFighted' + str(i)] = str(friendsInfo[i]['isBattled'])


# @DEPRECATED
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
            # raise Exception("ERROR: empty longitude or latitude")
            longitude = float('NaN')
            latitude = float('NaN')
        else:
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

# @DEPRECATED
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
    return LikeDelikeServlet().execute(request)

class LikeDelikeServlet(AttribServlet):
    def _action(self, request, response):
        # get user wechat id from request
        user = request.get("user")
        if user == "" :
            raise Exception("ERROR: empty user id")

        # get the one being liked from request
        friend = request.get("friend")
        if friend == "":
            raise Exception("ERROR: empty friend id")

        typeStr = request.get("type")
        if typeStr == "1":
            type = 1
        else:
            type = 0

        # perform like
        result = communityDAOs.LikeDelike().likeDelike(user, friend, type)

        # return
        if result:
            response['performed'] = 1
        else:
            response['performed'] = 0



# servlet for community/afterbattle
# request: GET or POST w/params
#   attacker (int) : the challenger wechatId 
#   defender (int) : the challenged wechatId
#   petId (int) : pet id of the pet whose exp remains to be updated
#   addExp (int) : the exp added to pet
# response: json
#   no additional information
def afterBattle(request):
    return AfterBattleServlet().execute(request)

class AfterBattleServlet(AttribServlet):
    def _action(self, request, response):
        challenger = request.get('attacker')
        challenged = request.get('defender')
        petId = request.get('petId')
        addExp = request.get('addExp')

        communityDAOs.AfterBattle().afterBattle(challenger, challenged, int(petId), int(addExp))
