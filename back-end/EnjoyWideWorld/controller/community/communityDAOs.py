# This file includes all data-access objects
# in global use-case 'community'.
# ZHOU Kunpeng, 21 Dec 2018

from model import models
from controller import utils
from math import isnan

# Get all users around R km range centered at given point 
#   or user's last location (if longitude & latitude not provided)
class GetNearbyInfo():
    # params: userId (wechat id, string) longitude (float) latitude (float)
    # returns: a list of dicts containing info of all users around the point, 
    #   descending according to pet's exp
    def getNearbyInfo(self, userId, longitude = float('NaN'), latitude = float('NaN')):

        R = 1.5 # (maximum range measured in km)

        user = models.User.objects.get(wechatId = userId)

        # lon & lat optional; if not provided, use user's last location instead
        # x != x means x is NaN
        if isnan(longitude):
            longitude = user.lastLongitude
        if isnan(latitude):
            latitude = user.lastLatitude

        # iterate through all users
        allUsers = models.User.objects.all()
        result = []
        for friend in allUsers:
            # skip user himself/herself
            # if friend.wechatId == user.wechatId:
            #     continue
            
            # dist <= R?
            dist = utils.getDistance(longitude, latitude, friend.lastLongitude, friend.lastLatitude)
            if dist <= R:
                # find pet
                # Added 30 Dec 18: if a user doesn't have a pet, returns 0 exp
                # (I think it is better to have 'continue'?)
                petQuery = models.Pet.objects.filter(master = friend)
                if len(petQuery) == 0:
                    petExp = 0
                else:
                    petExp = petQuery[0].experience
                # find like record; record exist -> user has liked him/her
                likeQueryResult = models.LikeRecord.objects.filter(userFrom = user, userTo = friend)
                if len(likeQueryResult) != 0:
                    like = 1
                else:
                    like = 0
                # find battle record; record exist -> user has challenged him/her
                battleQueryResult = models.BattleRecord.objects.filter(userFrom=user, userTo=friend)
                if len(battleQueryResult) != 0:
                    battle = 1
                else:
                    battle = 0
                dict = {'wechatId': friend.wechatId, 'nickname' : friend.nickname, \
                    'avatarUrl' : friend.avatarUrl, 'exp' : petExp, 'isLiked' : like, 'isBattled' : battle}
                result.append(dict)
        
        result.sort(key=lambda element:element['exp'], reverse=True)

        return result


# Deprecated
# Get all users with most recent location within (longitude,latitude)'s R km range
class GerUsersNearby():
    # params: user (string, wechat id), longitude(float), latitude(float), R=1.5(float, range in km)
    def getUsersNearby(self, userId, longitude = float('NaN'), latitude = float('NaN'), R = 1.5):

        user = models.User.objects.get(wechatId = userId)

        if longitude == float('NaN'):
            longitude = user.lastLongitude
        if latitude == float('NaN'):
            latitude = user.lastLatitude

        allUsers = models.User.objects.all()
        result = []
        for u in allUsers:
            if u.wechatId == user.wechatId:
                continue
            dist = utils.getDistance(longitude, latitude, u.lastLongitude, u.lastLatitude)
            if dist <= R:
                result.append(u.wechatId)
        
        return result 

# Deprecated
# Issue: we can't get user anymore once queried in another DAO. (Why?)
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



# perform like or cancel like
class LikeDelike():

    # find a user with given wechat id. Raise Exception if not found
    def _queryUser(self, userId):
        queryResult = models.User.objects.filter(wechatId = userId)
        if len(queryResult) == 0:
            raise Exception("invalid user name: " + userId)
        return queryResult[0]

    # Do a like (type = 1) / cancel like (delike) (type = 0)
    # params: userFromId (wechat id, string) userToId (wechat id, string)
    # returns: True if perform success,
    #   False if the user tries to like someone he/she has liked
    #                           or delike someone he/she has not liked
    # (if other things go wrong, raise Exception)
    def likeDelike(self, userFromId, userToId, type):
        # Looks like liking oneself is allowed?
        # if userFromId == userToId:
        #     raise Exception("A user cannot like oneself")
        userFrom = self._queryUser(userFromId)
        userTo = self._queryUser(userToId)

        # find potential like record: None if not found
        likeRecordQueryResult = models.LikeRecord.objects.filter(userFrom = userFrom, userTo = userTo)
        if len(likeRecordQueryResult) > 0:
            likeRecord = likeRecordQueryResult[0]
        else:
            likeRecord = None

        if type > 0: # like
            if likeRecord != None:  # has liked before: failed to perform
                return False
            likeRecord = models.LikeRecord(userFrom = userFrom, userTo = userTo)
            likeRecord.save()
            userTo.totalLikes += 1
            userTo.save()

        else:   # delike
            if likeRecord == None:  # has never liked before: failed to perform
                return False
            likeRecord.delete()
            userTo.totalLikes -= 1
            userTo.save()

        return True

class AfterBattle():
    # params: challenger (wechat id, string) challenged (wechat id, string) 
    #   petId (winner's pet id, int) addExp (increase in winner's pet's exp, int)
    # no return value
    def afterBattle(self, challenger, challenged, petId, addExp):
        userFrom = models.User.objects.get(wechatId=challenger)
        userTo = models.User.objects.get(wechatId=challenged)

        battleQueryResult = models.BattleRecord.objects.filter(userFrom=userFrom, userTo=userTo)
        if len(battleQueryResult) > 0:
            raise Exception( \
                "Battle has completed before between {0} and {1}".format(challenger, challenged))
        
        models.BattleRecord.objects.create(userFrom=userFrom, userTo=userTo)

        pet = models.Pet.objects.get(id=petId)
        
        from controller.pet.petDAOs import UpdateExperience
        UpdateExperience().updateExperience(petId, pet.experience + addExp)
        