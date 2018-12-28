# Test cases for global usecase 'pet'.
# ZHOU Kunpeng, 27 Dec 2018

from random import random
from math import floor
import json

from django.test import TestCase

from model import models

class UserTestCase(TestCase):
    # all users are created by posting requests. pass
    def setUp(self):
        pass
    
    def test_userUpdate(self):
        numOfUsers = 30
        numOfUpdates = 100
        # create some users using http request
        for k in range(numOfUsers):
            resp = self.client.post("/user/add",        \
                {'wechatId' : 'usertestcase' + str(k),  \
                 'nickname' : 'nickname' + str(k),      \
                 'avatarurl' : '127.0.0.1:100' + str(k),\
                 'province' : 'Peking',                 \
                 'city' : 'Haidian'})

            self.assertEqual(resp.status_code, 200)
            jsonResp = json.loads(resp.content)
            self.assertEqual(jsonResp['success'], 1)
        
        # update their info
        for k in range(numOfUpdates):
            target = floor(random() * numOfUsers)
            omit = floor(random() * 2)
            randy = floor(random() * 100)
            if omit == 0:
                resp = self.client.post("/user/add",            \
                {'wechatId' : 'usertestcase' + str(target),     \
                 'nickname' : 'nicknameUpd' + str(randy),       \
                 'avatarurl' : '127.0.0.1:200' + str(randy),    \
                 'province' : 'Tianjin' + str(randy),           \
                 'city' : 'Nankai' + str(randy)})
            else:
                resp = self.client.post("/user/add",         \
                {'wechatId' : 'usertestcase' + str(target),  \
                 'nickname' : 'nicknameUpd' + str(randy)})
            
            self.assertEqual(resp.status_code, 200)
            jsonResp = json.loads(resp.content)
            self.assertEqual(jsonResp['success'], 1)

            user = models.User.objects.get(wechatId = 'usertestcase' + str(target))
            self.assertEqual(user.nickname, 'nicknameUpd' + str(randy))
            if omit == 0:
                self.assertEqual(user.avatarUrl, '127.0.0.1:200' + str(randy))
                self.assertEqual(user.province, 'Tianjin' + str(randy))
                self.assertEqual(user.city, 'Nankai' + str(randy))
