# Test cases for global usecase 'pet'.
# ZHOU Kunpeng, 27 Dec 2018

from random import random
from math import floor
import json

from django.test import TestCase

from model import models

class PetTestCase(TestCase):

    # create pet
    def _petSetup(self):
        self._pet = models.Pet.objects.create(master=self._user, \
            name='Charizard',                        \
            experience=floor(random() * 2900 + 100), \
            appearanceId=0,                     \
            health=floor(random() * 300 + 100), \
            attack=floor(random() * 20 + 5),    \
            defend=floor(random() * 20 + 5),    \
            speed=floor(random() * 20 + 5),     \
            dodgeRate=floor(random() * 10))

    # when setting up, create user first and create pet when calling test_xxx() each.
    # this is for not conflicting with test_create().
    def setUp(self):
        self._user = models.User.objects.create(wechatId='wxid_testcase')
    
    # temporary create a pet and check its status
    def test_create(self):
        resp = self.client.post("/pet/add", \
            {'wechatId' : 'wxid_testcase', \
             'characterName' : 'Charizardo',                 \
             'characterExp' : floor(random() * 2900 + 100), \
             'characterAppearance' : 0,                     \
             'characterHP' : floor(random() * 300 + 100),   \
             'characterAD' : floor(random() * 20 + 5),      \
             'characterDF' : floor(random() * 20 + 5),      \
             'characterSP' : floor(random() * 20 + 5),      \
             'characterMiss' : floor(random() * 10)})
        self.assertEqual(resp.status_code, 200)
        jsonResp = json.loads(resp.content)
        self.assertEqual(jsonResp['success'], 1)
        self._pet = models.Pet.objects.get(id=jsonResp['characterID'])
        self.assertEqual(self._pet.name, 'Charizardo')
        self.assertEqual(self._pet.master.wechatId, 'wxid_testcase')
        self._pet.delete()

    # re-setup a pet and get its info
    def test_petinfo(self):
        self._petSetup()
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
    
    # re-setup a pet and try to get its info with an incorrect user id
    def test_petIllegal(self):
        self._petSetup()
        resp = self.client.post("/pet/petinfo", \
            {'wechatId' : 'wechatId_testcase'})
        
        self.assertEqual(resp.status_code, 200)
        jsonResp = json.loads(resp.content)
        self.assertEqual(jsonResp['success'], 0)