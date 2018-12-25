# Test cases for global usecase 'map'.
# ZHOU Kunpeng, 25 Dec 2018

from random import random
from math import floor
import json

from django.test import TestCase

from model import models


class MapTestCase(TestCase):

    _points = []
    _items = []

    _lower = 39.98
    _upper = 40.02
    _left = 116.30
    _right = 116.35

    def _createPairs(self, numberOfPoints):
        for i in range(numberOfPoints):
            lon = random() * (self._right - self._left) + self._left
            lat = random() * (self._upper - self._lower) + self._lower
            self._points.append((lon, lat))

    def setUp(self):
        # number of items and positions to create
        numberOfPoints = 20

        # Create items
        for i in range(numberOfPoints):
            item = models.Item.objects.create(         \
                name='item' + str(i),                  \
                description='itemDesc' + str(i),       \
                addExp=floor(random() * 200 + 50),            \
                addHealth=floor(random() * 50 + 2),           \
                addAttack=floor(random() * 10 + 2),           \
                addDefend=floor(random() * 10 + 2),           \
                addSpeed=floor(random() * 10 + 2),            \
                addDodgeRate=floor(random() * 1.5))
            
            self._items.append(item)

        # create positions
        self._createPairs(numberOfPoints)
        for i in range(numberOfPoints):
            lon, lat = self._points[i]
            models.Position.objects.create(            \
                name='position' + str(i),              \
                longitude=lon, latitude=lat,           \
                pictureAddr='pic' + str(i),     \
                description='posDesc' + str(i),        \
                itemLinked=self._items[i])
        
        # create user and his pet 
        self._user = models.User.objects.create(wechatId='JonDoe1997')
        self._pet = models.Pet.objects.create(master=self._user, \
            name='pikachu', experience=100, appearanceId=0, \
            health=50, attack=12, defend=6, speed=10, dodgeRate=1)
    
    # Randomly changes user's position and do repeating queries
    def test_getPositions(self):
        numberOfReq = 100
        for i in range(numberOfReq):
            # raise query in a random position
            lon = random() * (self._right - self._left) + self._left
            lat = random() * (self._upper - self._lower) + self._lower
            response = self.client.post('/map/getpositions',     \
                {'wechatId': self._user.wechatId,               \
                 'longitude': lon, 'latitude': lat})
            self.assertEqual(response.status_code, 200) # no http failure
            # check if user's last location has been updated
            self.assertAlmostEqual(float(models.User.objects.get(wechatId=self._user.wechatId).lastLongitude), lon)
            self.assertAlmostEqual(float(models.User.objects.get(wechatId=self._user.wechatId).lastLatitude), lat)

    # Randomly check in positions, and check results
    def test_checkIn(self):
        numberOfReq = 40
        
        # initialize records whether position i is checked in 
        # where its index ranges [0, number of points - 1]
        # (id ranges [1, number of points])
        checked = [] 
        for i in range(len(self._points)):
            checked.append(False)
        
        # do checkins
        for i in range(numberOfReq):
            id = floor(random() * len(self._points) + 1)
            response = self.client.post('/map/checkin',      \
                {'wechatId' : self._user.wechatId, 'positionId' : id})
            jsonResp = json.loads(response.content)

            self.assertEqual(response.status_code, 200) # no http failure
            # checked in before: should fail
            if checked[id - 1]:
                self.assertEqual(jsonResp['success'], 0)
            # should success
            else:
                self.assertEqual(jsonResp['success'], 1)
                # check item linked
                self.assertEqual(jsonResp['item'], self._items[id - 1].id)
                self.assertEqual(jsonResp['addExp'], self._items[id - 1].addExp)
                self.assertEqual(jsonResp['addHealth'], self._items[id - 1].addHealth)
                self.assertEqual(jsonResp['addAttack'], self._items[id - 1].addAttack)
                self.assertEqual(jsonResp['addDefend'], self._items[id - 1].addDefend)
                self.assertEqual(jsonResp['addSpeed'], self._items[id - 1].addSpeed)
                self.assertEqual(jsonResp['addDodgeRate'], self._items[id - 1].addDodgeRate)
                # check pet info
                self._pet.experience += self._items[id - 1].addExp
                self._pet.health += self._items[id - 1].addHealth
                self._pet.attack += self._items[id - 1].addAttack
                self._pet.defend += self._items[id - 1].addDefend
                self._pet.speed += self._items[id - 1].addSpeed
                self._pet.dodgeRate += self._items[id - 1].addDodgeRate
                self.assertEqual(models.Pet.objects.get(id=self._pet.id).experience, self._pet.experience)
                self.assertEqual(models.Pet.objects.get(id=self._pet.id).health, self._pet.health)
                self.assertEqual(models.Pet.objects.get(id=self._pet.id).attack, self._pet.attack)
                self.assertEqual(models.Pet.objects.get(id=self._pet.id).defend, self._pet.defend)
                self.assertEqual(models.Pet.objects.get(id=self._pet.id).speed, self._pet.speed)
                self.assertEqual(models.Pet.objects.get(id=self._pet.id).dodgeRate, self._pet.dodgeRate)
            
            # set checked
            checked[id - 1] = True
