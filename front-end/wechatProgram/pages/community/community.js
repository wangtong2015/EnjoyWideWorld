// pages/user/user.js

var app = getApp()
var the_url = 'http://wangtong15.com:20001/community'

Page({
  data: {
    list: null,
    list2: []
  },


  onLoad: function (options) {
    var that = this;
    wx.showLoading({
      title: '加载中',
    })
    //加载数据
    wx.request({
      url: the_url + '/nearbyinfo',
      data: {
        user: 'hhp1210384183', // app.globalData.openid
        latitude: app.globalData.latitude,
        longitude: app.globalData.longitude
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded' // 默认值
      },
      method: 'POST',
      success: function (res) {
        that.abc(res);
      },
    });
  },
  abc: function(e){
    var list2 = [];
    console.log(e.data);
    if (e.data.success == 0) { // 不存在这个用户
    }
    else {
      this.setData({ list: e.data });
      
      for (var i = 0; i < e.data.length; i++) {
        list2[i] = {
          avatarUrl: e.data["avatarUrl" + i],
          exp: e.data["exp" + i],
          isLiked: e.data["isLiked" + i],
          nickName: e.data["nickName" + i],
          wechatId: e.data["wechatId" + i],
        }
      };
      this.setData({ list2: list2 })
    }
  }
})