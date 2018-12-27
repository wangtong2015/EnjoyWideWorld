# All Data Access Objects in global usecase 'user'.
# ZHOU Kunpeng, 24 Dec 2018

from model import models

class GetUserProfileDAO():
    def getUserProfile(self, userId):
        user = models.User.objects.get(wechatId = userId)
        result = {}
        result['totalLikes'] = user.totalLikes
        return result