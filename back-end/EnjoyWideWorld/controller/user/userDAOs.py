# All Data Access Objects in global usecase 'user'.
# ZHOU Kunpeng, 24 Dec 2018

from model import models

class GetUserProfileDAO():
    def getUserProfile(self, userId):
        user = models.User.objects.get(wechatId = userId)
        result = {}
        result['totalLikes'] = user.totalLikes
        return result


# update the user info with given nickname, avatar, and other stuffs
# if user does not exist, then create one.
class UpdateUserInfoDAO():
    def updateUserInfo(self, userId, nickname = None, avatarurl = None, province = None, city = None):
        # find user; if not exist, then create one
        userQuery = models.User.objects.filter(wechatId = userId)
        if len(userQuery) == 0:
            user = models.User.objects.create(wechatId = userId)
        else:
            user = userQuery[0]
        
        # update
        if nickname != None:
            user.nickname = nickname
        if avatarurl != None:
            user.avatarUrl = avatarurl
        if province != None:
            user.province = province
        if city != None:
            user.city = city
        user.save()