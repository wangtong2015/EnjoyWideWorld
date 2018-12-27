# Test cases for global usecase 'pet'.
# ZHOU Kunpeng, 27 Dec 2018

from random import random
from math import floor
import json

from django.test import TestCase

from model import models

class PetTestCase(TestCase):

    def setUp(self):
        self._user = models.User.objects.create(wechatId='wxid_testcase')
        self._pet = models.Pet.objects.create(master=self._user, \
            name='Charizard',                        \
            experience=floor(random() * 2900 + 100), \
            appearanceId=0,                     \
            health=floor(random() * 300 + 100), \
            attack=floor(random() * 20 + 5),    \
            defend=floor(random() * 20 + 5),    \
            speed=floor(random() * 20 + 5),     \
            dodgeRate=floor(random() * 10))
    
    def test_petinfo(self):
        resp = self.client.post("/pet/petinfo", \
            {'wechatId' : 'wxid_testcase'})
        
        self.assertEqual(resp.status_code, 200)
        jsonResp = json.loads(resp.content)
        self.assertEqual(jsonResp['success'], 1)
        self.assertEqual(jsonResp['name'], 'Charizard')
        self.assertEqual(jsonResp['appearance'], 0)
        self.assertEqual(jsonResp['exp'], self._pet.experience)
        self.assertEqual(jsonResp['health'], self._pet.health)
        self.assertEqual(jsonResp['attack'], self._pet.attack)
        self.assertEqual(jsonResp['defend'], self._pet.defend)
        self.assertEqual(jsonResp['speed'], self._pet.speed)
        self.assertEqual(jsonResp['dodgeRate'], self._pet.dodgeRate)
    
    def test_petIllegal(self):
        resp = self.client.post("/pet/petinfo", \
            {'wechatId' : 'wechatId_testcase'})
        
        self.assertEqual(resp.status_code, 200)
        jsonResp = json.loads(resp.content)
        self.assertEqual(jsonResp['success'], 0)