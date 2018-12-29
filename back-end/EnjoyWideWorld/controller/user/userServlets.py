# This file includes all funtions handling HttpRequests
# in global usecase 'user'.
# ZHOU Kunpeng, 24 Dec 2018

from controller.servlet import AttribServlet
from controller.user import userDAOs

# Servlet for user/profile
# returns all informations displayed on 'user' screen
# request: GET or POST w/params
#   wechatId (string)
# response: user information to show
#   totalLikes (int)
# (For now, only returns total likes)

def getUserProfile(request):
    return GetUserProfileServlet().execute(request)

class GetUserProfileServlet(AttribServlet):
    def _action(self, request, response):
        userId = request.get('wechatId')
        profile = userDAOs.GetUserProfileDAO().getUserProfile(userId)
        response['totalLikes'] = profile['totalLikes']
        

# Servlet for user/openid
# Using the code from wx.login() at front-end, call code2session to get user's openid 
# which will become wechatId, the primary key for User.
# See https://developers.weixin.qq.com/miniprogram/dev/api/code2Session.html
# request: POST/GET w/params
#   code: the code obtained from wx.login() at front-end
# response: POST w/json
#   openid: the wechatid for this user
#   session_key: the session_key obtaied from code2session

import requests
import json

def getOpenId(request):
    return GetOpenIdServlet().execute(request)

class GetOpenIdServlet(AttribServlet):
    def _action(self, request, response):
        tempCode = request.get('code')

        # code2session
        # use tempCode to post request to wechat, getting openid, session_key and so
        APP_ID = "wxf6948f5ae095fe6c"
        APP_SECRET = "b02f7f8c0e9293087ebd8f0ae7a026d8"

        print("user/openid: code received " + str(tempCode))

        wxResp = requests.get("https://api.weixin.qq.com/sns/jscode2session", \
            {'appid' : APP_ID, 'secret' : APP_SECRET, 'js_code' : tempCode, \
             'grant_type' : 'authorization_code'})
        
        print("user/openid: status_code " + str(wxResp.status_code))
        print(wxResp.text)
        jsonResp = json.loads(wxResp.text)

        openid = jsonResp.get('openid')
        print("user/openid: openid " + str(openid))

        response['openid'] = openid
        response['session_key'] = jsonResp['session_key']
        # response['unionid'] = jsonResp['unionid']


# Servlet for user/add
# update the user info with given nickname, avatar, and other stuffs
# if user does not exist, then create one.
# request: POST/GET w/params
#   wechatId : the user to update
#   nickname, avatarurl, province, city: the informations to update
# response: POST w/json
#   success = 1 if successfully updated.

def updateUserInfo(request):
    return UpdateUserInfoServlet().execute(request)

class UpdateUserInfoServlet(AttribServlet):
    def _action(self, request, response):
        wechatId = request.get('wechatId')
        nickname = request.get('nickname', None)
        avatarurl = request.get('avatarurl', None)
        province = request.get('province', None)
        city = request.get('city', None)

        userDAOs.UpdateUserInfoDAO().updateUserInfo(wechatId, nickname, avatarurl, province, city)