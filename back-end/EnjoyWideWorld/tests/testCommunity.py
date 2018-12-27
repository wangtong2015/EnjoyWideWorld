# Test cases for global usecase 'community' and 'user'.
# User is here since it involves total number of likes. Use the setup here.
# ZHOU Kunpeng, 25 Dec 2018

from random import random
from math import floor
import json

from django.test import TestCase

from model import models
from controller import utils


class CommunityTestCase(TestCase):
    

    def setUp(self):
        n = 30
        userLocs = self._createPairs(n)
        self._users = []
        self._pets = []
        for i in range(n):
            user = models.User.objects.create(wechatId='wxid_testcase' + str(i), \
                lastLongitude=userLocs[i][0], lastLatitude=userLocs[i][1])
            pet = models.Pet.objects.create(master=user, name='pet' + str(i), \
                experience=floor(random() * 2900 + 100), appearanceId=0)
            self._users.append(user)
            self._pets.append(pet)

    # create random N points within given area on earth
    def _createPairs(self, numberOfPoints):
        _lower = 39.98
        _upper = 40.02
        _left = 116.30
        _right = 116.35

        points = []
        for i in range(numberOfPoints):
            lon = random() * (_right - _left) + _left
            lat = random() * (_upper - _lower) + _lower
            points.append((lon, lat))
        return points

    # NOTE Issue: if sent a bunch of requests together, 
    # will raise TypeError: argument must be int or float
    # when iterating models.User.objects.get().
    # (This error is raised within django's library code. It makes NO f**king sense.)
    # But if run one test at a time, there's no such problem.
    # Doesn't seem to be happening when running on server. Have to rewrite it into 3 tests seperately.
    def _test_nearbyInfo(self, type):
        userIdx = floor(random() * len(self._users)) 
        # randomly create 3 types of requests
        # type = floor(random() * 3)

        # type 0: with user id and location
        # type 1: only with user id
        if type == 0 or type == 1:
            if type == 0:
                lon, lat = self._createPairs(1)[0]
                resp = self.client.post('/community/nearbyinfo', \
                    {'user' : self._users[userIdx].wechatId, \
                    'longitude' : lon, 'latitude' : lat})
            else:
                currentUserInfo = models.User.objects.get(wechatId=self._users[userIdx].wechatId)
                lon = currentUserInfo.lastLongitude
                lat = currentUserInfo.lastLatitude
                resp = self.client.post('/community/nearbyinfo', \
                    {'user' : self._users[userIdx].wechatId})
            
            self.assertEqual(resp.status_code, 200)
            jsonResp = json.loads(resp.content)
            print(resp.content)
            self.assertEqual(jsonResp['success'], 1)
        
        # type 2: invalid user id
        else:
            resp = self.client.post('/community/nearbyinfo', 
                {'user' : 'wxid_xxx'})
            self.assertEqual(resp.status_code, 200)
            jsonResp = json.loads(resp.content)
            self.assertEqual(jsonResp['success'], 0)
    
    def test_nearbyInfoFull(self):
        self._test_nearbyInfo(0)
    
    def test_nearbyInfoWOLoc(self):
        self._test_nearbyInfo(1)
    
    def test_nearbyInfoIllegal(self):
        self._test_nearbyInfo(2)


    # test community/like and user/profile together.
    def test_likeDelike_user(self):

        # total number of requests
        numberOfReqs = 100

        # record all like records locally
        liked = set()

        # init totalLikes to 0 for each user
        totalLikes = []
        for i in range(len(self._users)):
            totalLikes.append(0)
        
        for k in range(numberOfReqs):

            via = floor(random() * len(self._users))
            to = floor(random() * len(self._users))
            userFrom = self._users[via].wechatId
            userTo = self._users[to].wechatId 

            likeType = floor(random() * 3)
            if likeType == 2:
                resp = self.client.post("/community/like", \
                    {'user' : "userFrom", 'friend' : "userTo", 'type' : floor(random() * 2)})
            else:
                resp = self.client.post("/community/like", \
                    {'user' : userFrom, 'friend' : userTo, 'type' : likeType})
            
            self.assertEqual(resp.status_code, 200)
            jsonResp = json.loads(resp.content)

            if likeType == 2:
                self.assertEqual(jsonResp['success'], 0)

            else:
                self.assertEqual(jsonResp['success'], 1)

                if (via, to) in liked and likeType == 0:
                    self.assertEqual(jsonResp['performed'], 1)
                    liked.remove((via, to))
                    totalLikes[to] -= 1

                elif (via, to) not in liked and likeType == 1:
                    self.assertEqual(jsonResp['performed'], 1)
                    liked.add((via, to))
                    totalLikes[to] += 1

                else:
                    self.assertEqual(jsonResp['performed'], 0)
        
        for i in range(len(self._users)):
            resp = self.client.post("/user/profile", \
                    {'wechatId' : self._users[i].wechatId})

            self.assertEqual(resp.status_code, 200)
            jsonResp = json.loads(resp.content)
            self.assertEqual(jsonResp['success'], 1)
            self.assertEqual(jsonResp['totalLikes'], totalLikes[i])