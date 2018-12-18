# This file includes all data-access objects
# in global use-case 'community'.
# ZHOU Kunpeng, 18 Dec 2018

from model import models
from math import *

# Get all positions around 2km range centered at given point
class GetFriendsInfo():
    # params: user (string, wechat id), friends(list of strings, wechat id)
    # returns: a list of dicts: each dict associated with a friend,
    #   with keys 'exp' and 'isLiked'
    def getFriendsInfo(self, userId, friends):

        # first get the user
        userQueryResult = models.User.objects.filter(wechatId = userId)
        if len(userQueryResult) == 0:
            raise Exception("ERROR: no such user " + userId)
        user = userQueryResult[0]

        # iterate through all friends
        result = []

        for i in range(len(friends)):
            # each friend is associated with a dict
            friendInfo = {}
            friendInfo['exist'] = 1

            # first find the friend
            friendId = friends[i]
            friendQueryResult = models.User.objects.filter(wechatId = friendId)
            if len(friendQueryResult) == 0:
                friendInfo['exist'] = 0
            else:
                friend = friendQueryResult[0]

                # find friend's pet and get its exp
                petQueryResult = models.Pet.objects.filter(master = friend)
                if len(petQueryResult) == 0:
                    friendInfo['exist'] = 0
                else:
                    friendInfo['exp'] = petQueryResult[0].experience

                # check if the user has liked the friend
                likeQueryResult = models.LikeRecord.objects.filter(userFrom = user, userTo = friend)
                if len(likeQueryResult) != 0:
                    friendInfo['isLiked'] = 1
                else:
                    friendInfo['isLiked'] = 0

            result.append(friendInfo)

        return result
