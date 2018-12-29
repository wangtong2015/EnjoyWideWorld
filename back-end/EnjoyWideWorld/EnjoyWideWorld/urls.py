"""EnjoyWideWorld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from controller.community import communityServlets
from controller.map import mapServlets
from controller.pet import petServlets
from controller.user import userServlets

from . import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^map/test$', mapServlets.test),
    url(r'^map/getpositions$', mapServlets.getPositions),
    url(r'^map/checkin$', mapServlets.checkIn),
    url(r'^pet/petinfo$', petServlets.getPetInfo),
    url(r'^community/friendsinfo$', communityServlets.getFriendsInfo),
    url(r'^community/usersnearby$', communityServlets.getUsersNearby),
    url(r'^community/nearbyinfo$', communityServlets.getNearbyInfo),
    url(r'^community/like$', communityServlets.likeDelike),
    url(r'^user/profile$', userServlets.getUserProfile),
    url(r'^user/openid$', userServlets.getOpenId),
    url(r'^user/add$', userServlets.updateUserInfo)
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
