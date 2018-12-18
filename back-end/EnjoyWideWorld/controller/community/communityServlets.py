# This file includes all funtions handling HttpRequests
# in global usecase 'community'.
# ZHOU Kunpeng, 18 Dec 2018

from django.http import HttpResponse
from . import communityDAOs
import json

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
        resp['length'] = 0
        resp['error'] = str(e)
        print(e)

    finally:
        # pack up json and return
        return HttpResponse(json.dumps(resp), content_type="application/json")
