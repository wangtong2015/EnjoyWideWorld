// pages/user/user.js

var app = getApp()
var the_url = 'http://wangtong15.com:20001/community'

Page({
  data: {
    list: null,
    list2: [],
    hidden:false,
  },


  onLoad: function (options) {
    var that = this;
    //加载数据
    wx.request({
      url: the_url + '/nearbyinfo',
      data: {
        user: app.globalData.openid,
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
          nickname: e.data["nickname" + i],
          wechatId: e.data["wechatId" + i],
        }
      };
      this.setData({ list2: list2 })
    }
  },
  returntape: function(e){
    this.setData({ my_modal_hidden: true })
  },
  tape: function(e){
    this.setData({hidden:true})
  },
  tape2: function (e) {
    this.setData({ hidden: false })
  }
})