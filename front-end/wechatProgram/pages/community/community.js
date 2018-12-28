// pages/user/user.js

var app = getApp()
var the_url = 'http://wangtong15.com:20001/community'

Page({
  data: {
    // list 
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
        if(res.data.success == 0){ // 不存在这个用户
        }
        else{
          that.list = res.data;
          //that.setData({ list: res.data }),
          console.log(that.list);
          for (var i = 0; i < that.list.length; ++i){
            that.list2[i].avatarUrl = that.list['vatarUrl'+i]
            that.list2[i].nickname = that.list['nickname'+i]
          }
        }
      },
    });

  },
})