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
        

